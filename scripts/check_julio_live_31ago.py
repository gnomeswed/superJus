# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.parse
import sys
import os
import time

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

print("================================================================================")
print("=== VERIFICAÇÃO ONLINE AO VIVO — JÚLIO PEREIRA MARCOS (31/08/2026) ===")
print("================================================================================")

# 1. CONSULTA STJ OFICIAL (HC 1.116.750 / RJ)
print("\n1. Consultando STJ (HC 1.116.750/RJ - Reg. 2026/0311210-7)...")
url_stj = "https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}
q_stj = {"query": {"match": {"numeroProcesso": "03112101020263000000"}}}

stj_status = {}
try:
    req = urllib.request.Request(url_stj, data=json.dumps(q_stj).encode("utf-8"), headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        hits = data.get("hits", {}).get("hits", [])
        if hits:
            src = hits[0]["_source"]
            movs = src.get("movimentos", [])
            movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
            last_dt = src.get("dataHoraUltimaAtualizacao")
            orgao = src.get("orgaoJulgador", {}).get("nome")
            
            print(f"   • Processo: HC 1.116.750 / RJ (Único: 0311210-10.2026.3.00.0000)")
            print(f"   • Órgão: {orgao}")
            print(f"   • Total de Movimentações Registradas: {len(movs)}")
            print(f"   • Última Atualização no Sistema: {last_dt}")
            print("   • Últimos 5 Movimentos:")
            for m in movs_sorted[:5]:
                dt = m.get("dataHora", "")[:19].replace("T", " ")
                comps = m.get("complementosTabelados", [])
                comp_str = " | ".join([f"{c.get('descricao')}: {c.get('nome')}" for c in comps])
                print(f"     -> [{dt}] {m.get('nome')} (Cód. {m.get('codigo')})" + (f" - {comp_str}" if comp_str else ""))
                
            stj_status = {
                "processo": "HC 1.116.750 / RJ",
                "orgao": orgao,
                "total_movimentos": len(movs),
                "ultima_atualizacao": last_dt,
                "ultimos_movimentos": movs_sorted[:5]
            }
except Exception as e:
    print(f"   ❌ Erro ao consultar STJ: {e}")

# 2. CONSULTA TJRJ (1ª INSTÂNCIA - BÚZIOS & 2ª INSTÂNCIA)
print("\n2. Consultando TJRJ...")
url_tjrj = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
procs_tjrj = [
    ("0023013-51.2021.8.19.0078", "00230135120218190078", "Ação Penal Desmembrada - 2ª Vara Búzios"),
    ("0001140-87.2024.8.19.0078", "00011408720248190078", "Apenso RSE - 2ª Vara Búzios"),
    ("0022975-39.2021.8.19.0078", "00229753920218190078", "Ação Originária Corréus - 2ª Vara Búzios"),
    ("0029845-67.2026.8.19.0000", "00298456720268190000", "HC 7ª Câmara Criminal TJRJ")
]

tjrj_status = {}
for cnj, clean, desc in procs_tjrj:
    q = {"query": {"match": {"numeroProcesso": clean}}}
    try:
        req = urllib.request.Request(url_tjrj, data=json.dumps(q).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"   • [{cnj}] ({desc}): {len(hits)} hit(s)")
            if hits:
                src = hits[0]["_source"]
                movs = src.get("movimentos", [])
                movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
                print(f"     -> Total movs: {len(movs)} | Último: {movs_sorted[0].get('dataHora')} - {movs_sorted[0].get('nome') if movs_sorted else ''}")
                tjrj_status[cnj] = {
                    "total_movimentos": len(movs),
                    "ultimo_movimento": movs_sorted[0] if movs_sorted else {}
                }
    except Exception as e:
        print(f"   ❌ Erro ao consultar {cnj}: {e}")

out_report = {
    "data_verificacao": "31/08/2026 13:58",
    "stj": stj_status,
    "tjrj": tjrj_status
}

out_file = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\07_RELATORIOS_ESTRATEGICOS_E_ANALISES\andamento_julio_31_08_2026.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(out_report, f, ensure_ascii=False, indent=2)

print("\n" + "="*80)
print(f"✅ Varredura ao vivo concluída com sucesso! Relatório gerado em: {out_file}")
print("="*80)
