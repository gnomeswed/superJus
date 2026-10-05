import sys, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
# -*- coding: utf-8 -*-
import json
import urllib.request
import os

clean_num = '00014922520168190046'
process_formatted = '0001492-25.2016.8.19.0046'
url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}
req_data = json.dumps({
    "query": {
        "match": {
            "numeroProcesso": clean_num
        }
    },
    "size": 50
}).encode('utf-8')

target_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_3\documentos_processo"
analises_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_3\analises"
case_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_3"

os.makedirs(target_dir, exist_ok=True)
os.makedirs(analises_dir, exist_ok=True)

req = urllib.request.Request(url, data=req_data, headers=headers)

with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode('utf-8'))
    hits = res.get('hits', {}).get('hits', [])
    
    # Salvar JSON completo com todas as instâncias
    with open(os.path.join(target_dir, "datajud_all_instances.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
        
    timeline_events = []
    report_sections = []
    
    report_sections.append(f"# ANÁLISE JURÍDICA E HISTÓRICO COMPLETO DO PROCESSO")
    report_sections.append(f"**Cliente/Réu:** Júlio Pereira Marcos")
    report_sections.append(f"**Número do Processo:** `{process_formatted}`")
    report_sections.append(f"**Tribunal:** TJRJ - Tribunal de Justiça do Rio de Janeiro")
    report_sections.append(f"**Comarca de Origem:** Rio Bonito (Código 0046)")
    report_sections.append(f"**Registros Encontrados no Datajud:** {len(hits)} instância(s)\n")
    
    for idx, hit in enumerate(hits, start=1):
        src = hit['_source']
        grau = src.get('grau', f'G{idx}')
        classe = src.get('classe', {}).get('nome', 'Não Informada')
        orgao = src.get('orgaoJulgador', {}).get('nome', 'Não Informado')
        dt_ajui = src.get('dataAjuizamento', '')
        assuntos = [a.get('nome') for a in src.get('assuntos', []) if a.get('nome')]
        movs = src.get('movimentos', [])
        
        report_sections.append(f"## {idx}. Instância/Grau: {grau} - {classe}")
        report_sections.append(f"- **Órgão Julgador:** {orgao}")
        report_sections.append(f"- **Assunto(s):** {', '.join(assuntos) if assuntos else 'Não especificado'}")
        report_sections.append(f"- **Data Ajuizamento:** {dt_ajui}")
        report_sections.append(f"- **Total de Movimentações:** {len(movs)}\n")
        report_sections.append("### Cronologia de Movimentações:")
        
        for m in movs:
            dt_raw = m.get('dataHora', '')
            dt_formatted = dt_raw[:10] if len(dt_raw) >= 10 else dt_raw
            nome = m.get('nome', '')
            codigo = m.get('codigo', '')
            comps = m.get('complementosTabelados', [])
            comp_details = []
            for c in comps:
                c_nome = c.get('nome', '')
                c_desc = c.get('descricao', '')
                if c_desc:
                    comp_details.append(f"{c_nome}: {c_desc}")
            comp_str = f" ({'; '.join(comp_details)})" if comp_details else ""
            
            report_sections.append(f"- **`{dt_formatted}`** - **{nome}**{comp_str} *(Código CNJ: {codigo})*")
            
            timeline_events.append({
                "date": dt_formatted,
                "event": f"[{grau}] {nome}{comp_str}",
                "grau": grau,
                "orgao": orgao,
                "codigo": codigo
            })
            
        report_sections.append("\n" + "-"*60 + "\n")

    # Ordenar linha do tempo por data
    timeline_events_sorted = sorted(timeline_events, key=lambda x: x["date"])
    
    # Salvar timeline.json no diretório do Caso 3
    with open(os.path.join(case_dir, "timeline.json"), "w", encoding="utf-8") as f:
        json.dump(timeline_events_sorted, f, indent=2, ensure_ascii=False)
        
    # Salvar Relatório de Análise
    report_path = os.path.join(analises_dir, f"analise_processual_{clean_num}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_sections))
        
    print(f"Sucesso! Gerados {len(timeline_events_sorted)} eventos na linha do tempo.")
    print(f"Relatório salvo em: {report_path}")
