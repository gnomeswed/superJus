# -*- coding: utf-8 -*-
import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== CONSULTA EM TEMPO REAL — LEANDRO DA SILVA (LEANDRO MECÂNICO) ===")
print("Processo: 0827233-23.2026.8.19.0001 (1ª Vara Criminal da Regional de Santa Cruz)")

headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

proc_clean = "08272332320268190001"
url_tjrj = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'

req_data = json.dumps({"query": {"match": {"numeroProcesso": proc_clean}}, "size": 10}).encode('utf-8')
req = urllib.request.Request(url_tjrj, data=req_data, headers=headers)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        hits = res.get('hits', {}).get('hits', [])
        print(f"\n📌 Encontrados {len(hits)} registros no Datajud:")
        for hit in hits:
            src = hit['_source']
            classe = src.get('classe', {}).get('nome', 'N/I')
            orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
            dt_at = src.get('dataHoraUltimaAtualizacao', 'N/I')
            movs = src.get('movimentos', [])
            movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
            print(f"   • Órgão: {orgao} | Classe: {classe}")
            print(f"   • Última Atualização no Datajud: {dt_at}")
            print(f"   • Total de movimentações: {len(movs)}")
            print("   • Últimas movimentações no Datajud:")
            for m in movs_sorted[:20]:
                dt = m.get('dataHora', '')[:19].replace('T', ' ')
                nome = m.get('nome', '')
                code = m.get('codigo', '')
                comps = m.get('complementosTabelados', [])
                comp_str = ""
                if comps:
                    comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")"
                print(f"     - {dt} | {nome}{comp_str} [Cód: {code}]")
except Exception as e:
    print(f"Erro na consulta Datajud: {e}")

print("\n=== CONSULTA CONCLUÍDA ===")
