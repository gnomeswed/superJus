import sys
import json
import os

# Forçar scraping real desligando o demo mode
os.environ["DEMO_MODE"] = "False"
os.environ["INTEGRITY_MODE"] = "production"

from tjrj_scraper_auto import scrape_process_documents
from process_and_timeline import generate_timeline_and_summary

def main():
    if len(sys.argv) > 1:
        process = sys.argv[1]
    else:
        process = "0011857-95.2024.8.19.0002"
        
    save_dir = rf"C:\Projetos\Super Analista Jurídico\Clientes\Processo_{process}"
    os.makedirs(save_dir, exist_ok=True)
    
    print(f"1. Baixando documentos do processo {process}...")
    paths = scrape_process_documents(process, save_dir)
    print(f"Documentos salvos em: {save_dir}")
    print(f"Arquivos: {paths}")
    
    output_path = rf"{save_dir}\analise_timeline.json"
    print(f"\n2. Analisando e gerando linha do tempo...")
    result = generate_timeline_and_summary(save_dir, output_path)
    
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
