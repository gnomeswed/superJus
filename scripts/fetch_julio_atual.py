import sys, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
# -*- coding: utf-8 -*-
import json
import urllib.request
import os

processes = [
    ("0023013-51.2021.8.19.0078", "00230135120218190078", "Ação Penal (2ª Vara de Búzios)"),
    ("0029845-67.2026.8.19.0000", "00298456720268190000", "Habeas Corpus (TJRJ - 7ª Câmara Criminal)"),
    ("0029845-67.2026.8.19.0002", "00298456720268190002", "Processo Relacionado TJRJ")
]

url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}

target_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(target_dir, exist_ok=True)

out_md = []
out_md.append("# MOVIMENTAÇÕES PROCESSUAIS ATUALIZADAS — JÚLIO PEREIRA MARCOS")
out_md.append(f"**Data da Consulta:** 24/07/2026\n")

for proc_fmt, proc_clean, desc in processes:
    out_md.append(f"## {desc} - Nº `{proc_fmt}`")
    req_data = json.dumps({"query": {"match": {"numeroProcesso": proc_clean}}, "size": 50}).encode('utf-8')
    req = urllib.request.Request(url, data=req_data, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            hits = res.get('hits', {}).get('hits', [])
            out_md.append(f"**Registros no Datajud:** {len(hits)}\n")
            
            if not hits:
                out_md.append("_Nenhum registro retornado pelo Datajud para este número especificamente._\n")
                continue
                
            for idx, hit in enumerate(hits, start=1):
                src = hit['_source']
                classe = src.get('classe', {}).get('nome', 'N/I')
                orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
                dt_at = src.get('dataHoraUltimaAtualizacao', 'N/I')
                movs = src.get('movimentos', [])
                
                out_md.append(f"### Instância {idx}: {classe}")
                out_md.append(f"- **Órgão Julgador:** {orgao}")
                out_md.append(f"- **Última Atualização:** {dt_at}")
                out_md.append(f"- **Total de Movimentos:** {len(movs)}\n")
                out_md.append("#### Últimas Movimentações (em ordem cronológica recente):")
                
                # Ordenar movimentos por data desc
                movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
                for m in movs_sorted[:15]:
                    dt = m.get('dataHora', '')
                    nome = m.get('nome', '')
                    comps = m.get('complementosTabelados', [])
                    comp_str = ""
                    if comps:
                        comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")"
                    out_md.append(f"- **[{dt[:19].replace('T', ' ')}]** — **{nome}**{comp_str}")
                    
                out_md.append("\n" + "-"*40 + "\n")
                
    except Exception as e:
        out_md.append(f"Erro ao consultar Datajud: {e}\n")

output_path = os.path.join(target_dir, "movimentacoes_atualizadas.md")
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(out_md))

print(f"Sucesso! Salvo em {output_path}")
