# -*- coding: utf-8 -*-
"""
SUPERJUS — CONSULTA AO VIVO TJMS: PROCESSO 0842165-16.2026.8.12.0001 (JOSÉ)
Tribunal de Justiça do Estado de Mato Grosso do Sul (Comarca de Campo Grande)
"""

import sys, os, json, ssl, urllib.request
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

DATAJUD_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {
    'Authorization': f"APIKey {DATAJUD_KEY}",
    'Content-Type': 'application/json'
}

PROC_CLEAN = "08421651620268120001"
PROC_FMT = "0842165-16.2026.8.12.0001"

print("=" * 85)
print(f"🔍 CONSULTA DATAJUD TJMS — PROCESSO {PROC_FMT}")
print(f"🏛️ Tribunal: TJMS (Mato Grosso do Sul — Campo Grande)")
print(f"⏰ Consulta: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
print("=" * 85)

ctx = ssl._create_unverified_context()
url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjms/_search"

payload = {
    "query": {
        "match": {
            "numeroProcesso": PROC_CLEAN
        }
    },
    "size": 5
}

req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=HEADERS)

try:
    with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        hits = data.get("hits", {}).get("hits", [])
        print(f"Total de registros encontrados no TJMS: {len(hits)}")
        
        if hits:
            src = hits[0]["_source"]
            np = src.get("numeroProcesso", "N/I")
            orgao = src.get("orgaoJulgador", {}).get("nome", "N/I")
            classe = src.get("classe", {}).get("nome", "N/I")
            dt_aj = src.get("dataAjuizamento", "N/I")
            dt_at = src.get("dataHoraUltimaAtualizacao", "N/I")
            assuntos = [a.get("nome", "") for a in src.get("assuntos", [])]
            
            # Polos
            polos = src.get("dadosBasicos", {}).get("polo", [])
            partes_str = []
            for p in polos:
                pol = p.get("polo", "")
                for part in p.get("parte", []):
                    pess = part.get("pessoa", {})
                    n = pess.get("nome", "")
                    doc = pess.get("numeroDocumentoPrincipal", "")
                    partes_str.append(f"{pol}: {n} (Doc: {doc})")
                    
            movs = src.get("movimentos", [])
            movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
            
            print(f"\n📂 Processo: {np}")
            print(f"   🏛️ Órgão Julgador: {orgao}")
            print(f"   📋 Classe: {classe}")
            print(f"   📅 Ajuizamento: {dt_aj} | Última Atualização: {dt_at}")
            print(f"   📌 Assuntos: {', '.join(assuntos)}")
            print(f"   👥 Partes: {', '.join(partes_str)}")
            print(f"\n📑 TOTAL DE MOVIMENTAÇÕES: {len(movs)}")
            print("📜 HISTÓRICO COMPLETO DE MOVIMENTAÇÕES (Mais Recentes Primeiro):")
            
            audiencias = []
            for m in movs_sorted:
                dt = m.get("dataHora", "")[:19].replace("T", " ")
                nm = m.get("nome", "")
                comps = m.get("complementosTabelados", [])
                comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")" if comps else ""
                print(f"   • {dt} — {nm}{comp_str} [Cód. {m.get('codigo')}]")
                if "audiência" in nm.lower() or "audiencia" in nm.lower():
                    audiencias.append((dt, nm, comp_str))
                    
            if audiencias:
                print("\n" + "─" * 60)
                print("🎯 MOVIMENTAÇÕES ESPECÍFICAS DE AUDIÊNCIA ENCONTRADAS:")
                for dt, nm, cs in audiencias:
                    print(f"   ⭐ {dt} — {nm}{cs}")
                print("─" * 60)
            else:
                print("\n⚠️ Nenhuma movimentação com termo 'audiência' encontrada nos registros.")
                
            # Salvar JSON
            out_file = Path(r"c:\Projetos\superJus\Clientes\processo_tjms_jose.json")
            with open(out_file, "w", encoding="utf-8") as fp:
                json.dump(src, fp, indent=2, ensure_ascii=False)
            print(f"\n💾 Arquivo bruto salvo em: {out_file}")
        else:
            print("⚠️ Nenhum registro retornado para este número no DataJud TJMS.")
            
except Exception as e:
    print(f"❌ Erro ao consultar DataJud TJMS: {e}")

print("\n" + "=" * 85)
