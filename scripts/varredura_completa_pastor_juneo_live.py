# -*- coding: utf-8 -*-
"""
SUPERJUS — VARREDURA EXAUSTIVA ONLINE: PASTOR JUNEO
Busca em:
1. DataJud TJRJ (1ª e 2ª Instâncias)
2. DataJud STJ (Habeas Corpus e Recursos)
3. Diário de Justiça Eletrônico Nacional (DJEN / Comunica PJe)
4. Consulta PJe TJRJ via Playwright
"""

import sys, os, json, ssl, urllib.request, urllib.parse, time
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

DATAJUD_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS_DATAJUD = {
    'Authorization': f"APIKey {DATAJUD_KEY}",
    'Content-Type': 'application/json'
}

PROC_NUM = "0810659-95.2026.8.19.0203"
PROC_CLEAN = "08106599520268190203"
CPF = "09176703703"
CPF_FMT = "091.767.037-03"
NOME = "Juneo Luciano de Oliveira"

print("=" * 85)
print(f"🔍 VARREDURA MULTI-FONTE AO VIVO — PASTOR JUNEO")
print(f"⚖️ Processo: {PROC_NUM} | CPF: {CPF_FMT} | Nome: {NOME}")
print(f"⏰ Consulta: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
print("=" * 85)

ctx = ssl._create_unverified_context()
achados = {}

# -------------------------------------------------------------
# 1. DATAJUD TJRJ — BUSCA POR NÚMERO
# -------------------------------------------------------------
print("\n[1] DATAJUD TJRJ — Consulta por número de processo...", flush=True)
url_tjrj = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"

queries = [
    ("Por Número Limpo", {"query": {"match": {"numeroProcesso": PROC_CLEAN}}, "size": 10}),
    ("Por Número Formatado", {"query": {"match": {"numeroProcesso": PROC_NUM}}, "size": 10}),
    ("Por CPF do Réu", {"query": {"query_string": {"query": f'"{CPF}" OR "{CPF_FMT}"'}}, "size": 10}),
    ("Por Nome do Réu", {"query": {"match_phrase": {"dadosBasicos.polo.parte.pessoa.nome": NOME}}, "size": 10})
]

for label, payload in queries:
    req = urllib.request.Request(url_tjrj, data=json.dumps(payload).encode('utf-8'), headers=HEADERS_DATAJUD)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            hits = data.get("hits", {}).get("hits", [])
            print(f"   • {label}: {len(hits)} registro(s) encontrado(s)")
            for h in hits:
                src = h["_source"]
                np = src.get("numeroProcesso")
                achados[np] = src
    except Exception as e:
        print(f"   • {label}: Erro ({e})")

# -------------------------------------------------------------
# 2. DATAJUD STJ — BUSCA POR HABEAS CORPUS
# -------------------------------------------------------------
print("\n[2] DATAJUD STJ — Verificação de Habeas Corpus ou Recursos...", flush=True)
url_stj = "https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search"
queries_stj = [
    ("STJ por Nome", {"query": {"match_phrase": {"dadosBasicos.polo.parte.pessoa.nome": NOME}}, "size": 5}),
    ("STJ por CPF", {"query": {"query_string": {"query": f'"{CPF}" OR "{CPF_FMT}"'}}, "size": 5})
]

for label, payload in queries_stj:
    req = urllib.request.Request(url_stj, data=json.dumps(payload).encode('utf-8'), headers=HEADERS_DATAJUD)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            hits = data.get("hits", {}).get("hits", [])
            print(f"   • {label}: {len(hits)} registro(s)")
            for h in hits:
                src = h["_source"]
                np = src.get("numeroProcesso")
                achados[f"STJ_{np}"] = src
    except Exception as e:
        print(f"   • {label}: Erro ({e})")

# -------------------------------------------------------------
# 3. DIÁRIO DE JUSTIÇA ELETRÔNICO NACIONAL (DJEN / COMUNICA PJE)
# -------------------------------------------------------------
print("\n[3] DJEN / COMUNICA PJE — Varredura de Publicações Oficiais...", flush=True)
url_comunica = "https://comunicaapi.pje.jus.br/api/v1/comunicacao"
headers_comunica = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

params_list = [
    ("Por Número do Processo", f"?numeroProcesso={PROC_CLEAN}&itensPorPagina=15"),
    ("Por Nome do Réu", f"?nomeParte={urllib.parse.quote(NOME)}&itensPorPagina=15")
]

comunicacoes = []
for label, qstr in params_list:
    req = urllib.request.Request(url_comunica + qstr, headers=headers_comunica)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            d = json.loads(resp.read().decode('utf-8'))
            items = d.get("items", [])
            print(f"   • {label}: {len(items)} publicação(ões)")
            for it in items:
                comunicacoes.append(it)
    except Exception as e:
        print(f"   • {label}: Erro ({e})")

# -------------------------------------------------------------
# 4. PROCESSAMENTO DOS RESULTADOS
# -------------------------------------------------------------
print("\n" + "=" * 85)
print(f"📊 CONSOLIDAÇÃO DOS DADOS ENCONTRADOS")
print("=" * 85)

if achados:
    for np, src in achados.items():
        orgao = src.get("orgaoJulgador", {}).get("nome", "N/I")
        classe = src.get("classe", {}).get("nome", "N/I")
        dt_at = src.get("dataHoraUltimaAtualizacao", "N/I")
        dt_aj = src.get("dataAjuizamento", "N/I")
        movs = src.get("movimentos", [])
        movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
        
        print(f"\n📂 Processo: {np}")
        print(f"   🏛️ Órgão: {orgao} | Classe: {classe}")
        print(f"   📅 Ajuizado em: {dt_aj} | Última Atualização no Banco: {dt_at}")
        print(f"   📑 Total de Movimentos Cadastrados: {len(movs)}")
        print("   📜 Movimentações:")
        for m in movs_sorted[:15]:
            dt = m.get("dataHora", "")[:19].replace("T", " ")
            nm = m.get("nome", "")
            comps = m.get("complementosTabelados", [])
            comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")" if comps else ""
            print(f"      • {dt} — {nm}{comp_str}")
else:
    print("⚠️ Nenhum registro bruto retornado pelos endpoints DataJud (provável segredo de justiça ou indexação em nível restrito).")

if comunicacoes:
    print("\n📢 PUBLICAÇÕES NO DJEN (DIÁRIO ELETRÔNICO):")
    for c in comunicacoes:
        dt_disp = c.get("data_disponibilizacao", "")
        trib = c.get("siglaTribunal", "")
        orgao = c.get("nomeOrgao", "")
        texto = c.get("texto", "")
        print(f"\n   🗓️ Data: {dt_disp} | Tribunal: {trib} — {orgao}")
        print(f"   📄 Trecho: {texto[:400]}...")
else:
    print("\n📢 Nenhuma publicação veiculada no DJEN.")

# Salvar relatório consolidado
out_file = Path(r"c:\Projetos\superJus\Clientes\Pastor_Juneo\resultado_varredura_completa_04_09_2026.json")
with open(out_file, "w", encoding="utf-8") as fp:
    json.dump({"processos": achados, "comunicacoes": comunicacoes}, fp, indent=2, ensure_ascii=False)

print(f"\n💾 Arquivo salvo com sucesso em: {out_file}")
print("=" * 85)
