# -*- coding: utf-8 -*-
"""
Busca completa de processos do Leandro da Silva em todas as instâncias.
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
    """Search DataJud API and return hits."""
    try:
        r = requests.post(base_url, headers=HEADERS, json={"query": query, "size": size}, timeout=30)
        if r.status_code == 200:
            data = r.json()
            hits = data.get("hits", {}).get("hits", [])
            return hits, data.get("hits", {}).get("total", {})
        else:
            print(f"  [!] HTTP {r.status_code}: {r.text[:200]}")
            return [], {}
    except Exception as e:
        print(f"  [!] Erro: {e}")
        return [], {}

def format_number(clean_num):
    """Format 20-digit clean number to CNJ format."""
    if len(clean_num) != 20:
        return clean_num
    return f"{clean_num[:7]}-{clean_num[7:9]}.{clean_num[9:13]}.{clean_num[13:15]}.{clean_num[15:19]}.{clean_num[19:]}"

def extract_process_info(hit):
    """Extract key info from a DataJud hit."""
    src = hit.get("_source", {})
    numero = src.get("numeroProcesso", "")
    classe = src.get("classe", {}).get("nome", "")
    orgao = src.get("orgaoJulgador", {}).get("nome", "")
    data_ult = src.get("dataHoraUltimaAtualizacao", "")
    movimentos = src.get("movimentos", [])
    
    # Get last 5 movements
    movs_recentes = sorted(movimentos, key=lambda m: m.get("dataHora", ""), reverse=True)[:5]
    
    return {
        "numeroProcesso": numero,
        "numeroFormatado": format_number(numero),
        "classe": classe,
        "orgaoJulgador": orgao,
        "dataUltimaAtualizacao": data_ult,
        "movimentosRecentes": [
            {
                "data": m.get("dataHora", ""),
                "tipo": m.get("nome", ""),
                "orgao": m.get("orgaoJulgador", {}).get("nome", "")
            } for m in movs_recentes
        ],
        "totalMovimentos": len(movimentos),
        "nivelSigilo": src.get("nivelSigilo", 0),
        "raw": src
    }

# ===== PARTE 1: Busca por texto (nome) =====
print("=" * 60)
print("ETAPA 1: Busca DataJud TJRJ por nome 'Leandro da Silva'")
print("=" * 60)

hits_tjrj_name, total = datajud_search(BASE_TJRJ, 
    {"query": {"query_string": {"query": "Leandro da Silva"}}}, size=20)
print(f"  Total encontrados: {total}")
for h in hits_tjrj_name:
    info = extract_process_info(h)
    print(f"  → {info['numeroFormatado']} | {info['classe']} | {info['orgaoJulgador']}")

# ===== PARTE 2: Busca pelo número específico =====
print("\n" + "=" * 60)
print("ETAPA 2: Busca DataJud TJRJ pelo número 0827233-23.2026.8.19.0001")
print("=" * 60)

clean_num = "08272332320268190001"
hits_tjrj_proc, total = datajud_search(BASE_TJRJ, 
    {"match": {"numeroProcesso": clean_num}}, size=5)
print(f"  Total encontrados: {total}")
for h in hits_tjrj_proc:
    info = extract_process_info(h)
    print(f"  → {info['numeroFormatado']} | {info['classe']} | {info['orgaoJulgador']}")
    print(f"    Última atualização: {info['dataUltimaAtualizacao']}")
    print(f"    Movimentos: {info['totalMovimentos']}")

# ===== PARTE 3: Busca wildcard 0827233* (todos os processos com esse número) =====
print("\n" + "=" * 60)
print("ETAPA 3: Busca DataJud TJRJ wildcard 0827233*")
print("=" * 60)

hits_tjrj_wild, total = datajud_search(BASE_TJRJ, 
    {"wildcard": {"numeroProcesso": "0827233*"}}, size=10)
print(f"  Total encontrados: {total}")
for h in hits_tjrj_wild:
    info = extract_process_info(h)
    print(f"  → {info['numeroFormatado']} | {info['classe']} | {info['orgaoJulgador']}")

# ===== PARTE 4: Busca STJ por nome =====
print("\n" + "=" * 60)
print("ETAPA 4: Busca DataJud STJ por nome 'Leandro da Silva'")
print("=" * 60)

hits_stj_name, total = datajud_search(BASE_STJ, 
    {"query": {"query_string": {"query": "Leandro da Silva"}}}, size=20)
print(f"  Total encontrados: {total}")
for h in hits_stj_name:
    info = extract_process_info(h)
    print(f"  → {info['numeroFormatado']} | {info['classe']} | {info['orgaoJulgador']}")

# ===== PARTE 5: Busca STJ por número do processo TJRJ =====
print("\n" + "=" * 60)
print("ETAPA 5: Busca DataJud STJ por número 0827233*")
print("=" * 60)

hits_stj_proc, total = datajud_search(BASE_STJ, 
    {"wildcard": {"numeroProcesso": "0827233*"}}, size=10)
print(f"  Total encontrados: {total}")
for h in hits_stj_proc:
    info = extract_process_info(h)
    print(f"  → {info['numeroFormatado']} | {info['classe']} | {info['orgaoJulgador']}")

# ===== PARTE 6: Busca TJRJ 2ª instância por nome do réu =====
print("\n" + "=" * 60)
print("ETAPA 6: Busca DataJud TJRJ 2ª instância (apelacoes, HCs)")
print("=" * 60)

# Search for HC with the party name
for classe in ["Habeas Corpus", "Recurso Criminal", "Recurso em Sentido Estrito", "Apelação Criminal"]:
    print(f"\n  Buscando: {classe}...")
    hits, total = datajud_search(BASE_TJRJ, 
        {"bool": {"must": [
            {"match": {"classe.nome": classe}},
            {"query_string": {"query": "Leandro da Silva"}}
        ]}}, size=10)
    print(f"  Total: {total}")
    for h in hits:
        info = extract_process_info(h)
        print(f"    → {info['numeroFormatado']} | {info['classe']} | {info['orgaoJulgador']}")

# ===== SALVAR TUDO =====
print("\n" + "=" * 60)
print("SALVANDO RESULTADOS...")
print("=" * 60)

all_results = {
    "busca_por_nome_tjrj": [extract_process_info(h) for h in hits_tjrj_name],
    "busca_por_numero_tjrj": [extract_process_info(h) for h in hits_tjrj_proc],
    "busca_wildcard_tjrj": [extract_process_info(h) for h in hits_tjrj_wild],
    "busca_nome_stj": [extract_process_info(h) for h in hits_stj_name],
    "busca_numero_stj": [extract_process_info(h) for h in hits_stj_proc],
}

output_file = os.path.join(OUTPUT_DIR, "datajud_resultados_completos.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)
print(f"Salvo em: {output_file}")

# Also save raw data for the main process
if hits_tjrj_proc:
    raw_file = os.path.join(OUTPUT_DIR, "datajud_raw_processo_principal.json")
    with open(raw_file, "w", encoding="utf-8") as f:
        json.dump(hits_tjrj_proc[0].get("_source", {}), f, ensure_ascii=False, indent=2)
    print(f"Raw do processo principal: {raw_file}")

print("\n✓ Busca completa finalizada!")
