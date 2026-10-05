# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

proc_num_clean = "00118579520248190002"
proc_fmt = "0011857-95.2024.8.19.0002"

url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}

lines = []
lines.append("=== CONSULTA EM TEMPO REAL DATAJUD — MOTOBOY LUCAS DE SOUZA FREITAS ===")

req_data = json.dumps({"query": {"match": {"numeroProcesso": proc_num_clean}}, "size": 10}).encode('utf-8')
req = urllib.request.Request(url, data=req_data, headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        hits = res.get('hits', {}).get('hits', [])
        lines.append(f"\n* Processo: {proc_fmt} — {len(hits)} registros no Datajud")
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
            for m in movs_sorted[:12]:
                dt = m.get('dataHora', '')
                nome = m.get('nome', '')
                code = m.get('codigo', '')
                comps = m.get('complementosTabelados', [])
                comp_str = ""
                if comps:
                    comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")"
                lines.append(f"      • {dt[:19].replace('T', ' ')} — {nome}{comp_str} (Cod. CNJ: {code})")
except Exception as e:
    lines.append(f"Erro ao consultar Datajud: {e}")

res_txt = "\n".join(lines)
target_path = r"c:\Projetos\superJus\lucas_online_result.txt"
with open(target_path, "w", encoding="utf-8") as f:
    f.write(res_txt)

print("SUCESSO: Resultado salvo em " + target_path)
