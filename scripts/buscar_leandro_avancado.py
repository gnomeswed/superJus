# -*- coding: utf-8 -*-
"""
Busca avançada — CPF, co-réus, e tentativa de acesso PJe.
Leandro da Silva CPF: 059.830.127-54
"""
import requests, json, os, time

DATAJUD_KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {"Authorization": DATAJUD_KEY, "Content-Type": "application/json"}
BASE_TJRJ = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"

OUTPUT_DIR = r"C:\Projetos\superJus\Clientes\Leandro_Mecanico\busca_completa"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def search(base_url, query, size=20):
    try:
        r = requests.post(base_url, headers=HEADERS, json={"query": query, "size": size}, timeout=30)
        if r.status_code == 200:
            return r.json().get("hits", {}).get("hits", []), r.json().get("hits", {}).get("total", {})
        print(f"  HTTP {r.status_code}: {r.text[:200]}")
        return [], {}
    except Exception as e:
        print(f"  Erro: {e}")
        return [], {}

def fmt(num):
    if len(num) != 20: return num
    return f"{num[:7]}-{num[7:9]}.{num[9:13]}.{num[13:15]}.{num[15:19]}.{num[19:]}"

# ===== 1: Busca por CPF nos processo PJe =====
print("=" * 60)
print("BUSCA 1: Por CPF 059.830.127-54 (Leandro)")
print("=" * 60)

# DataJud indexes CPF in different ways, try several
cpf_clean = "05983012754"
for query_name, q in [
    ("match documentos.valor", {"match": {"documentos.valor": cpf_clean}}),
    ("wildcard documentos.valor", {"wildcard": {"documentos.valor": f"*{cpf_clean}*"}}),
    ("query_string documentos", {"query_string": {"query": cpf_clean, "default_field": "documentos.valor"}}),
]:
    hits, total = search(BASE_TJRJ, q, size=10)
    print(f"  {query_name}: {total}")
    for h in hits:
        src = h.get("_source", {})
        print(f"    → {fmt(src.get('numeroProcesso',''))} | {src.get('classe',{}).get('nome','')}")

# ===== 2: Busca por co-réus =====
print("\n" + "=" * 60)
print("BUSCA 2: Por co-réus (Ryan, Reinaldo, João Clayton)")
print("=" * 60)

for nome in ["RYAN FERREIRA VENCESLAU", "REINALDO VENCESLAU DOS SANTOS", "JOAO CLAYTON DE JESUS FERREIRA"]:
    hits, total = search(BASE_TJRJ, 
        {"query_string": {"query": f'"{nome}"', "default_field": "*"}}, size=5)
    print(f"\n  {nome}: {total}")
    for h in hits:
        src = h.get("_source", {})
        num = fmt(src.get('numeroProcesso',''))
        classe = src.get('classe',{}).get('nome','')
        orgao = src.get('orgaoJulgador',{}).get('nome','')
        print(f"    → {num} | {classe} | {orgao}")

# ===== 3: Busca TJRJ 2ª instância — HC com réu Leandro =====
print("\n" + "=" * 60)
print("BUSCA 3: TJRJ 2ª instância — HC/RHC/Apelação")
print("=" * 60)

# Search for any HC in TJRJ that mentions Leandro da Silva
for classe in ["Habeas Corpus", "Recurso em Sentido Estrito", "Apelação"]:
    hits, total = search(BASE_TJRJ,
        {"bool": {"must": [
            {"match": {"classe.nome": classe}},
            {"match_phrase": {"_all": "Leandro da Silva"}}
        ]}}, size=10)
    print(f"\n  {classe}: {total}")
    for h in hits:
        src = h.get("_source", {})
        num = fmt(src.get('numeroProcesso',''))
        orgao = src.get('orgaoJulgador',{}).get('nome','')
        print(f"    → {num} | {orgao}")

# ===== 4: Busca wildcard por número raiz 0827233-23* =====
print("\n" + "=" * 60)
print("BUSCA 4: Wildcard 0827233-23* (mesmo ano, mesma comarca)")
print("=" * 60)

hits, total = search(BASE_TJRJ, 
    {"wildcard": {"numeroProcesso": "082723323*"}}, size=20)
print(f"  Total: {total}")
for h in hits:
    src = h.get("_source", {})
    num = fmt(src.get('numeroProcesso',''))
    classe = src.get('classe',{}).get('nome','')
    orgao = src.get('orgaoJulgador',{}).get('nome','')
    movimentos = src.get('movimentos', [])
    print(f"  → {num} | {classe} | {orgao} | {len(movimentos)} movs")

# ===== 5: Tentar acessar PJe via URL do documento =====
print("\n" + "=" * 60)
print("BUSCA 5: Tentativa de acesso ao documento PJe")
print("=" * 60)

try:
    pje_url = "https://tjrj.pje.jus.br:443/pje/Processo/ConsultaDocumento/listView.seam?x=26061119331904800000272755463"
    r = requests.get(pje_url, timeout=15, allow_redirects=True)
    print(f"  PJe status: {r.status_code}")
    print(f"  PJe URL final: {r.url[:100]}")
    print(f"  PJe body: {r.text[:500]}")
except Exception as e:
    print(f"  PJe erro: {e}")

# ===== SALVAR =====
print("\n" + "=" * 60)
print("SALVANDO RESULTADOS...")
print("=" * 60)

results = {
    "cpf_leandro": cpf_clean,
    "co_reus": ["RYAN FERREIRA VENCESLAU", "REINALDO VENCESLAU DOS SANTOS", "JOAO CLAYTON DE JESUS FERREIRA"],
    "nota": "DataJud retornou 0 para buscas por CPF e co-réus — provavelmente sigiloso. Portal TJRJ bloqueado por PJe."
}

out = os.path.join(OUTPUT_DIR, "busca_avancada.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"Salvo: {out}")

print("\n✓ Busca avançada finalizada!")
