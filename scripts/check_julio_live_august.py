# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

procs = [
    ("0023013-51.2021.8.19.0078", "00230135120218190078", "Acao Penal - 2a Vara Buzios"),
    ("0029845-67.2026.8.19.0000", "00298456720268190000", "Habeas Corpus - 7a Cam. Criminal TJRJ"),
    ("0022975-39.2021.8.19.0078", "00229753920218190078", "Processo Principal - Buzios"),
    ("0001140-87.2024.8.19.0078", "00011408720248190078", "Execucao / Medida - Buzios"),
    ("0001492-25.2016.8.19.0046", "00014922520168190046", "Processo Antigo - Rio Bonito")
]

url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}

lines = []
lines.append("=== CONSULTA TJRJ / DATAJUD EM TEMPO REAL — JULIO PEREIRA MARCOS ===")
lines.append("Data da Consulta: 01/08/2026 17:24")

for formatted, clean, label in procs:
    req_data = json.dumps({"query": {"match": {"numeroProcesso": clean}}, "size": 10}).encode('utf-8')
    req = urllib.request.Request(url, data=req_data, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            hits = res.get('hits', {}).get('hits', [])
            lines.append(f"\n* Processo: {formatted} ({label}) — {len(hits)} registros no Datajud")
            for hit in hits:
                src = hit['_source']
                classe = src.get('classe', {}).get('nome', 'N/I')
                orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
                dt_at = src.get('dataHoraUltimaAtualizacao', 'N/I')
                movs = src.get('movimentos', [])
                movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
                lines.append(f"   - Orgao: {orgao} | Classe: {classe}")
                lines.append(f"   - Ultima Atualizacao no Sistema: {dt_at}")
                lines.append(f"   - Total de movimentos: {len(movs)}")
                lines.append("   - Ultimas movimentacoes:")
                for m in movs_sorted[:10]:
                    dt = m.get('dataHora', '')
                    nome = m.get('nome', '')
                    code = m.get('codigo', '')
                    comps = m.get('complementosTabelados', [])
                    comp_str = ""
                    if comps:
                        comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")"
                    lines.append(f"      • {dt[:19].replace('T', ' ')} — {nome}{comp_str} (Cod: {code})")
    except Exception as e:
        lines.append(f"Erro em {formatted}: {e}")

res_txt = "\n".join(lines)
target_path = r"c:\Projetos\superJus\julio_august1_check.txt"
with open(target_path, "w", encoding="utf-8") as f:
    f.write(res_txt)

print("SUCESSO: Consulta finalizada e salva em " + target_path)
