# -*- coding: utf-8 -*-
"""
SuperJus - Pipeline de OCR Automatizado para Inquéritos e Documentos Digitalizados
==================================================================================
Escaneia pastas de clientes (c:\\Projetos\\superJus\\Clientes\\), detecta PDFs que são
imagens puras ou contêm anexos digitalizados sem camada de texto selecionável,
e aplica OCR em português brasileiro preservando carimbos, assinaturas, selos
e o layout original do tribunal/delegacia.

Dependências externas:
  - Tesseract-OCR (com suporte ao idioma 'por')
  - OCRmyPDF (>= 16.0.0)
  - PyTesseract (>= 0.3.10)
  - PyMuPDF (fitz) ou pypdf para inspeção e métricas
"""

import argparse
import datetime
import json
import logging
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Reconfigurar stdout para UTF-8 no Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("OCRmyPDF_Sanitizer")

# ==============================================================================
# CONFIGURAÇÃO E TRATAMENTO DE AMBIENTE WINDOWS (FALLBACKS DO TESSERACT)
# ==============================================================================

TESSERACT_CANDIDATE_PATHS = [
    os.environ.get("TESSERACT_CMD", ""),
    os.environ.get("TESSERACT_PATH", ""),
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe"),
    os.path.expandvars(r"%USERPROFILE%\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"),
    r"C:\tools\tesseract\tesseract.exe",
    r"C:\ProgramData\chocolatey\bin\tesseract.exe",
]


def resolve_tesseract_path() -> Optional[str]:
    """Localiza o binário do Tesseract no Windows com múltiplos fallbacks."""
    # 1. Verificar se tesseract já está acessível no PATH do sistema
    which_path = shutil.which("tesseract")
    if which_path and os.path.isfile(which_path):
        return os.path.abspath(which_path)

    # 2. Verificar lista de caminhos comuns do Windows
    for path_str in TESSERACT_CANDIDATE_PATHS:
        if path_str and os.path.isfile(path_str):
            return os.path.abspath(path_str)

    return None


def setup_tesseract_environment() -> Dict[str, Any]:
    """
    Configura variáveis de ambiente (PATH, TESSDATA_PREFIX) e vincula
    ao pytesseract e ocrmypdf de forma transparente.
    """
    tess_exe = resolve_tesseract_path()
    env_info = {
        "tesseract_found": False,
        "tesseract_path": None,
        "tessdata_path": None,
        "languages": [],
        "has_por": False,
        "ocrmypdf_available": False,
        "pytesseract_available": False,
        "ocrmypdf_version": None,
        "pytesseract_version": None,
    }

    if tess_exe:
        tess_dir = os.path.dirname(tess_exe)
        env_info["tesseract_found"] = True
        env_info["tesseract_path"] = tess_exe

        # Injetar pasta do Tesseract no PATH do processo para subprocessos do OCRmyPDF
        curr_path = os.environ.get("PATH", "")
        if tess_dir.lower() not in curr_path.lower():
            os.environ["PATH"] = f"{tess_dir};{curr_path}"

        # Localizar tessdata
        tessdata_candidates = [
            os.environ.get("TESSDATA_PREFIX", ""),
            os.path.join(tess_dir, "tessdata"),
            r"C:\Program Files\Tesseract-OCR\tessdata",
        ]
        found_tessdata = None
        for td in tessdata_candidates:
            if td and os.path.isdir(td):
                found_tessdata = os.path.abspath(td)
                break

        if found_tessdata:
            os.environ["TESSDATA_PREFIX"] = found_tessdata
            env_info["tessdata_path"] = found_tessdata
            # Listar idiomas instalados
            langs = [
                f.replace(".traineddata", "")
                for f in os.listdir(found_tessdata)
                if f.endswith(".traineddata")
            ]
            env_info["languages"] = langs
            env_info["has_por"] = "por" in langs

    # Verificar e configurar pytesseract
    try:
        import pytesseract

        env_info["pytesseract_available"] = True
        env_info["pytesseract_version"] = getattr(pytesseract, "__version__", "unknown")
        if tess_exe:
            pytesseract.pytesseract.tesseract_cmd = tess_exe
    except ImportError:
        pass

    # Verificar ocrmypdf
    try:
        import ocrmypdf

        env_info["ocrmypdf_available"] = True
        env_info["ocrmypdf_version"] = getattr(ocrmypdf, "__version__", "unknown")
    except ImportError:
        pass

    return env_info


# ==============================================================================
# MOTOR DE ANÁLISE DE PDFS (DETECÇÃO DE IMAGENS PURAS E AUSÊNCIA DE TEXTO)
# ==============================================================================

def analyze_pdf(pdf_path: str, threshold_chars_per_page: int = 40) -> Dict[str, Any]:
    """
    Inspeciona o PDF página por página para classificar se é:
      - 'PURE_SCAN': Todas as páginas são imagens puras (sem texto selecionável).
      - 'PARTIAL_SCAN': Mistura de páginas com e sem texto (comum em anexos de inquérito).
      - 'ALREADY_SEARCHABLE': Todas as páginas possuem texto selecionável acima do threshold.
      - 'EMPTY_OR_CORRUPT': Arquivo ilegível ou vazio.
    """
    res = {
        "file_path": str(pdf_path),
        "file_name": os.path.basename(pdf_path),
        "file_size_bytes": 0,
        "total_pages": 0,
        "pages_with_text": 0,
        "pages_without_text": 0,
        "total_chars": 0,
        "avg_chars_per_page": 0.0,
        "image_count": 0,
        "classification": "UNKNOWN",
        "needs_ocr": False,
        "page_details": [],
        "error": None,
    }

    if not os.path.isfile(pdf_path):
        res["error"] = "Arquivo não encontrado."
        res["classification"] = "NOT_FOUND"
        return res

    res["file_size_bytes"] = os.path.getsize(pdf_path)

    # Tentativa primária: PyMuPDF (fitz)
    try:
        import pymupdf

        doc = pymupdf.open(pdf_path)
        res["total_pages"] = len(doc)

        if res["total_pages"] == 0:
            res["classification"] = "EMPTY_OR_CORRUPT"
            doc.close()
            return res

        for page_idx in range(len(doc)):
            page = doc[page_idx]
            text = page.get_text().strip()
            char_count = len(text)
            images = page.get_images()
            img_count = len(images)

            res["total_chars"] += char_count
            res["image_count"] += img_count

            has_sufficient_text = char_count >= threshold_chars_per_page
            if has_sufficient_text:
                res["pages_with_text"] += 1
            else:
                res["pages_without_text"] += 1

            res["page_details"].append(
                {
                    "page_number": page_idx + 1,
                    "chars": char_count,
                    "images": img_count,
                    "has_text": has_sufficient_text,
                }
            )

        doc.close()

    except Exception as e_fitz:
        # Tentativa secundária: pypdf
        try:
            from pypdf import PdfReader

            reader = PdfReader(pdf_path)
            res["total_pages"] = len(reader.pages)

            if res["total_pages"] == 0:
                res["classification"] = "EMPTY_OR_CORRUPT"
                return res

            for page_idx, page in enumerate(reader.pages):
                text = (page.extract_text() or "").strip()
                char_count = len(text)
                res["total_chars"] += char_count

                has_sufficient_text = char_count >= threshold_chars_per_page
                if has_sufficient_text:
                    res["pages_with_text"] += 1
                else:
                    res["pages_without_text"] += 1

                res["page_details"].append(
                    {
                        "page_number": page_idx + 1,
                        "chars": char_count,
                        "images": len(page.images) if hasattr(page, "images") else 0,
                        "has_text": has_sufficient_text,
                    }
                )
        except Exception as e_pypdf:
            res["error"] = f"Falha na leitura (PyMuPDF: {e_fitz}; pypdf: {e_pypdf})"
            res["classification"] = "EMPTY_OR_CORRUPT"
            return res

    # Contabilização refinada de páginas escaneadas vs em branco
    pages_scanned = 0
    pages_blank = 0
    for p in res["page_details"]:
        if not p["has_text"]:
            if p["images"] == 0 and p["chars"] == 0:
                pages_blank += 1
            else:
                pages_scanned += 1

    res["pages_scanned"] = pages_scanned
    res["pages_blank"] = pages_blank

    # Classificação precisa
    if res["total_pages"] > 0 and res["total_chars"] == 0:
        res["classification"] = "PURE_SCAN"
        res["needs_ocr"] = True
    elif pages_scanned > 0:
        res["classification"] = "PARTIAL_SCAN"
        res["needs_ocr"] = True
    else:
        res["classification"] = "ALREADY_SEARCHABLE"
        res["needs_ocr"] = False

    return res


# ==============================================================================
# MOTOR DE PROCESSAMENTO OCR (OCRMYPDF)
# ==============================================================================

class OCRSanitizer:
    """Controlador principal do pipeline de OCR do SuperJus."""

    def __init__(
        self,
        language: str = "por",
        threshold_chars: int = 40,
        deskew: bool = True,
        rotate_pages: bool = True,
        create_backup: bool = True,
        skip_text: bool = True,
        force_ocr: bool = False,
    ):
        self.language = language
        self.threshold_chars = threshold_chars
        self.deskew = deskew
        self.rotate_pages = rotate_pages
        self.create_backup = create_backup
        self.skip_text = skip_text
        self.force_ocr = force_ocr
        self.env_info = setup_tesseract_environment()

    def check_readiness(self) -> Tuple[bool, str]:
        """Verifica se todas as dependências estão operacionais."""
        if not self.env_info["tesseract_found"]:
            return (
                False,
                "Tesseract-OCR não encontrado nos caminhos padrão do Windows ou PATH. "
                "Instale via: winget install UB-Mannheim.TesseractOCR",
            )
        if not self.env_info["has_por"] and "por" in self.language:
            return (
                False,
                f"Tesseract encontrado ({self.env_info['tesseract_path']}), "
                "mas o pacote de idioma 'por.traineddata' não está em tessdata.",
            )
        if not self.env_info["ocrmypdf_available"]:
            return (
                False,
                "Biblioteca 'ocrmypdf' não instalada no ambiente Python. Execute: pip install ocrmypdf",
            )
        return True, "Ambiente OCR pronto e operacional."

    def process_file(
        self,
        input_pdf_path: str,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """
        Executa o pipeline completo em um arquivo PDF:
          1. Análise inicial
          2. Decisão de necessidade de OCR
          3. Backup de segurança
          4. Execução do OCRmyPDF preservando carimbos e layout
          5. Validação pós-OCR e cálculo de ganho de texto
        """
        start_time = time.time()
        result = {
            "file_path": str(input_pdf_path),
            "file_name": os.path.basename(input_pdf_path),
            "status": "SKIPPED",
            "dry_run": dry_run,
            "classification": "UNKNOWN",
            "chars_before": 0,
            "chars_after": 0,
            "chars_added": 0,
            "total_pages": 0,
            "duration_seconds": 0.0,
            "backup_path": None,
            "error_message": None,
        }

        # 1. Análise inicial
        analysis = analyze_pdf(input_pdf_path, self.threshold_chars)
        result["classification"] = analysis["classification"]
        result["chars_before"] = analysis["total_chars"]
        result["total_pages"] = analysis["total_pages"]

        if analysis["error"]:
            result["status"] = "ERROR"
            result["error_message"] = analysis["error"]
            result["duration_seconds"] = round(time.time() - start_time, 2)
            return result

        needs_action = analysis["needs_ocr"] or self.force_ocr

        if not needs_action:
            result["status"] = "ALREADY_SEARCHABLE"
            result["chars_after"] = result["chars_before"]
            result["duration_seconds"] = round(time.time() - start_time, 2)
            return result

        if dry_run:
            result["status"] = "NEEDS_OCR"
            result["duration_seconds"] = round(time.time() - start_time, 2)
            return result

        # 2. Verificar prontidão do ambiente
        ready, reason = self.check_readiness()
        if not ready:
            result["status"] = "ERROR"
            result["error_message"] = reason
            result["duration_seconds"] = round(time.time() - start_time, 2)
            return result

        import ocrmypdf
        import ocrmypdf.exceptions

        abs_input = os.path.abspath(input_pdf_path)
        dir_name = os.path.dirname(abs_input)
        base_name = os.path.basename(abs_input)

        # 3. Criar backup se solicitado
        backup_path = None
        if self.create_backup:
            backup_dir = os.path.join(dir_name, "_scanned_backups")
            os.makedirs(backup_dir, exist_ok=True)
            backup_path = os.path.join(backup_dir, f"{base_name}.scanned_backup.pdf")
            try:
                shutil.copy2(abs_input, backup_path)
                result["backup_path"] = backup_path
            except Exception as e_bkp:
                logger.warning(f"Não foi possível criar backup de {base_name}: {e_bkp}")

        # 4. Arquivo temporário de saída
        temp_fd, temp_output = tempfile.mkstemp(
            prefix="superjus_ocr_", suffix=".pdf", dir=dir_name
        )
        os.close(temp_fd)

        try:
            logger.info(f"Iniciando OCR em: {base_name} ({analysis['classification']}, {analysis['total_pages']} págs)...")

            # Configurações do OCRmyPDF para preservar fidelidade absoluta
            ocr_kwargs = {
                "language": self.language,
                "deskew": self.deskew,
                "rotate_pages": self.rotate_pages,
                "invalidate_digital_signatures": True,  # Permite processar peças com assinaturas do PJe
                "optimize": 1,                         # Otimização lossless preservando carimbos
                "output_type": "pdf",                  # Mantém formato PDF padrão
                "progress_bar": False,
            }

            if self.force_ocr:
                ocr_kwargs["redo_ocr"] = True
            elif self.skip_text:
                ocr_kwargs["skip_text"] = True

            exit_code = ocrmypdf.ocr(abs_input, temp_output, **ocr_kwargs)

            if exit_code != 0 and not os.path.exists(temp_output):
                raise RuntimeError(f"OCRmyPDF encerrou com código {exit_code}")

            # 5. Validação pós-OCR
            post_analysis = analyze_pdf(temp_output, self.threshold_chars)
            chars_after = post_analysis["total_chars"]
            result["chars_after"] = chars_after
            result["chars_added"] = max(0, chars_after - result["chars_before"])

            # Substituição atômica
            shutil.move(temp_output, abs_input)
            result["status"] = "SUCCESS"
            logger.info(
                f"OCR concluído com sucesso: {base_name} | "
                f"Chars: {result['chars_before']} -> {result['chars_after']} (+{result['chars_added']})"
            )

        except ocrmypdf.exceptions.PriorOcrFoundError:
            result["status"] = "ALREADY_SEARCHABLE"
            result["chars_after"] = result["chars_before"]
            if os.path.exists(temp_output):
                os.remove(temp_output)
            logger.info(f"Ignorado (já possui OCR completo): {base_name}")

        except Exception as e_ocr:
            result["status"] = "ERROR"
            result["error_message"] = str(e_ocr)
            if os.path.exists(temp_output):
                os.remove(temp_output)
            logger.error(f"Erro ao processar OCR em {base_name}: {e_ocr}")

        result["duration_seconds"] = round(time.time() - start_time, 2)
        return result

    def scan_and_process(
        self,
        target_dir: str,
        client_filter: Optional[str] = None,
        dry_run: bool = False,
    ) -> List[Dict[str, Any]]:
        """Varre recursivamente a pasta de clientes e processa todos os PDFs elegíveis."""
        target_path = Path(target_dir).resolve()
        if not target_path.exists():
            raise FileNotFoundError(f"Diretório não encontrado: {target_path}")

        logger.info(f"Iniciando varredura em: {target_path}")
        if client_filter:
            logger.info(f"Filtro de cliente ativo: {client_filter}")

        pdf_files: List[Path] = []
        for root, dirs, files in os.walk(target_path):
            # Ignorar diretórios internos de backup e caches
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".")
                and d not in ["_scanned_backups", "__pycache__", "node_modules"]
            ]

            if client_filter:
                rel = os.path.relpath(root, target_path)
                parts = rel.split(os.sep)
                if parts and parts[0] != "." and client_filter.lower() not in parts[0].lower():
                    continue

            for f in files:
                if f.lower().endswith(".pdf") and not f.endswith(".scanned_backup.pdf"):
                    pdf_files.append(Path(root) / f)

        logger.info(f"Total de PDFs encontrados para auditoria: {len(pdf_files)}")

        results = []
        for idx, pdf in enumerate(pdf_files, 1):
            logger.info(f"[{idx}/{len(pdf_files)}] Inspecionando: {pdf.name}")
            res = self.process_file(str(pdf), dry_run=dry_run)
            res["relative_path"] = str(pdf.relative_to(target_path))
            results.append(res)

        return results


# ==============================================================================
# GERAÇÃO DE RELATÓRIOS (MARKDOWN E JSON)
# ==============================================================================

def generate_reports(
    results: List[Dict[str, Any]],
    env_info: Dict[str, Any],
    output_dir: str,
    dry_run: bool = False,
) -> Tuple[str, str]:
    """Gera relatórios estruturados em Markdown e JSON."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    mode_str = "SIMULACAO_DRYRUN" if dry_run else "EXECUCAO_REAL"

    json_path = os.path.join(output_dir, f"relatorio_ocr_{mode_str}_{timestamp}.json")
    md_path = os.path.join(output_dir, f"relatorio_ocr_{mode_str}_{timestamp}.md")

    total_scanned = len(results)
    pure_scans = sum(1 for r in results if r.get("classification") == "PURE_SCAN")
    partial_scans = sum(1 for r in results if r.get("classification") == "PARTIAL_SCAN")
    searchable = sum(1 for r in results if r.get("classification") == "ALREADY_SEARCHABLE")
    success_ocr = sum(1 for r in results if r.get("status") == "SUCCESS")
    needs_ocr = sum(1 for r in results if r.get("status") == "NEEDS_OCR")
    errors = sum(1 for r in results if r.get("status") == "ERROR")
    total_chars_added = sum(r.get("chars_added", 0) for r in results)
    total_duration = sum(r.get("duration_seconds", 0.0) for r in results)

    report_payload = {
        "timestamp": timestamp,
        "mode": "DRY_RUN" if dry_run else "LIVE_EXECUTION",
        "system_environment": env_info,
        "summary": {
            "total_files_audited": total_scanned,
            "pure_scans_detected": pure_scans,
            "partial_scans_detected": partial_scans,
            "already_searchable": searchable,
            "successfully_ocred": success_ocr,
            "pending_ocr_dryrun": needs_ocr,
            "errors": errors,
            "total_characters_added": total_chars_added,
            "total_duration_seconds": round(total_duration, 2),
        },
        "details": results,
    }

    with open(json_path, "w", encoding="utf-8") as f_json:
        json.dump(report_payload, f_json, ensure_ascii=False, indent=2)

    md_content = f"""# 📄 Relatório de OCR Automatizado — SuperJus
**Data/Hora:** {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}  
**Modo de Execução:** `{'SIMULAÇÃO (DRY-RUN)' if dry_run else 'APLICAÇÃO REAL'}`  
**Ambiente:** Tesseract `{env_info.get('tesseract_path') or 'N/A'}` | Idiomas: `{', '.join(env_info.get('languages', []))}`

---

## 📊 Resumo Executivo

| Métrica | Quantidade |
| :--- | :--- |
| **Total de PDFs Auditados** | **{total_scanned}** |
| **Documentos 100% Imagem (Pure Scan)** | **{pure_scans}** |
| **Documentos com Anexos Sem Texto (Partial Scan)** | **{partial_scans}** |
| **Documentos já Pesquisáveis (Born-digital / OCR)** | **{searchable}** |
| **Documentos Processados com Sucesso** | **{success_ocr}** |
| **Documentos com Pendência de OCR (Identificados)** | **{needs_ocr}** |
| **Erros Encontrados** | **{errors}** |
| **Caracteres Textuais Adicionados** | **+{total_chars_added:,} chars** |
| **Tempo Total de Processamento** | **{round(total_duration, 1)}s** |

---

## 📋 Detalhamento dos Arquivos

| Arquivo | Classificação | Status | Págs | Chars Antes | Chars Depois | Ganho | Duração |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
"""

    for r in results:
        fname = r.get("file_name", "Desconhecido")
        rel_p = r.get("relative_path", fname)
        cls_name = r.get("classification", "-")
        status_name = r.get("status", "-")
        pages = r.get("total_pages", 0)
        c_before = r.get("chars_before", 0)
        c_after = r.get("chars_after", 0)
        c_diff = r.get("chars_added", 0)
        dur = r.get("duration_seconds", 0.0)

        badge = status_name
        if status_name == "SUCCESS":
            badge = "✅ Sucesso"
        elif status_name == "NEEDS_OCR":
            badge = "🔍 OCR Necessário"
        elif status_name == "ALREADY_SEARCHABLE":
            badge = "ℹ️ Já Pesquisável"
        elif status_name == "ERROR":
            badge = "❌ Erro"

        md_content += f"| `{rel_p}` | {cls_name} | {badge} | {pages} | {c_before} | {c_after} | +{c_diff} | {dur}s |\n"

    md_content += """
---

## ⚙️ Orientações de Preservação e Segurança Jurídica
- **Camada Invisível (Sandwich):** O OCRmyPDF posiciona o texto reconhecido diretamente sobre/sob o mapa de bits original, assegurando que carimbos de protocolo, rubricas, assinaturas manuais e marcas d'água permaneçam 100% visíveis e fidedignos.
- **Validação de Integridade:** Cada arquivo modificado possui cópia de segurança salva em `_scanned_backups/` com a extensão `.scanned_backup.pdf`.
"""

    with open(md_path, "w", encoding="utf-8") as f_md:
        f_md.write(md_content)

    return json_path, md_path


# ==============================================================================
# CLI PRINCIPAL
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="SuperJus - Pipeline de OCR Automatizado para Inquéritos e Documentos Digitalizados"
    )
    parser.add_argument(
        "--path",
        "-p",
        default=r"c:\Projetos\superJus\Clientes",
        help="Diretório raiz para varredura (Padrão: c:\\Projetos\\superJus\\Clientes)",
    )
    parser.add_argument(
        "--client",
        "-c",
        default=None,
        help="Filtrar por nome de cliente específico (ex.: Julio_Pereira_Marcos)",
    )
    parser.add_argument(
        "--file",
        "-f",
        default=None,
        help="Processar um arquivo PDF específico individualmente",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Apenas audita e gera relatório de PDFs que precisam de OCR, sem modificar arquivos",
    )
    parser.add_argument(
        "--force",
        "--redo-ocr",
        action="store_true",
        help="Força a reexecução de OCR mesmo se o PDF já possuir texto selecionável",
    )
    parser.add_argument(
        "--lang",
        "-l",
        default="por",
        help="Código do idioma do Tesseract (Padrão: por para português brasileiro)",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=40,
        help="Quantidade mínima de caracteres por página para considerar texto selecionável (Padrão: 40)",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Desativa a criação de backups dos PDFs originais digitalizados",
    )
    parser.add_argument(
        "--no-deskew",
        action="store_true",
        help="Desativa a rotação/desinclinação automática de páginas tortas",
    )
    parser.add_argument(
        "--no-rotate",
        action="store_true",
        help="Desativa a detecção de orientação de páginas",
    )
    parser.add_argument(
        "--report-dir",
        default=r"c:\Projetos\superJus\docs\relatorios_ocr",
        help="Pasta de saída dos relatórios Markdown e JSON (Padrão: c:\\Projetos\\superJus\\docs\\relatorios_ocr)",
    )
    parser.add_argument(
        "--check-env",
        action="store_true",
        help="Apenas verifica a instalação do Tesseract, pacotes Python e status do ambiente",
    )

    args = parser.parse_args()

    # Modo de verificação de ambiente
    if args.check_env:
        print("\n=== VERIFICAÇÃO DO AMBIENTE OCR — SUPERJUS ===")
        env = setup_tesseract_environment()
        print(f"• Tesseract encontrado: {'SIM' if env['tesseract_found'] else 'NÃO'}")
        print(f"• Binário: {env['tesseract_path']}")
        print(f"• Tessdata: {env['tessdata_path']}")
        print(f"• Idiomas disponíveis: {', '.join(env['languages']) if env['languages'] else 'Nenhum'}")
        print(f"• Suporte a Português (por): {'SIM' if env['has_por'] else 'NÃO'}")
        print(f"• OCRmyPDF: {'SIM (v' + str(env['ocrmypdf_version']) + ')' if env['ocrmypdf_available'] else 'NÃO'}")
        print(f"• PyTesseract: {'SIM (v' + str(env['pytesseract_version']) + ')' if env['pytesseract_available'] else 'NÃO'}")
        print("==============================================\n")
        return

    sanitizer = OCRSanitizer(
        language=args.lang,
        threshold_chars=args.threshold,
        deskew=not args.no_deskew,
        rotate_pages=not args.no_rotate,
        create_backup=not args.no_backup,
        skip_text=True,
        force_ocr=args.force,
    )

    # Modo arquivo único
    if args.file:
        file_path = os.path.abspath(args.file)
        if not os.path.exists(file_path):
            logger.error(f"Arquivo não encontrado: {file_path}")
            sys.exit(1)
        res = sanitizer.process_file(file_path, dry_run=args.dry_run)
        json_p, md_p = generate_reports(
            [res], sanitizer.env_info, args.report_dir, dry_run=args.dry_run
        )
        print(f"\nProcessamento concluído. Relatório salvo em:\n  MD: {md_p}\n  JSON: {json_p}")
        return

    # Modo varredura recursiva de clientes
    results = sanitizer.scan_and_process(
        target_dir=args.path,
        client_filter=args.client,
        dry_run=args.dry_run,
    )

    json_p, md_p = generate_reports(
        results, sanitizer.env_info, args.report_dir, dry_run=args.dry_run
    )

    print("\n" + "=" * 60)
    print("RESUMO DA OPERAÇÃO DE OCR:")
    print(f"  • Total auditados: {len(results)}")
    print(f"  • Pure Scans: {sum(1 for r in results if r['classification'] == 'PURE_SCAN')}")
    print(f"  • Partial Scans: {sum(1 for r in results if r['classification'] == 'PARTIAL_SCAN')}")
    print(f"  • Já pesquisáveis: {sum(1 for r in results if r['classification'] == 'ALREADY_SEARCHABLE')}")
    print(f"  • Sucesso no OCR: {sum(1 for r in results if r['status'] == 'SUCCESS')}")
    print(f"  • Pendentes (dry-run): {sum(1 for r in results if r['status'] == 'NEEDS_OCR')}")
    print(f"  • Erros: {sum(1 for r in results if r['status'] == 'ERROR')}")
    print(f"\nRelatórios gerados:")
    print(f"  Markdown: {md_p}")
    print(f"  JSON:     {json_p}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
