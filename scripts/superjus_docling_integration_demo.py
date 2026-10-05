# -*- coding: utf-8 -*-
"""
SuperJus Docling Integration Demo & Analyst Helper
==================================================
Demonstra a integração prática do IBM Docling nos fluxos de trabalho dos
analistas jurídicos e agentes autônomos do SuperJus (Hermes, Antigravity, OpenCode).

Fluxo Demonstrado:
1. Ingestão de PDF Jurídico Complexo (Decisão / Acórdão / Parecer / Despacho / Espelho).
2. Extração Estruturada via Docling (tabelas perfeitas, hierarquia e metadados).
3. Extração Especializada Criminal (Dosimetria Art. 59/68 CP e Interceptações).
4. Integração com Base de Memória Persistente Compartilhada (memU).
5. Geração de Briefing Executivo para a Banca de Advocacia.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

# Garantir UTF-8
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Importar o parser mestre
from superjus_docling_parser import SuperJusDoclingParser, parse_pdf


def sync_to_memu(
    doc_name: str,
    summary_content: str,
    track: str = "Julio_Pereira_Marcos_Caso_Principal",
    description: str = "Extração estruturada de PDF via IBM Docling",
) -> bool:
    """Registra o conhecimento estruturado na memória compartilhada memU."""
    memu_store_script = Path(__file__).parent / "memu_store.py"
    if not memu_store_script.exists():
        print(f"[-] Script memu_store.py não localizado em {memu_store_script}")
        return False

    cmd = [
        sys.executable,
        str(memu_store_script),
        "--name",
        f"docling_{Path(doc_name).stem}.md",
        "--track",
        track,
        "--description",
        description,
        "--content",
        summary_content,
    ]
    try:
        print(f"[*] Sincronizando com memU ({track})...")
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if res.returncode == 0:
            print("[+] Memória persistida no memU com sucesso!")
            return True
        else:
            print(f"[-] Aviso ao gravar no memU: {res.stderr or res.stdout}")
            return False
    except Exception as e:
        print(f"[-] Falha na execução do memu_store: {e}")
        return False


def run_analyst_pipeline(
    pdf_path: Path,
    sync_memu: bool = False,
    engine: str = "auto",
    track: str = "Julio_Pereira_Marcos_Caso_Principal",
) -> None:
    print("\n" + "=" * 75)
    print("⚖️  SUPERJUS · FLUXO INTEGRADO DO ANALISTA JURÍDICO COM IBM DOCLING")
    print("=" * 75)
    print(f"Documento de Entrada : {pdf_path.resolve()}")
    print(f"Motor Selecionado    : {engine}")
    print(f"Persistência memU    : {'Ativa' if sync_memu else 'Inativa (use --sync-memu para ativar)'}")
    print("-" * 75)

    t0 = time.time()
    parser = SuperJusDoclingParser(ocr_mode="auto", prefer_engine=engine)
    result = parser.convert(pdf_path)

    # 1. Salvar Markdown na mesma pasta
    output_md = pdf_path.with_suffix(".analise_docling.md")
    result.save_markdown(output_md)

    # 2. Salvar Tabelas JSON se houver tabelas
    output_json = None
    if result.tables:
        output_json = pdf_path.with_suffix(".tabelas_docling.json")
        result.save_tables_json(output_json)

    # 3. Exibir Diagnóstico Estratégico
    print("\n📊 [DIAGNÓSTICO TÉCNICO DA EXTRAÇÃO]")
    print(f"• Motor Utilizado       : {result.engine_used}")
    print(f"• Duração               : {result.duration_seconds:.2f}s")
    print(f"• Total de Páginas      : {result.pages_count}")
    print(f"• Tabelas Estruturadas  : {len(result.tables)}")
    print(f"• Processos Identificados: {', '.join(result.processos_cnj) if result.processos_cnj else 'Nenhum'}")
    print(f"• Arquivo Markdown      : {output_md.name}")
    if output_json:
        print(f"• Arquivo Tabelas JSON  : {output_json.name}")

    # 4. Detalhamento de Tabelas Extraídas
    if result.tables:
        print("\n📑 [AMOSTRAGEM DAS TABELAS RECONHECIDAS PELO DOCLING]")
        for tbl in result.tables[:3]:
            print(f"\n  ▶ Tabela #{tbl.index} (Pág. {tbl.page} | {tbl.rows_count} linhas x {tbl.cols_count} colunas):")
            print(f"    Colunas: {', '.join(tbl.headers[:4])}{'...' if len(tbl.headers) > 4 else ''}")
            if tbl.rows:
                first_row = [c[:30] + '...' if len(c) > 30 else c for c in tbl.rows[0][:4]]
                print(f"    Amostra L1: {' | '.join(first_row)}")

    # 5. Detecção Criminal Especializada
    if result.dosimetria.detectada:
        print("\n⚖️ [DETECÇÃO CRIMINAL: DOSIMETRIA DA PENA]")
        if result.dosimetria.pena_base:
            print(f"  • 1ª Fase (Pena-Base) : {result.dosimetria.pena_base}")
        if result.dosimetria.atenuantes or result.dosimetria.agravantes:
            print(f"  • 2ª Fase             : Atenuantes={result.dosimetria.atenuantes} | Agravantes={result.dosimetria.agravantes}")
        if result.dosimetria.pena_definitiva:
            print(f"  • Pena Definitiva     : {result.dosimetria.pena_definitiva}")
        if result.dosimetria.regime_inicial:
            print(f"  • Regime Prisional    : {result.dosimetria.regime_inicial}")

    if result.interceptacoes.detectada:
        print("\n📞 [AUDITORIA CRIMINAL: INTERCEPTAÇÕES & PROVA TELEMÁTICA]")
        print(f"  • Diálogos / Registros: {result.interceptacoes.total_dialogos_identificados}")
        print(f"  • Alvos Mapeados      : {', '.join(result.interceptacoes.alvos_mencionados[:5])}")
        print(f"  • Alerta de Perícia   : {'⚠️ Ausência de Confronto Vocálico' if result.interceptacoes.alerta_confronto_vocalico else 'OK'}")

    # 6. Sincronização memU se solicitado
    if sync_memu:
        briefing = f"""# Extração Estruturada de Documento via IBM Docling
- **Documento:** {result.file_name}
- **Data da Análise:** {time.strftime("%d/%m/%Y %H:%M:%S")}
- **Motor:** {result.engine_used}
- **Processos CNJ:** {', '.join(result.processos_cnj)}
- **Tabelas Extraídas:** {len(result.tables)}
- **Caminho Markdown:** {output_md.resolve()}

## Resumo das Tabelas e Conteúdo
{result.markdown_content[:2000]}
... (conteúdo completo em {output_md.name})
"""
        sync_to_memu(
            doc_name=result.file_name,
            summary_content=briefing,
            track=track,
            description=f"Extração Docling de {result.file_name} com {len(result.tables)} tabelas",
        )

    print("\n" + "=" * 75)
    print("✅  FLUXO DE INTEGRAÇÃO DO ANALISTA CONCLUÍDO COM SUCESSO!")
    print("=" * 75 + "\n")


def main():
    default_pdf = (
        Path(__file__).parent.parent
        / "Clientes"
        / "Júlio_Pereira_Marcos"
        / "04_RECURSOS_SUPERIORES_STJ"
        / "03_Peticoes_e_Pareceres"
        / "Relatorio_Comparativo_Parecer_MPF_vs_Defesa_STJ.pdf"
    )

    parser = argparse.ArgumentParser(description="SuperJus Docling Integration Demo")
    parser.add_argument("pdf_path", nargs="?", default=str(default_pdf), help="Caminho do PDF para teste")
    parser.add_argument("--sync-memu", action="store_true", help="Persiste o resumo estruturado na base memU")
    parser.add_argument("--track", default="Julio_Pereira_Marcos_Caso_Principal", help="Trilha do memU")
    parser.add_argument("--engine", choices=["auto", "docling", "fallback"], default="auto", help="Motor a executar")

    args = parser.parse_args()

    pdf_file = Path(args.pdf_path)
    if not pdf_file.exists():
        print(f"[-] Erro: Arquivo {pdf_file} não encontrado.")
        sys.exit(1)

    run_analyst_pipeline(
        pdf_path=pdf_file,
        sync_memu=args.sync_memu,
        engine=args.engine,
        track=args.track,
    )


if __name__ == "__main__":
    main()
