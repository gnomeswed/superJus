# -*- coding: utf-8 -*-
"""
SUPERJUS — VARREDURA EXAUSTIVA DE NOVO PROCESSO DE RENATO BASTOS ROCHA (2026)
Pesquisa em DataJud TJRJ, TRF2, STJ por:
- "Renato Bastos Rocha"
- CPF "12498197761"
- "Renato Bastos" em Itaperuna / Região Noroeste / Custódia / VEP
- Termos de Furto em 2026
"""

import sys, os, json, ssl, urllib.request
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {
    'Authorization': f"APIKey {API_KEY}",
    'Content-Type': 'application/json'
}

CPF = "12498197761"
NOME = "Renato Bastos Rocha"

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
print(f"🔍 VARREDURA EXAUSTIVA — NOVO PROCESSO / FLAGRANTE / FURTO 2026: {NOME}")
print(f"⏰ Consulta em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
print("=" * 85)

queries = [
    # 1. Busca por nome no campo dadosBasicos.polo.parte.pessoa.nome
    ("TJRJ - Nome Exato", "api_publica_tjrj", {
        "query": {"match_phrase": {"dadosBasicos.polo.parte.pessoa.nome": NOME}},
        "size": 20
    }),
    # 2. Busca por query string geral
    ("TJRJ - Query String Nome", "api_publica_tjrj", {
        "query": {"query_string": {"query": f'"{NOME}"'}},
        "size": 20
    }),
    # 3. Busca por CPF no TJRJ
    ("TJRJ - CPF", "api_publica_tjrj", {
        "query": {"query_string": {"query": f'"{CPF}" OR "124.981.977-61"'}},
        "size": 20
    }),
    # 4. Busca por "Renato Bastos" na comarca de Itaperuna
    ("TJRJ - Itaperuna + Renato Bastos", "api_publica_tjrj", {
        "query": {
            "bool": {
                "must": [
                    {"query_string": {"query": '"Renato Bastos"'}},
                    {"match_phrase": {"orgaoJulgador.nome": "ITAPERUNA"}}
                ]
            }
        },
        "size": 20
    }),
    # 5. Busca em Custódia (Campos / Benfica) com "Renato Bastos"
    ("TJRJ - Custódia + Renato Bastos", "api_publica_tjrj", {
        "query": {
            "bool": {
                "must": [
                    {"query_string": {"query": '"Renato Bastos"'}}
                ]
            }
        },
        "size": 30
    }),
    # 6. Busca por número de processo em 2026 em Itaperuna com assunto Furto
    ("TJRJ - Itaperuna 2026 Furto", "api_publica_tjrj", {
        "query": {
            "bool": {
                "must": [
                    {"match_phrase": {"orgaoJulgador.nome": "ITAPERUNA"}},
                    {"wildcard": {"numeroProcesso": "*20268190026"}},
                    {"query_string": {"query": "Furto"}}
                ]
            }
        },
        "size": 20
    })
]

encontrados = {}

for label, endpoint, payload in queries:
    print(f"\n🔎 [{label}] Executando pesquisa...", flush=True)
    res = query_endpoint(endpoint, payload)
    hits = res.get("hits", {}).get("hits", [])
    print(f"   -> {len(hits)} hits encontrados.", flush=True)
    for h in hits:
        src = h["_source"]
        num = src.get("numeroProcesso", "N/I")
        classe = src.get("classe", {}).get("nome", "N/I")
        orgao = src.get("orgaoJulgador", {}).get("nome", "N/I")
        dt_aj = src.get("dataAjuizamento", "N/I")
        dt_at = src.get("dataHoraUltimaAtualizacao", "N/I")
        assuntos = [a.get("nome", "") for a in src.get("assuntos", [])]
        movs = src.get("movimentos", [])
        
        # Obter nomes das partes
        polos = src.get("dadosBasicos", {}).get("polo", [])
        partes_str = []
        for p in polos:
            for part in p.get("parte", []):
                pess = part.get("pessoa", {})
                if pess.get("nome"):
                    partes_str.append(f"{pess.get('nome')} ({p.get('polo')})")

        encontrados[num] = {
            "numeroProcesso": num,
            "orgao": orgao,
            "classe": classe,
            "dataAjuizamento": dt_aj,
            "dataHoraUltimaAtualizacao": dt_at,
            "assuntos": assuntos,
            "partes": partes_str,
            "total_movimentos": len(movs),
            "ultimos_movimentos": movs[-5:] if movs else []
        }

print("\n" + "=" * 85)
print(f"📊 RESULTADO FINAL DA VARREDURA: {len(encontrados)} PROCESSO(S) IDENTIFICADO(S)")
print("=" * 85)

for num, d in encontrados.items():
    print(f"\n📂 Processo: {num}")
    print(f"   🏛️ Órgão: {d['orgao']} | Classe: {d['classe']}")
    print(f"   📅 Ajuizamento: {d['dataAjuizamento']} | Atualização: {d['dataHoraUltimaAtualizacao']}")
    print(f"   📌 Assuntos: {', '.join(d['assuntos'])}")
    print(f"   👥 Partes: {', '.join(d['partes'][:4])}")
    print(f"   📑 Movimentações: {d['total_movimentos']}")

# Salvar resultado
out_file = Path(r"c:\Projetos\superJus\Clientes\Renato_Bastos_Rocha\resultado_varredura_novo_2026.json")
with open(out_file, "w", encoding="utf-8") as fp:
    json.dump(encontrados, fp, indent=2, ensure_ascii=False)

print(f"\n✅ Relatório JSON salvo em: {out_file}")
