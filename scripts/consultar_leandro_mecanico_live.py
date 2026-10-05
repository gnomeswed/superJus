# -*- coding: utf-8 -*-
"""
SUPERJUS — CONSULTA EM TEMPO REAL: LEANDRO DA SILVA ("LEANDRO MECÂNICO")
Processo: 0827233-23.2026.8.19.0001 (1ª Vara Criminal da Regional de Santa Cruz / TJRJ)
CPF: 059.830.127-54
"""

import sys, os, json, ssl, urllib.request
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {'Authorization': f"APIKey {API_KEY}", 'Content-Type': 'application/json'}

proc_clean = "08272332320268190001"
proc_fmt = "0827233-23.2026.8.19.0001"
cpf = "05983012754"

print("=" * 85)
print(f"🔍 CONSULTA EM TEMPO REAL — LEANDRO DA SILVA ('LEANDRO MECÂNICO')")
print(f"⚖️ Processo: {proc_fmt} | CPF: 059.830.127-54")
print(f"⏰ Consulta Realizada em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
print("=" * 85)

# 1. Consulta DataJud TJRJ pelo número do processo
url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
payload = json.dumps({"query": {"match": {"numeroProcesso": proc_clean}}, "size": 5}).encode("utf-8")
req = urllib.request.Request(url, data=payload, headers=HEADERS)
ctx = ssl._create_unverified_context()

try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        hits = data.get("hits", {}).get("hits", [])
        print(f"Total de registros encontrados no DataJud TJRJ: {len(hits)}")
        for hit in hits:
            src = hit["_source"]
            orgao = src.get("orgaoJulgador", {}).get("nome", "N/I")
            classe = src.get("classe", {}).get("nome", "N/I")
            dt_at = src.get("dataHoraUltimaAtualizacao", "N/I")
            movs = src.get("movimentos", [])
            movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
            
            print(f"\n🏛️ Órgão: {orgao} | Classe: {classe}")
            print(f"📅 Última Atualização no Sistema: {dt_at}")
            print(f"📑 Total de Movimentos: {len(movs)}")
            print("📌 Últimas 15 Movimentações:")
            for m in movs_sorted[:15]:
                dt = m.get("dataHora", "")[:19].replace("T", " ")
                nm = m.get("nome", "")
                code = m.get("codigo", "")
                comps = m.get("complementosTabelados", [])
                comp_str = ""
                if comps:
                    comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")"
                print(f"   • {dt} — {nm}{comp_str} [Cód. {code}]")
                
            # Salvar JSON completo
            out_file = Path(r"c:\Projetos\superJus\Clientes\Leandro_Mecanico\datajud_live_02_09_2026.json")
            with open(out_file, "w", encoding="utf-8") as fp:
                json.dump(src, fp, indent=2, ensure_ascii=False)
            print(f"\n💾 Snapshot salvo em: {out_file}")
except Exception as e:
    print(f"Erro DataJud: {e}")

# 2. Busca por CPF no TJRJ e STJ para checar eventuais HCs distribuídos
print("\n" + "─" * 85)
print("🔍 Verificando se há Habeas Corpus distribuído no TJRJ ou STJ...")
payload_cpf = json.dumps({"query": {"match": {"dadosBasicos.polo.parte.pessoa.numeroDocumentoPrincipal": cpf}}, "size": 5}).encode("utf-8")
req_cpf = urllib.request.Request(url, data=payload_cpf, headers=HEADERS)
try:
    with urllib.request.urlopen(req_cpf, context=ctx, timeout=15) as resp:
        data_cpf = json.loads(resp.read().decode("utf-8"))
        hits_cpf = data_cpf.get("hits", {}).get("hits", [])
        print(f"Processos vinculados ao CPF no TJRJ: {len(hits_cpf)}")
        for h in hits_cpf:
            s = h["_source"]
            print(f" • {s.get('numeroProcesso')} | {s.get('orgaoJulgador',{}).get('nome')} | {s.get('classe',{}).get('nome')}")
except Exception as e:
    print(f"Erro busca CPF: {e}")

print("\n" + "=" * 85)
print("✅ Varredura concluída.")
print("=" * 85)
