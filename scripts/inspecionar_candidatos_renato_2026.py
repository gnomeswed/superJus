# -*- coding: utf-8 -*-
"""
SUPERJUS — INSPEÇÃO DETALHADA DOS CANDIDATOS DE 2026 EM ITAPERUNA
Inspeciona os processos de furto / flagrante de 2026 para encontrar o novo caso de Renato Bastos Rocha.
"""

import sys, json, ssl, urllib.request
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {'Authorization': f"APIKey {API_KEY}", 'Content-Type': 'application/json'}

candidate_file = Path(r"c:\Projetos\superJus\Clientes\Renato_Bastos_Rocha\resultado_varredura_novo_2026.json")
data = json.load(open(candidate_file, encoding="utf-8"))

print("=" * 85)
print(f"🔍 ANALISANDO {len(data)} PROCESSOS CANDIDATOS DE FURTO / FLAGRANTE EM ITAPERUNA (2026)")
print("=" * 85)

for num, d in data.items():
    url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
    payload = json.dumps({"query": {"match": {"numeroProcesso": num}}, "size": 1}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=HEADERS)
    ctx = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            hits = res.get("hits", {}).get("hits", [])
            if hits:
                src = hits[0]["_source"]
                movs = src.get("movimentos", [])
                movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
                
                # Check for mention of Renato or flagrante in complementos
                txt_all = json.dumps(src, ensure_ascii=False)
                has_renato = "renato" in txt_all.lower()
                has_rocha = "rocha" in txt_all.lower()
                has_flagrante = "flagrante" in txt_all.lower() or "preventiva" in txt_all.lower() or "custódia" in txt_all.lower() or "prisão" in txt_all.lower()
                
                num_fmt = f"{num[:7]}-{num[7:9]}.{num[9:13]}.{num[13]}.{num[14:16]}.{num[16:]}" if len(num) == 20 else num
                print(f"\n📂 Processo: {num_fmt} ({d['orgao']})")
                print(f"   Classe: {d['classe']} | Ajuizado em: {d['dataAjuizamento']}")
                print(f"   Total de Movimentos: {len(movs)} | Prisão/Flagrante no texto: {has_flagrante}")
                if has_renato or has_rocha:
                    print(f"   ⭐ MATCH NOME: Renato={has_renato}, Rocha={has_rocha}")
                print("   Últimos atos:")
                for m in movs_sorted[:4]:
                    dt = m.get("dataHora", "")[:19].replace("T", " ")
                    nm = m.get("nome", "")
                    comps = m.get("complementosTabelados", [])
                    comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")" if comps else ""
                    print(f"      • {dt} — {nm}{comp_str}")
    except Exception as e:
        print(f"Erro em {num}: {e}")

print("\n" + "=" * 85)
print("✅ Análise dos candidatos concluída.")
print("=" * 85)
