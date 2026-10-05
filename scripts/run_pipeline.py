import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.tjrj_scraper_auto import scrape_process_documents  # type: ignore
from scripts.process_and_timeline import generate_timeline_and_summary  # type: ignore

def main():
    ap = argparse.ArgumentParser(description="Pipeline TJRJ -> analise_timeline.json")
    ap.add_argument("process", nargs="?", default="0011857-95.2024.8.19.0002")
    ap.add_argument("--out", dest="out_dir", default=None)
    ap.add_argument("--json", action="store_true", default=True)
    ap.add_argument("--no-json", dest="no_json", action="store_true")
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()
    process = args.process
    save_dir = Path(args.out_dir) if args.out_dir else (ROOT / "Clientes" / f"Processo_{process}")
    want_json = not args.no_json
    if args.demo:
        os.environ["DEMO_MODE"] = "True"
    os.makedirs(save_dir, exist_ok=True)
    
    print(f"1. Baixando documentos do processo {process}...")
    try:
        paths = scrape_process_documents(process, str(save_dir))
    except Exception as e:
        print(f"[FALHA] scraping: {e}")
        sys.exit(2)
    print(f"Documentos salvos em: {save_dir}")
    print(f"Arquivos: {paths}")
    ext = ".json" if want_json else ".md"
    output_path = str(save_dir / f"analise_timeline{ext}")
    print(f"\n2. Analisando e gerando linha do tempo em {output_path}...")
    try:
        result = generate_timeline_and_summary(str(save_dir), output_path)
    except Exception as e:
        print(f"[FALHA] analise: {e}")
        sys.exit(3)
    
    print("\n================================================")
    print("RESUMO DOS FATOS:")
    print(result.get("summary", ""))
    print("\nJUIZ IDENTIFICADO:", result.get("judge", ""))
    print("\nLINHA DO TEMPO:")
    for t in result.get("timeline", []):
        print(f" - {t['date']}: {t['description']}")
    
    if result.get("contradictions"):
        print("\nCONTRADIÇÕES ENCONTRADAS:")
        for c in result.get("contradictions"):
            print(f" - {c['description']} (Entre {c.get('document_a')} e {c.get('document_b')})")
    
    print("================================================")
    print(f"\nRelatório completo salvo em: {output_path}")

if __name__ == "__main__":
    main()
