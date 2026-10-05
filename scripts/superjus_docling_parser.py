# -*- coding: utf-8 -*-
"""
SuperJus Docling Parser - Módulo Mestre de Conversão de PDFs Jurídicos
=======================================================================
Converte PDFs jurídicos complexos (sentenças criminais com dosimetria,
inquéritos policiais, laudos telemáticos, interceptações telefônicas e
espelhos processuais) em Markdown estruturado preservando tabelas,
cabeçalhos e hierarquias.

Recursos:
1. Motor Primário: IBM Docling 2.x (TableFormer em modo ACCURATE/FAST).
2. Fallback Inteligente Nativo: PyMuPDF (fitz) com `page.find_tables()`
   automático caso dependências de IA falhem ou sejam executadas em ambiente restrito.
3. Otimização Adaptativa de OCR (Auto/Force/Off) para máxima velocidade em PDFs digitais.
4. Extrator Especializado de Direito Penal & Processual Penal:
   - Mapeamento e estruturação de Dosimetria da Pena (Arts. 59 e 68 do CP).
   - Auditoria de Interceptações Telefônicas & Telemática (confronto vocálico e cadeia de custódia).
   - Detecção e normalização de números de processo CNJ.
5. Exportação simultânea para Markdown (.md), Tabelas em JSON e DataFrames Pandas.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import logging
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Garantir UTF-8 na saída padrão em ambiente Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [SuperJus-Docling] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("superjus_docling")

# ---------------------------------------------------------------------------
# Verificação de dependências disponíveis
# ---------------------------------------------------------------------------
DOCLING_AVAILABLE = False
try:
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
    from docling.datamodel.base_models import InputFormat
    DOCLING_AVAILABLE = True
except ImportError:
    DOCLING_AVAILABLE = False

PYMUPDF_AVAILABLE = False
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False


# ---------------------------------------------------------------------------
# Estruturas de Dados
# ---------------------------------------------------------------------------
@dataclasses.dataclass
class ExtractedTable:
    index: int
    page: int
    rows_count: int
    cols_count: int
    headers: List[str]
    rows: List[List[str]]
    markdown: str
    dataframe_dict: Optional[List[Dict[str, Any]]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "page": self.page,
            "rows_count": self.rows_count,
            "cols_count": self.cols_count,
            "headers": self.headers,
            "rows": self.rows,
            "markdown": self.markdown,
        }


@dataclasses.dataclass
class DosimetriaAnalysis:
    detectada: bool = False
    pena_base: Optional[str] = None
    circunstancias_judiciais: List[str] = dataclasses.field(default_factory=list)
    atenuantes: List[str] = dataclasses.field(default_factory=list)
    agravantes: List[str] = dataclasses.field(default_factory=list)
    causas_aumento: List[str] = dataclasses.field(default_factory=list)
    causas_diminuicao: List[str] = dataclasses.field(default_factory=list)
    trafico_privilegiado: Optional[str] = None
    pena_definitiva: Optional[str] = None
    regime_inicial: Optional[str] = None
    substituicao_prd: Optional[str] = None
    trecho_relevante: Optional[str] = None

    def to_markdown(self) -> str:
        if not self.detectada:
            return ""
        lines = [
            "\n### ⚖️ Auditoria Especializada de Dosimetria da Pena (Arts. 59 e 68 do CP)",
            "",
            "| Etapa Trifásica | Detalhamento Detectado na Decisão |",
            "| :--- | :--- |",
        ]
        if self.pena_base:
            lines.append(f"| **1ª Fase (Pena-Base)** | {self.pena_base} |")
        if self.circunstancias_judiciais:
            circ_str = "<br>• " + "<br>• ".join(self.circunstancias_judiciais[:4])
            lines.append(f"| **Circunstâncias Judiciais (Art. 59)** | {circ_str} |")
        if self.atenuantes or self.agravantes:
            fase2 = []
            if self.atenuantes:
                fase2.append("Atenuantes: " + ", ".join(self.atenuantes))
            if self.agravantes:
                fase2.append("Agravantes: " + ", ".join(self.agravantes))
            lines.append(f"| **2ª Fase (Atenuantes/Agravantes)** | {'<br>'.join(fase2)} |")
        if self.causas_aumento or self.causas_diminuicao or self.trafico_privilegiado:
            fase3 = []
            if self.trafico_privilegiado:
                fase3.append(f"§ 4º Art. 33 (Tráfico Privilegiado): {self.trafico_privilegiado}")
            if self.causas_diminuicao:
                fase3.append("Diminuições: " + ", ".join(self.causas_diminuicao))
            if self.causas_aumento:
                fase3.append("Aumentos/Majorantes: " + ", ".join(self.causas_aumento))
            lines.append(f"| **3ª Fase (Majorantes/Minorantes)** | {'<br>'.join(fase3)} |")
        if self.pena_definitiva:
            lines.append(f"| **Pena Definitiva Fixada** | **{self.pena_definitiva}** |")
        if self.regime_inicial:
            lines.append(f"| **Regime Inicial de Cumprimento** | {self.regime_inicial} |")
        if self.substituicao_prd:
            lines.append(f"| **Substituição por Restritivas (Art. 44)** | {self.substituicao_prd} |")
        lines.append("")
        return "\n".join(lines)


@dataclasses.dataclass
class InterceptacaoAudit:
    detectada: bool = False
    total_dialogos_identificados: int = 0
    alvos_mencionados: List[str] = dataclasses.field(default_factory=list)
    telefones_ou_imeis: List[str] = dataclasses.field(default_factory=list)
    alerta_confronto_vocalico: bool = False
    alerta_cadeia_custodia: bool = False
    resumo_analitico: Optional[str] = None

    def to_markdown(self) -> str:
        if not self.detectada:
            return ""
        lines = [
            "\n### 📞 Auditoria de Interceptações Telefônicas & Telemática (Cadeia de Custódia)",
            "",
            f"- **Diálogos / Registros Identificados:** {self.total_dialogos_identificados}",
        ]
        if self.alvos_mencionados:
            lines.append(f"- **Alvos / Interlocutores Mapeados:** {', '.join(set(self.alvos_mencionados[:8]))}")
        if self.telefones_ou_imeis:
            lines.append(f"- **Terminais / IMEIs Identificados:** {', '.join(set(self.telefones_ou_imeis[:6]))}")
        
        # Alertas estratégicos de defesa
        lines.append("\n> [!IMPORTANT]")
        lines.append("> **Pontos Críticos de Defesa Criminal Mapeados:**")
        if self.alerta_confronto_vocalico:
            lines.append("> - **Confronto Vocálico Ausente:** Verifique se há perícia de identificação do falante (STJ HC 512.278/SP). Transcrições sem laudo fonético oficial ensejam nulidade probatória por fragilidade de autoria.")
        else:
            lines.append("> - **Perícia Fonética:** Confirmar nos autos se houve laudo pericial formal para atestar que os áudios pertencem indubitavelmente ao acusado.")
        
        if self.alerta_cadeia_custodia:
            lines.append("> - **Cadeia de Custódia (Art. 158-A/B CPP):** Áudios ou prints telemáticos exigem integridade de hash e espelhamento oficial sob pena de ilicitude probatória.")
        lines.append("")
        return "\n".join(lines)


@dataclasses.dataclass
class DoclingParseResult:
    source_path: str
    file_name: str
    file_sha256: str
    engine_used: str  # "ibm_docling" | "pymupdf_fallback"
    pages_count: int
    duration_seconds: float
    tables: List[ExtractedTable]
    markdown_content: str
    processos_cnj: List[str] = dataclasses.field(default_factory=list)
    dosimetria: DosimetriaAnalysis = dataclasses.field(default_factory=DosimetriaAnalysis)
    interceptacoes: InterceptacaoAudit = dataclasses.field(default_factory=InterceptacaoAudit)

    def save_markdown(self, output_path: str | Path) -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.markdown_content)
        return str(path.resolve())

    def save_tables_json(self, output_path: str | Path) -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "source_file": self.file_name,
            "engine": self.engine_used,
            "tables_count": len(self.tables),
            "tables": [t.to_dict() for t in self.tables],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return str(path.resolve())


# ---------------------------------------------------------------------------
# Analisador Especializado de Direito Penal (SuperJus Legal Enricher)
# ---------------------------------------------------------------------------
class SuperJusLegalEnricher:
    CNJ_REGEX = re.compile(r"\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b")
    
    # Padrões para dosimetria
    PENA_BASE_REGEX = re.compile(r"(?:pena[\s\-]base|primeira fase|1[ªa]\s*fase)[\s\:\-]+([^\.\n]+(?:\.|\n|$))", re.IGNORECASE)
    PENA_DEF_REGEX = re.compile(r"(?:torno[\s\-]+a\s+pena\s+definitiva|fixo\s+a\s+pena\s+definitiva|pena\s+definitiva\s+em|totalizando|condeno.*à\s+pena\s+de)[\s\:\-]+([^\.\n]+(?:\.|\n|$))", re.IGNORECASE)
    REGIME_REGEX = re.compile(r"regime\s+inicial\s+(?:de\s+cumprimento\s+)?(?:de\s+pena\s+)?(fechado|semiaberto|semi\-aberto|aberto)", re.IGNORECASE)
    SUBST_REGEX = re.compile(r"(substituo|substitui[\s\-]se|inviável\s+a\s+substituição|cabível\s+a\s+substituição|art(?:igo|\.)\s*44\s*do\s*cp)[\s\:\-]+([^\.\n]+(?:\.|\n|$))", re.IGNORECASE)

    # Padrões para interceptações telefônicas
    TEL_REGEX = re.compile(r"(?:\(?\d{2}\)?\s*)?(?:9\d{4}[\-\s]?\d{4}|\d{4}[\-\s]?\d{4})\b")
    IMEI_REGEX = re.compile(r"\b\d{15}\b")
    INTERLOC_REGEX = re.compile(r"(?:de|para|alvo|interlocutor|chamador|ligador|interlocutores)[\s\:\-]+([^\,\.\n\(\)\|\;]{3,35})", re.IGNORECASE)

    @classmethod
    def extract_processos_cnj(cls, text: str) -> List[str]:
        matches = cls.CNJ_REGEX.findall(text)
        return list(dict.fromkeys(matches))  # preserva ordem e remove duplicatas

    @classmethod
    def analyze_dosimetria(cls, text: str) -> DosimetriaAnalysis:
        analysis = DosimetriaAnalysis()
        lower_text = text.lower()

        keywords = ["art. 59", "art. 68", "pena-base", "circunstâncias judiciais", "atenuante", "agravante", "tráfico privilegiado", "regime inicial"]
        found_keywords = sum(1 for kw in keywords if kw in lower_text)

        if found_keywords >= 2:
            analysis.detectada = True

            # 1ª fase
            pb_match = cls.PENA_BASE_REGEX.search(text)
            if pb_match:
                analysis.pena_base = pb_match.group(1).strip()

            # Circunstâncias judiciais do art. 59
            circ_keys = ["culpabilidade", "antecedentes", "conduta social", "personalidade", "motivos", "circunstâncias", "consequências", "comportamento da vítima"]
            for ck in circ_keys:
                if re.search(rf"\b{ck}\b.*?(?:desfavor[aá]vel|negativ|prejudicial|neutr|favor[aá]vel)", lower_text):
                    analysis.circunstancias_judiciais.append(f"{ck.capitalize()} valorada")

            # 2ª fase
            if "confissão" in lower_text:
                analysis.atenuantes.append("Confissão Espontânea (Art. 65, III, 'd', CP)")
            if "menoridade" in lower_text or "21 anos" in lower_text:
                analysis.atenuantes.append("Menoridade Relativa (Art. 65, I, CP)")
            if "reincidência" in lower_text or "reincidente" in lower_text:
                analysis.agravantes.append("Reincidência (Art. 61, I, CP)")
            if "calamidade" in lower_text or "pandemia" in lower_text:
                analysis.agravantes.append("Calamidade Pública (Art. 61, II, 'j', CP)")

            # 3ª fase
            if "33, § 4" in lower_text or "privilegiado" in lower_text or "§ 4º" in lower_text:
                analysis.trafico_privilegiado = "Mencionado na decisão"
                if "afasto" in lower_text or "inaplicável" in lower_text or "dedicação" in lower_text:
                    analysis.trafico_privilegiado = "Inaplicado / Negado (verificar requisitos de primariedade e ausência de dedicação criminosa)"
                elif "aplico" in lower_text or "reduzo" in lower_text or "fração de" in lower_text:
                    analysis.trafico_privilegiado = "Aplicado com redução"

            # Majorantes
            if "art. 40" in lower_text:
                analysis.causas_aumento.append("Majorante da Lei de Drogas (Art. 40)")

            # Pena Definitiva
            pdef_match = cls.PENA_DEF_REGEX.search(text)
            if pdef_match:
                analysis.pena_definitiva = pdef_match.group(1).strip()

            # Regime
            reg_match = cls.REGIME_REGEX.search(text)
            if reg_match:
                analysis.regime_inicial = f"Regime {reg_match.group(1).capitalize()}"

            # Substituição
            sub_match = cls.SUBST_REGEX.search(text)
            if sub_match:
                analysis.substituicao_prd = sub_match.group(0).strip()[:150]

        return analysis

    @classmethod
    def analyze_interceptacoes(cls, text: str) -> InterceptacaoAudit:
        audit = InterceptacaoAudit()
        lower_text = text.lower()

        keywords = ["intercepta", "degrava", "áudio", "ligação", "interlocut", "chamada", "whatsapp", "conversa telefônica", "escuta"]
        found_count = sum(1 for kw in keywords if kw in lower_text)

        if found_count >= 2:
            audit.detectada = True
            
            # Alvos e interlocutores
            interloc_matches = cls.INTERLOC_REGEX.findall(text)
            clean_alvos = [m.strip() for m in interloc_matches if len(m.strip()) > 3 and not m.strip().isdigit()]
            audit.alvos_mencionados = clean_alvos[:15]

            # Telefones e IMEIs
            tels = cls.TEL_REGEX.findall(text)
            imeis = cls.IMEI_REGEX.findall(text)
            audit.telefones_ou_imeis = list(dict.fromkeys(tels + imeis))[:10]

            # Diálogos identificados
            dialogos_count = len(re.findall(r"(?:áudio|chamada|ligação|diálogo)\s*(?:n[ºo°]|\d+)", lower_text))
            audit.total_dialogos_identificados = max(dialogos_count, len(audit.alvos_mencionados))

            # Alertas defensivos
            if "confronto vocálico" not in lower_text and "perícia de voz" not in lower_text and "laudo pericial de voz" not in lower_text:
                audit.alerta_confronto_vocalico = True
            
            if "cadeia de custódia" not in lower_text or "hash" not in lower_text:
                audit.alerta_cadeia_custodia = True

        return audit


# ---------------------------------------------------------------------------
# Fallback PyMuPDF (Extração Nativa com Tabelas)
# ---------------------------------------------------------------------------
class PyMuPDFTableFallback:
    """Motor de fallback leve, rápido e com extração nativa de tabelas."""

    @staticmethod
    def is_pdf_digital(doc: Any) -> bool:
        """Verifica se o documento já possui camada de texto digital ou se é digitalizado."""
        total_chars = 0
        pages_to_check = min(len(doc), 5)
        for i in range(pages_to_check):
            total_chars += len(doc[i].get_text())
        avg_chars = total_chars / max(pages_to_check, 1)
        return avg_chars > 80

    @classmethod
    def convert(cls, pdf_path: str | Path) -> DoclingParseResult:
        if not PYMUPDF_AVAILABLE:
            raise RuntimeError("PyMuPDF (fitz) não está disponível para executar o fallback.")

        pdf_path = Path(pdf_path)
        t0 = time.time()

        with open(pdf_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        doc = fitz.open(str(pdf_path))
        pages_count = len(doc)
        tables_list: List[ExtractedTable] = []
        md_pages: List[str] = []
        full_text_accumulator: List[str] = []

        table_counter = 1

        for page_idx in range(pages_count):
            page = doc[page_idx]
            page_text = page.get_text("text")
            full_text_accumulator.append(page_text)

            # Buscar tabelas na página
            tabs = []
            if hasattr(page, "find_tables"):
                try:
                    table_finder = page.find_tables()
                    tabs = list(table_finder.tables)
                except Exception as e:
                    logger.debug(f"Erro ao buscar tabelas na página {page_idx+1}: {e}")

            page_md = [f"## Página {page_idx + 1}\n"]

            if tabs:
                # Extrair cada tabela detectada
                for t in tabs:
                    try:
                        extracted = t.extract()
                        if not extracted or len(extracted) < 1:
                            continue
                        
                        raw_headers = extracted[0]
                        headers = [str(h).strip().replace("\n", " ") if h is not None else f"Coluna_{c+1}" for c, h in enumerate(raw_headers)]
                        rows = []
                        for r in extracted[1:]:
                            clean_r = [str(val).strip().replace("\n", " ") if val is not None else "" for val in r]
                            rows.append(clean_r)

                        # Montar Markdown da tabela
                        tbl_md_lines = [
                            "| " + " | ".join(headers) + " |",
                            "| " + " | ".join([":---"] * len(headers)) + " |",
                        ]
                        for r in rows:
                            # Ajustar tamanho da linha se divergir das colunas
                            if len(r) < len(headers):
                                r.extend([""] * (len(headers) - len(r)))
                            tbl_md_lines.append("| " + " | ".join(r[:len(headers)]) + " |")
                        tbl_md = "\n".join(tbl_md_lines)

                        ext_table = ExtractedTable(
                            index=table_counter,
                            page=page_idx + 1,
                            rows_count=len(rows),
                            cols_count=len(headers),
                            headers=headers,
                            rows=rows,
                            markdown=tbl_md,
                        )
                        tables_list.append(ext_table)
                        table_counter += 1

                        page_md.append(f"\n{tbl_md}\n")
                    except Exception as err:
                        logger.warning(f"Erro ao formatar tabela na pág {page_idx+1}: {err}")
            
            # Adicionar texto limpo da página
            clean_text = re.sub(r"\n{3,}", "\n\n", page_text.strip())
            page_md.append(clean_text)
            md_pages.append("\n".join(page_md))

        doc.close()
        full_text = "\n\n".join(full_text_accumulator)

        # Análise de domínio penal
        cnjs = SuperJusLegalEnricher.extract_processos_cnj(full_text)
        dosimetria = SuperJusLegalEnricher.analyze_dosimetria(full_text)
        interceptacoes = SuperJusLegalEnricher.analyze_interceptacoes(full_text)

        # Montagem do cabeçalho de metadados
        banner = cls._build_metadata_banner(
            file_name=pdf_path.name,
            engine="PyMuPDF Native Table Fallback",
            pages=pages_count,
            tables=len(tables_list),
            cnjs=cnjs,
            duration=time.time() - t0,
        )

        final_md = (
            banner
            + dosimetria.to_markdown()
            + interceptacoes.to_markdown()
            + "\n\n---\n\n"
            + "\n\n---\n\n".join(md_pages)
        )

        return DoclingParseResult(
            source_path=str(pdf_path.resolve()),
            file_name=pdf_path.name,
            file_sha256=file_hash,
            engine_used="pymupdf_fallback",
            pages_count=pages_count,
            duration_seconds=time.time() - t0,
            tables=tables_list,
            markdown_content=final_md,
            processos_cnj=cnjs,
            dosimetria=dosimetria,
            interceptacoes=interceptacoes,
        )

    @staticmethod
    def _build_metadata_banner(file_name: str, engine: str, pages: int, tables: int, cnjs: List[str], duration: float) -> str:
        cnj_str = ", ".join(cnjs) if cnjs else "Não identificado expressamente"
        return f"""<!-- SUPERJUS METADATA HEADER -->
# Relatório de Extração Documental · SuperJus

| Metadado | Detalhe |
| :--- | :--- |
| **Arquivo Analisado** | `{file_name}` |
| **Motor de Conversão** | {engine} |
| **Processo(s) CNJ Identificado(s)** | `{cnj_str}` |
| **Total de Páginas** | {pages} |
| **Tabelas Estruturadas Extraídas** | {tables} |
| **Tempo de Processamento** | {duration:.2f}s |
| **Data do Processamento** | {time.strftime("%d/%m/%Y %H:%M:%S")} |

<!-- FIM DO CABEÇALHO -->
"""


# ---------------------------------------------------------------------------
# Motor Primário: IBM Docling 2.x
# ---------------------------------------------------------------------------
class SuperJusDoclingParser:
    """Conversor avançado de documentos jurídicos baseado no IBM Docling."""

    def __init__(
        self,
        ocr_mode: str = "auto",  # "auto" | "force" | "off"
        table_mode: str = "accurate",  # "accurate" | "fast"
        prefer_engine: str = "auto",  # "auto" | "docling" | "fallback"
    ):
        self.ocr_mode = ocr_mode.lower()
        self.table_mode = table_mode.lower()
        self.prefer_engine = prefer_engine.lower()
        self._converter: Optional[Any] = None

    def _get_converter(self, is_digital_pdf: bool = True) -> Any:
        if not DOCLING_AVAILABLE:
            raise RuntimeError("Docling não está instalado.")

        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_table_structure = True
        
        # Modo de reconhecimento de tabelas
        if self.table_mode == "fast":
            pipeline_options.table_structure_options.mode = TableFormerMode.FAST
        else:
            pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE

        # Decisão de OCR
        if self.ocr_mode == "force":
            pipeline_options.do_ocr = True
        elif self.ocr_mode == "off":
            pipeline_options.do_ocr = False
        else:  # "auto"
            # Se for um PDF já com camada de texto digital, desativa OCR para aceleração 15x
            if is_digital_pdf:
                pipeline_options.do_ocr = False
                logger.info("PDF digital detectado: OCR desativado para ganho de velocidade (TableFormer ativo).")
            else:
                pipeline_options.do_ocr = True
                logger.info("PDF digitalizado/sem texto: OCR RapidOCR ativado.")

        format_options = {
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
        return DocumentConverter(format_options=format_options)

    def convert(self, pdf_path: str | Path) -> DoclingParseResult:
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_path}")

        t0 = time.time()
        with open(pdf_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        # Decisão de fallback se solicitado explicitamente
        if self.prefer_engine == "fallback" or not DOCLING_AVAILABLE:
            if not DOCLING_AVAILABLE and self.prefer_engine != "fallback":
                logger.warning("IBM Docling não disponível. Acionando Fallback Inteligente PyMuPDF...")
            return PyMuPDFTableFallback.convert(pdf_path)

        # Checar se o PDF tem camada de texto nativa via PyMuPDF para otimizar OCR
        is_digital = True
        pages_count = 0
        if PYMUPDF_AVAILABLE:
            try:
                probe_doc = fitz.open(str(pdf_path))
                pages_count = len(probe_doc)
                is_digital = PyMuPDFTableFallback.is_pdf_digital(probe_doc)
                probe_doc.close()
            except Exception:
                pass

        try:
            logger.info(f"Iniciando conversão via IBM Docling de '{pdf_path.name}' (páginas={pages_count})...")
            converter = self._get_converter(is_digital_pdf=is_digital)
            conversion_result = converter.convert(str(pdf_path))
            doc = conversion_result.document

            # Extração de tabelas reconhecidas pelo Docling
            tables_list: List[ExtractedTable] = []
            for i, tbl in enumerate(doc.tables):
                try:
                    try:
                        df = tbl.export_to_dataframe(doc=doc)
                    except TypeError:
                        df = tbl.export_to_dataframe()
                    headers = [str(col) for col in df.columns]
                    rows = [[str(val) for val in row] for row in df.values]
                    tbl_md_lines = [
                        "| " + " | ".join(headers) + " |",
                        "| " + " | ".join([":---"] * len(headers)) + " |",
                    ]
                    for r in rows:
                        tbl_md_lines.append("| " + " | ".join(r) + " |")
                    tbl_md = "\n".join(tbl_md_lines)

                    tables_list.append(
                        ExtractedTable(
                            index=i + 1,
                            page=getattr(tbl, "page_no", 1) or 1,
                            rows_count=len(rows),
                            cols_count=len(headers),
                            headers=headers,
                            rows=rows,
                            markdown=tbl_md,
                            dataframe_dict=df.to_dict(orient="records"),
                        )
                    )
                except Exception as e:
                    logger.debug(f"Erro ao processar tabela {i+1} do Docling: {e}")

            # Exportar Markdown puro do Docling
            base_md = doc.export_to_markdown()

            # Análise criminal especializada SuperJus
            cnjs = SuperJusLegalEnricher.extract_processos_cnj(base_md)
            dosimetria = SuperJusLegalEnricher.analyze_dosimetria(base_md)
            interceptacoes = SuperJusLegalEnricher.analyze_interceptacoes(base_md)

            duration = time.time() - t0
            banner = PyMuPDFTableFallback._build_metadata_banner(
                file_name=pdf_path.name,
                engine="IBM Docling 2.x (Accurate TableFormer)",
                pages=pages_count or getattr(doc, "pages_count", 1) or 1,
                tables=len(tables_list),
                cnjs=cnjs,
                duration=duration,
            )

            final_md = (
                banner
                + dosimetria.to_markdown()
                + interceptacoes.to_markdown()
                + "\n\n---\n\n"
                + base_md
            )

            logger.info(f"Conversão concluída com sucesso via Docling em {duration:.2f}s ({len(tables_list)} tabelas).")

            return DoclingParseResult(
                source_path=str(pdf_path.resolve()),
                file_name=pdf_path.name,
                file_sha256=file_hash,
                engine_used="ibm_docling",
                pages_count=pages_count or 1,
                duration_seconds=duration,
                tables=tables_list,
                markdown_content=final_md,
                processos_cnj=cnjs,
                dosimetria=dosimetria,
                interceptacoes=interceptacoes,
            )

        except Exception as e:
            logger.error(f"Falha na conversão com IBM Docling ({e}). Acionando Fallback PyMuPDF...", exc_info=False)
            if PYMUPDF_AVAILABLE:
                return PyMuPDFTableFallback.convert(pdf_path)
            raise


# ---------------------------------------------------------------------------
# Função utilitária de conveniência
# ---------------------------------------------------------------------------
def parse_pdf(
    pdf_path: str | Path,
    output_md_path: Optional[str | Path] = None,
    export_tables_json: bool = False,
    ocr_mode: str = "auto",
    prefer_engine: str = "auto",
) -> DoclingParseResult:
    """Função de alto nível para chamada direta por outros scripts do SuperJus."""
    parser = SuperJusDoclingParser(ocr_mode=ocr_mode, prefer_engine=prefer_engine)
    result = parser.convert(pdf_path)
    
    if output_md_path:
        result.save_markdown(output_md_path)
    
    if export_tables_json:
        json_path = (
            Path(output_md_path).with_suffix(".tables.json")
            if output_md_path
            else Path(pdf_path).with_suffix(".tables.json")
        )
        result.save_tables_json(json_path)

    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="SuperJus Docling Parser - Conversor de PDFs Jurídicos para Markdown Estruturado"
    )
    parser.add_argument("input_pdf", nargs="?", help="Caminho do arquivo PDF para conversão")
    parser.add_argument("-o", "--output", help="Caminho do arquivo de saída .md")
    parser.add_argument("--batch-dir", help="Converte em lote todos os PDFs de um diretório de cliente")
    parser.add_argument("--ocr", choices=["auto", "force", "off"], default="auto", help="Modo de OCR (padrão: auto)")
    parser.add_argument("--engine", choices=["auto", "docling", "fallback"], default="auto", help="Preferência de motor")
    parser.add_argument("--table-mode", choices=["accurate", "fast"], default="accurate", help="Modo do TableFormer")
    parser.add_argument("--export-tables", action="store_true", help="Salva tabelas em formato JSON estruturado")
    parser.add_argument("--quiet", action="store_true", help="Suprime logs informativos")

    args = parser.parse_args()

    if args.quiet:
        logger.setLevel(logging.WARNING)

    if not args.input_pdf and not args.batch_dir:
        parser.print_help()
        sys.exit(1)

    doc_parser = SuperJusDoclingParser(
        ocr_mode=args.ocr,
        table_mode=args.table_mode,
        prefer_engine=args.engine,
    )

    if args.batch_dir:
        batch_path = Path(args.batch_dir)
        if not batch_path.is_dir():
            logger.error(f"Diretório não encontrado: {batch_path}")
            sys.exit(1)
        
        pdf_files = list(batch_path.rglob("*.pdf"))
        logger.info(f"Modo em lote: {len(pdf_files)} PDFs localizados em {batch_path}")
        
        success_count = 0
        for pdf_file in pdf_files:
            try:
                out_file = pdf_file.with_suffix(".docling.md")
                res = doc_parser.convert(pdf_file)
                res.save_markdown(out_file)
                if args.export_tables and res.tables:
                    res.save_tables_json(pdf_file.with_suffix(".tables.json"))
                logger.info(f"Concluído: {pdf_file.name} -> {out_file.name} ({len(res.tables)} tabelas)")
                success_count += 1
            except Exception as e:
                logger.error(f"Erro em {pdf_file.name}: {e}")
        
        logger.info(f"Lote finalizado: {success_count}/{len(pdf_files)} convertidos com sucesso.")
        return

    # Processamento individual
    input_path = Path(args.input_pdf)
    output_path = Path(args.output) if args.output else input_path.with_suffix(".docling.md")

    result = doc_parser.convert(input_path)
    saved_md = result.save_markdown(output_path)
    logger.info(f"Markdown estruturado gravado em: {saved_md}")

    if args.export_tables and result.tables:
        json_path = output_path.with_suffix(".tables.json")
        saved_json = result.save_tables_json(json_path)
        logger.info(f"Tabelas JSON gravadas em: {saved_json}")

    print("\n" + "=" * 60)
    print(f"📄 RESUMO DA CONVERSÃO · SUPERJUS DOCLING")
    print("=" * 60)
    print(f"Arquivo: {result.file_name}")
    print(f"Motor Utilizado: {result.engine_used}")
    print(f"Páginas: {result.pages_count}")
    print(f"Tabelas Estruturadas: {len(result.tables)}")
    print(f"Processos CNJ: {', '.join(result.processos_cnj) if result.processos_cnj else 'Nenhum'}")
    print(f"Dosimetria Detectada: {'Sim' if result.dosimetria.detectada else 'Não'}")
    print(f"Interceptações Mapeadas: {'Sim' if result.interceptacoes.detectada else 'Não'}")
    print(f"Tempo Total: {result.duration_seconds:.2f}s")
    print(f"Destino: {saved_md}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
