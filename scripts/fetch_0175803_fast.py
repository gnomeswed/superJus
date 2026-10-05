# -*- coding: utf-8 -*-
import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== CONSULTA RÁPIDA DATAJUD — PROCESSO 0175803-86.2023.8.19.0001 ===")

headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNxLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

proc_clean = "01758038620238190001"
url_tjrj = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'

req_data = json.dumps({"query": {"match": {"numeroProcesso": proc_clean}}, "size": 10}).encode('utf-8')
req = urllib.request.Request(url_tjrj, data=req_data, headers=headers)

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        hits = res.get('hits', {}).get('hits', [])
        print(f"\n📌 Datajud encontrou {len(hits)} registros no TJRJ:")
        for hit in hits:
            src = hit['_source']
            classe = src.get('classe', {}).get('nome', 'N/I')
            orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
            dt_at = src.get('dataHoraUltimaAtualizacao', 'N/I')
            movs = src.get('movimentos', [])
            pessoas = src.get('pessoas', [])
            
            print(f"\n• Processo: {src.get('numeroProcesso')}")
            print(f"  - Órgão: {orgao}")
            print(f"  - Classe: {classe}")
            print(f"  - Última Atualização: {dt_at}")
            
            print("  - Envolvidos (Partes):")
            for p in pessoas:
                nome = p.get('nome', 'N/I')
                tipo = p.get('tipoPessoa', 'N/I')
                polo = p.get('polo', 'N/I')
                print(f"    • [{polo}] {nome} ({tipo})")
                
            print(f"\n  - Total de movimentações: {len(movs)}")
            movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
            print("  - Últimas 15 movimentações:")
            for m in movs_sorted[:15]:
                dt = m.get('dataHora', '')[:19].replace('T', ' ')
                nome_mov = m.get('nome', '')
                code = m.get('codigo', '')
                comps = m.get('complementosTabelados', [])
                comp_str = ""
                if comps:
                    comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")"
                print(f"    • {dt} | {nome_mov}{comp_str} [Cód: {code}]")

except Exception as e:
    print(f"Erro ao consultar Datajud: {e}")

print("\n=== CONSULTA FINALIZADA ===")
