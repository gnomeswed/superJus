# -*- coding: utf-8 -*-
import json
import urllib.request
import time
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

proc_num_clean = "00118579520248190002"
proc_fmt = "0011857-95.2024.8.19.0002"
nome_cliente = "Lucas de Souza Freitas"

headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}

output_lines = []
output_lines.append(f"==========================================================================")
output_lines.append(f"=== CONSULTA EM TEMPO REAL EM TODAS AS INSTÂNCIAS — LUCAS DE SOUZA FREITAS ===")
output_lines.append(f"=== Data/Hora Local: {time.strftime('%Y-%m-%d %H:%M:%S')} ===")
output_lines.append(f"==========================================================================\n")

def query_datajud(endpoint, payload, max_retries=3):
    url = f"https://api-publica.datajud.cnj.jus.br/{endpoint}/_search"
    req_data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=req_data, headers=headers)
    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            if attempt == max_retries:
                return {"error": str(e)}
            time.sleep(2)

# --- 1. CONSULTA DATAJUD TJRJ — PROCESSO PRINCIPAL (1ª INSTÂNCIA & RECURSOS LINKADOS) ---
output_lines.append("📌 1. PRIMEIRA INSTÂNCIA & 2ª INSTÂNCIA LINKADA (TJRJ — Processo 0011857-95.2024.8.19.0002)")
res_tjrj = query_datajud("api_publica_tjrj", {"query": {"match": {"numeroProcesso": proc_num_clean}}, "size": 10})

if "error" in res_tjrj:
    output_lines.append(f"   ⚠️ Erro na consulta DataJud TJRJ (Número): {res_tjrj['error']}")
else:
    hits = res_tjrj.get('hits', {}).get('hits', [])
    output_lines.append(f"   • Total de registros encontrados no TJRJ por número de processo: {len(hits)}")
    for hit in hits:
        src = hit['_source']
        classe = src.get('classe', {}).get('nome', 'N/I')
        orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
        dt_at = src.get('dataHoraUltimaAtualizacao', 'N/I')
        movs = src.get('movimentos', [])
        movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
        
        output_lines.append(f"   • Órgão Julgador: {orgao} | Classe: {classe}")
        output_lines.append(f"   • Última Atualização no Sistema CNJ: {dt_at}")
        output_lines.append(f"   • Total de Movimentações Registradas: {len(movs)}")
        output_lines.append("   • Últimas 10 Movimentações em Ordem Cronológica:")
        for m in movs_sorted[:10]:
            dt = m.get('dataHora', '')
            nome = m.get('nome', '')
            code = m.get('codigo', '')
            comps = m.get('complementosTabelados', [])
            comp_str = ""
            if comps:
                comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")"
            output_lines.append(f"      - {dt[:19].replace('T', ' ')} | {nome}{comp_str} (Cód. CNJ: {code})")
output_lines.append("")

# --- 2. CONSULTA DATAJUD TJRJ — BUSCA POR NOME (2ª INSTÂNCIA / SEGUNDO GRAU / RECURSOS DA APELAÇÃO) ---
output_lines.append("📌 2. SEGUNDA INSTÂNCIA TJRJ (Busca Ampla por Nome 'Lucas de Souza Freitas')")
res_nome_tjrj = query_datajud("api_publica_tjrj", {"query": {"match_phrase": {"partes.nome": nome_cliente}}, "size": 10})

if "error" in res_nome_tjrj:
    output_lines.append(f"   ⚠️ Erro na consulta DataJud TJRJ (Nome): {res_nome_tjrj['error']}")
else:
    hits = res_nome_tjrj.get('hits', {}).get('hits', [])
    output_lines.append(f"   • Total de processos vinculados ao nome no TJRJ: {len(hits)}")
    for hit in hits:
        src = hit['_source']
        num = src.get('numeroProcesso', 'N/I')
        classe = src.get('classe', {}).get('nome', 'N/I')
        orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
        dt_at = src.get('dataHoraUltimaAtualizacao', 'N/I')
        output_lines.append(f"   - Processo: {num} | Órgão: {orgao} | Classe: {classe} | Última Modif: {dt_at}")
output_lines.append("")

# --- 3. CONSULTA STJ (SUPERIOR TRIBUNAL DE JUSTIÇA — 3ª INSTÂNCIA) ---
output_lines.append("📌 3. TERCEIRA INSTÂNCIA (STJ — Superior Tribunal de Justiça)")
res_stj = query_datajud("api_publica_stj", {"query": {"match_phrase": {"partes.nome": nome_cliente}}, "size": 10})

if "error" in res_stj:
    output_lines.append(f"   ⚠️ Erro na consulta DataJud STJ: {res_stj['error']}")
else:
    hits = res_stj.get('hits', {}).get('hits', [])
    output_lines.append(f"   • Total de processos encontrados no STJ em nome de Lucas de Souza Freitas: {len(hits)}")
    for hit in hits:
        src = hit['_source']
        num = src.get('numeroProcesso', 'N/I')
        classe = src.get('classe', {}).get('nome', 'N/I')
        orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
        dt_at = src.get('dataHoraUltimaAtualizacao', 'N/I')
        output_lines.append(f"   - Processo STJ: {num} | Órgão: {orgao} | Classe: {classe} | Última Modif: {dt_at}")
output_lines.append("")

# --- 4. CONSULTA STF (SUPREMO TRIBUNAL FEDERAL — INSTÂNCIA EXTRAORDINÁRIA) ---
output_lines.append("📌 4. INSTÂNCIA EXTRAORDINÁRIA (STF — Supremo Tribunal Federal)")
res_stf = query_datajud("api_publica_stf", {"query": {"match_phrase": {"partes.nome": nome_cliente}}, "size": 10})

if "error" in res_stf:
    output_lines.append(f"   ⚠️ Erro na consulta DataJud STF: {res_stf['error']}")
else:
    hits = res_stf.get('hits', {}).get('hits', [])
    output_lines.append(f"   • Total de processos encontrados no STF em nome de Lucas de Souza Freitas: {len(hits)}")
    for hit in hits:
        src = hit['_source']
        num = src.get('numeroProcesso', 'N/I')
        classe = src.get('classe', {}).get('nome', 'N/I')
        output_lines.append(f"   - Processo STF: {num} | Classe: {classe}")
output_lines.append("")

# --- 5. CONSULTA PROCESSO ANTERIOR (2017) ---
output_lines.append("📌 5. PROCESSO ANTERIOR (0000253-78.2017.8.19.0004 & HC 0046418-98.2017.8.19.0000)")
res_old = query_datajud("api_publica_tjrj", {"query": {"match": {"numeroProcesso": "00002537820178190004"}}, "size": 5})
if "error" in res_old:
    output_lines.append(f"   ⚠️ Erro na consulta do Processo de 2017: {res_old['error']}")
else:
    hits = res_old.get('hits', {}).get('hits', [])
    output_lines.append(f"   • Total de registros DataJud para o processo de 2017: {len(hits)} (Processo Arquivado Definitivamente em 08/11/2017 - Maço 1310262)")

output_lines.append("\n==========================================================================")
output_lines.append("=== FIM DO RELATÓRIO DE CONSULTA EM TEMPO REAL ===")
output_lines.append("==========================================================================")

report_content = "\n".join(output_lines)
print(report_content)

out_file = r"c:\Projetos\superJus\lucas_todas_instancias_result.txt"
with open(out_file, "w", encoding="utf-8") as f:
    f.write(report_content)

