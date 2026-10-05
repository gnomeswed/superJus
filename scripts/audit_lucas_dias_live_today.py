# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.parse
import sys
import time
import os

sys.stdout.reconfigure(encoding="utf-8")

print("================================================================================")
print("🔍 ATUALIZAÇÃO ONLINE EM TEMPO REAL — LUCAS DIAS OLIVEIRA (DATA: 05/09/2026)")
print("================================================================================\n")

DATAJUD_KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

def check_datajud_proc(proc_clean):
    print("--- [1] CONSULTANDO DATAJUD CNJ (TJRJ) PELO NÚMERO DO PROCESSO ---")
    url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
    headers = {
        "Authorization": DATAJUD_KEY,
        "Content-Type": "application/json"
    }
    payload = json.dumps({"query": {"match": {"numeroProcesso": proc_clean}}, "size": 10}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"Total de registros encontrados: {len(hits)}")
            for hit in hits:
                src = hit["_source"]
                print(f"• Processo: {src.get('numeroProcesso')}")
                print(f"  Grau: {src.get('grau')}")
                print(f"  Órgão: {src.get('orgaoJulgador', {}).get('nome')}")
                print(f"  Última Atualização no Banco: {src.get('dataHoraUltimaAtualizacao')}")
                movs = src.get("movimentos", [])
                print(f"  Total de Movimentos: {len(movs)}")
                movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
                print("  Top 10 Movimentações mais recentes:")
                for i, m in enumerate(movs_sorted[:10], start=1):
                    dt = m.get("dataHora", "")[:19].replace("T", " ")
                    nome = m.get("nome", "")
                    code = m.get("codigo", "")
                    comps = m.get("complementosTabelados", [])
                    comp_str = ""
                    if comps:
                        comp_str = " -> " + " | ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps])
                    print(f"    {i:02d}. {dt} | {nome}{comp_str} [Cód: {code}]")
    except Exception as e:
        print(f"Erro DataJud: {e}")

def check_djen(termo):
    print(f"\n--- [2] CONSULTANDO DIÁRIO DA JUSTIÇA ELETRÔNICO NACIONAL (DJEN) PARA '{termo}' ---")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json, text/plain, */*"
    }
    url = f"https://comunicaapi.pje.jus.br/api/v1/comunicacao?texto={urllib.parse.quote(termo)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            items = data.get("items", [])
            print(f"Publicações encontradas no DJEN: {len(items)}")
            for it in items[:10]:
                dt_disp = it.get("data_disponibilizacao")
                tribunal = it.get("siglaTribunal")
                orgao = it.get("nomeOrgao")
                tipo = it.get("tipoComunicacao")
                numero_proc = it.get("numero_processo")
                print(f"  📌 [{dt_disp}] {tribunal} - {orgao} | Proc: {numero_proc} ({tipo})")
                texto = it.get("texto", "")
                resumo = " ".join(texto.split())[:350]
                print(f"     Trecho: {resumo}...\n")
    except Exception as e:
        print(f"Erro DJEN: {e}")

def check_stj(termo):
    print(f"\n--- [3] CONSULTANDO DATAJUD STJ PARA '{termo}' ---")
    url = "https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search"
    headers = {
        "Authorization": DATAJUD_KEY,
        "Content-Type": "application/json"
    }
    payload = json.dumps({"query": {"match_phrase": {"pessoas.nome": termo}}, "size": 10}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"Processos no STJ em nome de '{termo}': {len(hits)}")
            for hit in hits:
                src = hit["_source"]
                print(f"  • STJ Processo: {src.get('numeroProcesso')} - {src.get('classe', {}).get('nome')}")
    except Exception as e:
        print(f"Erro STJ: {e}")

check_datajud_proc("08085953620268190002")
check_djen("0808595-36.2026.8.19.0002")
check_djen("Lucas Dias Oliveira")
check_stj("Lucas Dias Oliveira")

