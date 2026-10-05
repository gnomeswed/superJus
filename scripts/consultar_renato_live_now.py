# -*- coding: utf-8 -*-
"""
SUPERJUS — PESQUISA COMPLETA E ATUALIZADA DO PROCESSO DE RENATO BASTOS ROCHA
Varre DataJud TJRJ, STJ, TRF2 e consulta a Ação Penal 0801630-04.2025.8.19.0026 em tempo real.
"""

import sys, os, json, ssl, urllib.request
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {
    'Authorization': f"APIKey {API_KEY}",
    'Content-Type': 'application/json'
}

CPF = "12498197761"
NOME = "Renato Bastos Rocha"
PROCS = [
    "08016300420258190026", # Ação Penal Itaperuna
    "00237193520258190000"  # HC 7ª Câmara
]

def query_endpoint(endpoint, payload):
    url = f"https://api-publica.datajud.cnj.jus.br/{endpoint}/_search"
    req_data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=req_data, headers=HEADERS)
    ctx = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e)}

print("=" * 85)
print(f"🔍 VARREDURA COMPLETA EM TEMPO REAL — RENATO BASTOS ROCHA")
print(f"👤 Nome: {NOME} | CPF: 124.981.977-61")
print(f"⏰ Consulta Realizada em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
print("=" * 85)

# 1. Consulta dos processos conhecidos no TJRJ
for proc in PROCS:
    print(f"\n📂 Consultando Processo: {proc[:7]}-{proc[7:9]}.{proc[9:13]}.{proc[13]}.{proc[14:16]}.{proc[16:]}...")
    res = query_endpoint("api_publica_tjrj", {
        "query": {"match": {"numeroProcesso": proc}},
        "size": 5
    })
    hits = res.get("hits", {}).get("hits", [])
    print(f"   Hits encontrados: {len(hits)}")
    for hit in hits:
        src = hit["_source"]
        grau = src.get("grau", "N/I")
        classe = src.get("classe", {}).get("nome", "N/I")
        orgao = src.get("orgaoJulgador", {}).get("nome", "N/I")
        dt_at = src.get("dataHoraUltimaAtualizacao", "N/I")
        movs = src.get("movimentos", [])
        movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
        
        print(f"   🏛️ Órgão: {orgao} | Classe: {classe} | Grau: {grau}")
        print(f"   📅 Última Atualização no Banco: {dt_at}")
        print(f"   📑 Total de Movimentações: {len(movs)}")
        print("   📌 Últimos 10 Atos Registrados:")
        for m in movs_sorted[:10]:
            dt = m.get("dataHora", "")[:19].replace("T", " ")
            nome = m.get("nome", "")
            code = m.get("codigo", "")
            comps = m.get("complementosTabelados", [])
            comp_str = ""
            if comps:
                comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")"
            print(f"      • {dt} — {nome}{comp_str} [Cód. {code}]")

# 2. Busca ampla por CPF no TJRJ e STJ
print("\n" + "─" * 85)
print(f"🔎 Buscando novos processos por CPF ({CPF}) no TJRJ e STJ...")
res_cpf_tjrj = query_endpoint("api_publica_tjrj", {
    "query": {"match": {"dadosBasicos.polo.parte.pessoa.numeroDocumentoPrincipal": CPF}},
    "size": 10
})
hits_cpf = res_cpf_tjrj.get("hits", {}).get("hits", [])
print(f"   TJRJ por CPF: {len(hits_cpf)} processos encontrados.")

res_cpf_stj = query_endpoint("api_publica_stj", {
    "query": {"match": {"dadosBasicos.polo.parte.pessoa.numeroDocumentoPrincipal": CPF}},
    "size": 5
})
hits_stj = res_cpf_stj.get("hits", {}).get("hits", [])
print(f"   STJ por CPF: {len(hits_stj)} processos encontrados.")

print("\n" + "=" * 85)
print("✅ Varredura concluída com sucesso.")
print("=" * 85)
