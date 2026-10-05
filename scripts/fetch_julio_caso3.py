# -*- coding: utf-8 -*-
import os
import sys
import json
import datetime
import urllib.request
import urllib.error

os.environ["DEMO_MODE"] = "False"
os.environ["INTEGRITY_MODE"] = "production"

process_number = "0001492-25.2016.8.19.0046"
clean_num = "00014922520168190046"

target_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_3\documentos_processo"
os.makedirs(target_dir, exist_ok=True)

print(f"=== Buscando processo {process_number} no Datajud CNJ / TJRJ ===")

url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}
req_data = json.dumps({"query": {"match": {"numeroProcesso": clean_num}}}).encode('utf-8')
req = urllib.request.Request(url, data=req_data, headers=headers)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        hits = res.get('hits', {}).get('hits', [])
        print(f"Hits retornados do Datajud: {len(hits)}")
        
        if hits:
            source = hits[0]['_source']
            
            # Salvar JSON completo do Datajud
            json_path = os.path.join(target_dir, "datajud_metadata.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(source, f, indent=2, ensure_ascii=False)
            print(f"Metadados salvos em: {json_path}")
            
            # Formatar Movimentações em Markdown
            movs = source.get('movimentos', [])
            orgao = source.get('orgaoJulgador', {}).get('nome', 'N/I')
            classe = source.get('classe', {}).get('nome', 'N/I')
            assuntos = [a.get('nome') for a in source.get('assuntos', []) if a.get('nome')]
            data_ajuizamento = source.get('dataAjuizamento', 'N/I')
            
            md_lines = []
            md_lines.append(f"# Processo TJRJ: {process_number}")
            md_lines.append(f"- **Órgão Julgador:** {orgao}")
            md_lines.append(f"- **Classe Processual:** {classe}")
            md_lines.append(f"- **Assuntos:** {', '.join(assuntos) if assuntos else 'Não informado'}")
            md_lines.append(f"- **Data de Ajuizamento:** {data_ajuizamento}")
            md_lines.append(f"- **Total de Movimentações Registradas:** {len(movs)}")
            md_lines.append("\n## Histórico Completo de Movimentações\n")
            
            # Ordenar movimentos por data se disponível
            for idx, m in enumerate(movs, start=1):
                dt = m.get('dataHora', '')
                nome_mov = m.get('nome', 'Movimentação sem título')
                code = m.get('codigo', '')
                complementos = m.get('complementosTabelados', [])
                comp_str = ""
                if complementos:
                    comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in complementos]) + ")"
                
                md_lines.append(f"### {idx}. {dt} - {nome_mov}{comp_str}")
                if code:
                    md_lines.append(f"- **Código CNJ:** {code}")
                md_lines.append("")
                
            md_path = os.path.join(target_dir, "movimentacoes_completas_datajud.md")
            with open(md_path, "w", encoding="utf-8") as f:
                f.write("\n".join(md_lines))
            print(f"Movimentações formatadas salvas em: {md_path}")
        else:
            print("Nenhum registro encontrado via consulta direta Datajud.")
            
except Exception as e:
    print(f"Erro na requisição ao Datajud: {e}")

# Tentar também o scraper Playwright / TJRJ se disponível
try:
    from tjrj_scraper_auto import scrape_process_documents
    print("\n=== Executando Scraper TJRJ (Playwright) ===")
    res_files = scrape_process_documents(process_number, target_dir)
    print(f"Scraper finalizado. Arquivos salvos: {res_files}")
except Exception as e:
    print(f"Aviso no scraper TJRJ: {e}")

print("=== Concluído ===")
