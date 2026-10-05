# -*- coding: utf-8 -*-
"""
SUPERJUS — CONSULTA DJEN / COMUNICA PJE AO VIVO (JÚLIO PEREIRA MARCOS)
Varre publicações recentes no Diário da Justiça Eletrônico Nacional (STJ e TJRJ).
"""

import sys, json, ssl, urllib.request
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

print("=" * 80)
print(f"🔍 CONSULTA AO VIVO DJEN / COMUNICA PJE — JÚLIO PEREIRA MARCOS")
print(f"⏰ Horário: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
print("=" * 80)

# Consulta pública da API Comunica PJe do CNJ
url_comunica = "https://comunicaapi.pje.jus.br/api/v1/comunicacao"
params = "?nomeParte=Julio+Pereira+Marcos&itensPorPagina=10"

req = urllib.request.Request(url_comunica + params, headers={"User-Agent": "Mozilla/5.0"})
ctx = ssl._create_unverified_context()

try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        items = data.get("items", [])
        print(f"Total de publicações encontradas no DJEN: {len(items)}")
        for it in items:
            dt = it.get("data_disponibilizacao", "")
            trib = it.get("siglaTribunal", "")
            proc = it.get("numero_processo", "")
            texto = it.get("texto", "")[:200]
            print(f"\n📢 [{dt}] Tribunal: {trib} | Processo: {proc}")
            print(f"   Conteúdo: {texto}...")
except Exception as e:
    print(f"Erro ao consultar DJEN: {e}")

# Consulta por número de processo da Ação Penal
proc_num = "00230135120218190078"
params_proc = f"?numeroProcesso={proc_num}&itensPorPagina=10"
req2 = urllib.request.Request(url_comunica + params_proc, headers={"User-Agent": "Mozilla/5.0"})

try:
    with urllib.request.urlopen(req2, context=ctx, timeout=15) as resp:
        data2 = json.loads(resp.read().decode("utf-8"))
        items2 = data2.get("items", [])
        print(f"\nTotal de publicações pelo número da Ação Penal de Búzios: {len(items2)}")
        for it in items2:
            dt = it.get("data_disponibilizacao", "")
            trib = it.get("siglaTribunal", "")
            proc = it.get("numero_processo", "")
            texto = it.get("texto", "")[:200]
            print(f"📢 [{dt}] Tribunal: {trib} | Processo: {proc}")
            print(f"   Conteúdo: {texto}...")
except Exception as e:
    print(f"Erro ao consultar por número: {e}")

print("\n" + "=" * 80)
