# -*- coding: utf-8 -*-
"""
Busca completa de processos do Leandro da Silva — v2 corrigido.
PJe 0827233-23.2026.8.19.0001 — TJRJ + DataJud + STJ
"""
import json, os, sys, time, requests

DATAJUD_KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {"Authorization": DATAJUD_KEY, "Content-Type": "application/json"}
BASE_TJRJ = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
BASE_STJ  = "https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search"

OUTPUT_DIR = r"C:\Projetos\superJus\Clientes\Leandro_Mecanico\busca_completa"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def datajud_search(base_url, query, size=20):
    try:
        r = requests.post(base_url, headers=HEADERS, json={"query": query, "size": size}, timeout=30)
        if r.status_code == 200:
            data = r.json()
            hits = data.get("hits", {}).get("hits", [])
            total = data.get("hits", {}).get("total", {})
            return hits, total
        else:
            print(f"  [!] HTTP {r.status_code}: {r.text[:300]}")
            return [], {}
    except Exception as e:
        print(f"  [!] Erro: {e}")
        return [], {}

def format_number(clean_num):
    if len(clean_num) != 20:
        return clean_num
    return f"{clean_num[:7]}-{clean_num[7:9]}.{clean_num[9:13]}.{clean_num[13:15]}.{clean_num[15:19]}.{clean_num[19:]}"

def extract_info(hit):
    src = hit.get("_source", {})
    numero = src.get("numeroProcesso", "")
    classe = src.get("classe", {}).get("nome", "")
    orgao = src.get("orgaoJulgador", {}).get("nome", "")
    data_ult = src.get("dataHoraUltimaAtualizacao", "")
    movimentos = src.get("movimentos", [])
    movs_recentes = sorted(movimentos, key=lambda m: m.get("dataHora", ""), reverse=True)[:10]
    
    return {
        "numeroProcesso": numero,
        "numeroFormatado": format_number(numero) if len(numero) == 20 else numero,
        "classe": classe,
        "orgaoJulgador": orgao,
        "dataUltimaAtualizacao": data_ult,
        "totalMovimentos": len(movimentos),
        "movimentosRecentes": [
            {"data": m.get("dataHora", ""), "tipo": m.get("nome", "")}
            for m in movs_recentes
        ],
        "nivelSigilo": src.get("nivelSigilo", 0),
        "raw": src
    }

# ===== 1: Busca por nome no TJRJ (query_string correto) =====
print("=" * 60)
print("ETAPA 1: Busca DataJud TJRJ por nome")
print("=" * 60)

hits, total = datajud_search(BASE_TJRJ, 
    {"query_string": {"query": "\"Leandro da Silva\"", "default_field": "*"}}, size=20)
print(f"  Total: {total}")
name_results = []
for h in hits:
    info = extract_info(h)
    name_results.append(info)
    print(f"  → {info['numeroFormatado']} | {info['classe']} | {info['orgaoJulgador']}")

# ===== 2: Busca pelo número específico =====
print("\n" + "=" * 60)
print("ETAPA 2: Busca pelo número 0827233-23.2026.8.19.0001")
print("=" * 60)

clean = "08272332320268190001"
hits2, total2 = datajud_search(BASE_TJRJ, {"match": {"numeroProcesso": clean}}, size=5)
print(f"  Total: {total2}")
proc_results = []
for h in hits2:
    info = extract_info(h)
    proc_results.append(info)
    print(f"  → {info['numeroFormatado']} | {info['classe']} | {info['orgaoJulgador']}")
    print(f"    Última: {info['dataUltimaAtualizacao']}")
    print(f"    Movimentos: {info['totalMovimentos']}")
    for m in info['movimentosRecentes']:
        print(f"      {m['data'][:10]} — {m['tipo']}")

# ===== 3: Busca STJ por nome =====
print("\n" + "=" * 60)
print("ETAPA 3: Busca DataJud STJ por nome")
print("=" * 60)

hits3, total3 = datajud_search(BASE_STJ, 
    {"query_string": {"query": "\"Leandro da Silva\"", "default_field": "*"}}, size=20)
print(f"  Total: {total3}")
stj_results = []
for h in hits3:
    info = extract_info(h)
    stj_results.append(info)
    print(f"  → {info['numeroFormatado']} | {info['classe']} | {info['orgaoJulgador']}")

# ===== 4: Busca STJ wildcard pelo número base =====
print("\n" + "=" * 60)
print("ETAPA 4: Busca STJ wildcard 0827233*")
print("=" * 60)

hits4, total4 = datajud_search(BASE_STJ, {"wildcard": {"numeroProcesso": "0827233*"}}, size=10)
print(f"  Total: {total4}")
for h in hits4:
    info = extract_info(h)
    print(f"  → {info['numeroFormatado']} | {info['classe']} | {info['orgaoJulgador']}")

# ===== 5: Busca TJRJ 2ª instância — HC e RHC com parties =====
print("\n" + "=" * 60)
print("ETAPA 5: Busca TJRJ 2ª instância por partes (Leandro)")
print("=" * 60)

for classe in ["Habeas Corpus", "Recurso em Sentido Estrito", "Apelação"]:
    hits5, total5 = datajud_search(BASE_TJRJ, 
        {"bool": {"must": [
            {"match": {"classe.nome": classe}},
            {"match_phrase": {"movimentos.complementosTabelados": "Leandro"}}
        ]}}, size=5)
    print(f"\n  {classe}: Total {total5}")
    for h in hits5:
        info = extract_info(h)
        # Verify it's actually related to Leandro
        partes = str(info['raw'].get('assunto', []))
        print(f"    → {info['numeroFormatado']} | {info['orgaoJulgador']}")

# ===== 6: Busca TJRJ com parties field =====
print("\n" + "=" * 60)
print("ETAPA 6: Busca TJRJ por campo 'partes'")
print("=" * 60)

hits6, total6 = datajud_search(BASE_TJRJ,
    {"query_string": {"query": "Leandro da Silva", "fields": ["partes.nome", "assunto.nome"]}}, size=20)
print(f"  Total: {total6}")
parte_results = []
for h in hits6:
    info = extract_info(h)
    parte_results.append(info)
    print(f"  → {info['numeroFormatado']} | {info['classe']} | {info['orgaoJulgador']}")

# ===== SALVAR =====
print("\n" + "=" * 60)
print("SALVANDO...")
print("=" * 60)

all_data = {
    "busca_nome_tjrj": name_results,
    "processo_principal_tjrj": proc_results,
    "busca_nome_stj": stj_results,
    "busca_partes_tjrj": parte_results,
}

out = os.path.join(OUTPUT_DIR, "datajud_resultados_v2.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)
print(f"Salvo: {out}")

# Raw do processo principal se encontrado
if proc_results:
    raw_out = os.path.join(OUTPUT_DIR, "processo_principal_raw.json")
    with open(raw_out, "w", encoding="utf-8") as f:
        json.dump(proc_results[0]['raw'], f, ensure_ascii=False, indent=2)
    print(f"Raw processo principal: {raw_out}")

print("\n✓ Busca v2 finalizada!")
