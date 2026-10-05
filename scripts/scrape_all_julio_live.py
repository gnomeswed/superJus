import sys, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
# -*- coding: utf-8 -*-
import json
import urllib.request
import os

processes = [
    ("0023013-51.2021.8.19.0078", "00230135120218190078", "Ação Penal (2ª Vara de Búzios)"),
    ("0029845-67.2026.8.19.0000", "00298456720268190000", "Habeas Corpus (TJRJ - 7ª Câmara)"),
    ("0022975-39.2021.8.19.0078", "00229753920218190078", "Processo Principal (Búzios)"),
    ("0001140-87.2024.8.19.0078", "00011408720248190078", "RESE do MP (TJRJ)")
]

url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}

target_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(target_dir, exist_ok=True)

out_md = []
out_md.append("# ATUALIZAÇÃO EM TEMPO REAL — ANDAMENTOS PROCESSUAIS DE JÚLIO PEREIRA MARCOS")
out_md.append(f"**Data da Consulta:** 24/07/2026\n")

for proc_fmt, proc_clean, desc in processes:
    out_md.append(f"## {desc} - Nº `{proc_fmt}`")
    req_data = json.dumps({
        "query": {"match": {"numeroProcesso": proc_clean}},
        "size": 50
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=req_data, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            hits = res.get('hits', {}).get('hits', [])
            
            if not hits:
                out_md.append("_Nenhum resultado retornado no Datajud._\n")
                continue
                
            for idx, hit in enumerate(hits, start=1):
                src = hit['_source']
                classe = src.get('classe', {}).get('nome', 'N/I')
                orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
                dt_at = src.get('dataHoraUltimaAtualizacao', 'N/I')
                movs = src.get('movimentos', [])
                
                out_md.append(f"### Registro {idx}: {classe} ({orgao})")
                out_md.append(f"- **Data/Hora Última Atualização no Sistema:** `{dt_at}`")
                out_md.append(f"- **Total de Movimentações Registradas:** {len(movs)}\n")
                out_md.append("#### Últimas 10 Movimentações (mais recentes primeiro):")
                
                movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
                for m in movs_sorted[:10]:
                    dt = m.get('dataHora', '')
                    nome = m.get('nome', '')
                    code = m.get('codigo', '')
                    comps = m.get('complementosTabelados', [])
                    comp_str = ""
                    if comps:
                        comp_str = " [" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + "]"
                    out_md.append(f"- **`{dt}`** | **{nome}**{comp_str} *(Cód. CNJ: {code})*")
                    
                out_md.append("\n" + "="*50 + "\n")
                
    except Exception as e:
        out_md.append(f"Erro na requisição Datajud para {proc_fmt}: {e}\n")

output_path = os.path.join(target_dir, "novos_andamentos_julho2026.md")
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(out_md))

print(f"Relatório gerado com sucesso em {output_path}")
