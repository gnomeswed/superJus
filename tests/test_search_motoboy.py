# Mantido como ferramenta manual — não coletado por pytest por padrão.
# Execute com: python scripts/search_docs_demo.py
import pathlib
import sys as _sys
_sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from scripts.search_docs import search_docs  # type: ignore
import json

ROOT = pathlib.Path(__file__).resolve().parents[1] / "Clientes" / "Lucas_Freitas" / "Caso_Principal" / "documentos_processo"
queries = ['processo', 'movimento', 'decisao', ' TJRJ', 'audiencia']
if __name__ == "__main__":
    if not ROOT.exists():
        print(f"[AVISO] {ROOT} ausente — nada a buscar.")
        raise SystemExit(0)
    results = {q: search_docs(str(ROOT), q, max_results=5) for q in queries}
    print(json.dumps(results, ensure_ascii=False, indent=2))
