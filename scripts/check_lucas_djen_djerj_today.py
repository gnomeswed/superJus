# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.parse
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

print("=== VERIFICANDO PUBLICAÇÕES NO DJEN / DJERJ PARA LUCAS MOTOBOY ===")

nproc = "0011857-95.2024.8.19.0002"
clean_proc = "00118579520248190002"
nome = "Lucas de Souza Freitas"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*"
}

termos = [nproc, clean_proc, nome]

for t in termos:
    print(f"\nConsultando termo: '{t}'...")
    try:
        url = f"https://comunicaapi.pje.jus.br/api/v1/comunicacao?texto={urllib.parse.quote(t)}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            items = data.get("items", [])
            print(f"  -> Itens encontrados: {len(items)}")
            for it in items[:5]:
                dt_disp = it.get("data_disponibilizacao")
                tribunal = it.get("siglaTribunal")
                orgao = it.get("nomeOrgao")
                tipo = it.get("tipoComunicacao")
                print(f"  📌 [{dt_disp}] {tribunal} - {orgao} ({tipo})")
                texto = it.get("texto", "")
                print(f"     Trecho: {texto[:200]}...\n")
    except Exception as e:
        print(f"  Erro: {e}")

print("\n=== CONSULTA DE DIÁRIOS CONCLUÍDA ===")
