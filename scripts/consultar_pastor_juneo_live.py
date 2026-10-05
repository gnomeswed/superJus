# -*- coding: utf-8 -*-
"""
SUPERJUS — CONSULTA EM TEMPO REAL: PASTOR JUNEO (JUNEO LUCIANO DE OLIVEIRA)
Processo: 0810659-95.2026.8.19.0203 (2ª Vara Criminal da Regional de Jacarepaguá / TJRJ)
Nome: Juneo Luciano de Oliveira
"""

import sys, os, json, ssl, urllib.request
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {'Authorization': f"APIKey {API_KEY}", 'Content-Type': 'application/json'}

proc_clean = "08106599520268190203"
proc_fmt = "0810659-95.2026.8.19.0203"
nome = "Juneo Luciano de Oliveira"

print("=" * 85)
print(f"🔍 CONSULTA EM TEMPO REAL — PASTOR JUNEO ({nome.upper()})")
print(f"⚖️ Processo: {proc_fmt} | 2ª Vara Criminal de Jacarepaguá")
print(f"⏰ Consulta: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
print("=" * 85)

ctx = ssl._create_unverified_context()

# 1. Consulta DataJud TJRJ pelo número do processo
url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
payload = json.dumps({"query": {"match": {"numeroProcesso": proc_clean}}, "size": 5}).encode("utf-8")
req = urllib.request.Request(url, data=payload, headers=HEADERS)

try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        hits = data.get("hits", {}).get("hits", [])
        print(f"\n[1] Registros encontrados no DataJud TJRJ pelo número: {len(hits)}")
        for hit in hits:
            src = hit["_source"]
            orgao = src.get("orgaoJulgador", {}).get("nome", "N/I")
            classe = src.get("classe", {}).get("nome", "N/I")
            dt_at = src.get("dataHoraUltimaAtualizacao", "N/I")
            dt_aj = src.get("dataAjuizamento", "N/I")
            movs = src.get("movimentos", [])
            movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
            
            print(f"   🏛️ Órgão: {orgao} | Classe: {classe}")
            print(f"   📅 Ajuizado: {dt_aj} | Última Atualização: {dt_at}")
            print(f"   📑 Total de Movimentos: {len(movs)}")
            print("   📌 Últimas Movimentações:")
            for m in movs_sorted[:12]:
                dt = m.get("dataHora", "")[:19].replace("T", " ")
                nm = m.get("nome", "")
                comps = m.get("complementosTabelados", [])
                comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")" if comps else ""
                print(f"      • {dt} — {nm}{comp_str}")
                
            out_file = Path(r"c:\Projetos\superJus\Clientes\Pastor_Juneo\datajud_live_04_09_2026.json")
            with open(out_file, "w", encoding="utf-8") as fp:
                json.dump(src, fp, indent=2, ensure_ascii=False)
except Exception as e:
    print(f"Erro DataJud: {e}")

# 2. Busca por Nome no TJRJ e STJ (procurando HCs)
print("\n[2] Verificando se há Habeas Corpus no TJRJ ou STJ...")
for ep_label, ep_name in [("TJRJ (2ª Instância)", "api_publica_tjrj"), ("STJ (3ª Instância)", "api_publica_stj")]:
    url_ep = f"https://api-publica.datajud.cnj.jus.br/{ep_name}/_search"
    payload_nome = json.dumps({
        "query": {
            "bool": {
                "must": [
                    {"match_phrase": {"dadosBasicos.polo.parte.pessoa.nome": nome}}
                ]
            }
        },
        "size": 5
    }).encode("utf-8")
    req_ep = urllib.request.Request(url_ep, data=payload_nome, headers=HEADERS)
    try:
        with urllib.request.urlopen(req_ep, context=ctx, timeout=15) as resp:
            d = json.loads(resp.read().decode("utf-8"))
            hits_ep = d.get("hits", {}).get("hits", [])
            print(f"   • {ep_label}: {len(hits_ep)} hit(s)")
            for h in hits_ep:
                s = h["_source"]
                print(f"     -> Proc: {s.get('numeroProcesso')} | Classe: {s.get('classe',{}).get('nome')} | Órgão: {s.get('orgaoJulgador',{}).get('nome')} | Atualização: {s.get('dataHoraUltimaAtualizacao')}")
    except Exception as e:
        print(f"   • {ep_label}: Erro ({e})")

print("\n" + "=" * 85)
print("✅ Varredura concluída.")
print("=" * 85)
