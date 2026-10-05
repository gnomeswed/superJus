# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.parse
import sys

sys.stdout.reconfigure(encoding="utf-8")

cpf = "06429650723"
cpf_formatted = "064.296.507-23"

print("=== CONSULTANDO DIÁRIO DE JUSTIÇA ELETRÔNICO NACIONAL (DJEN) ===")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*"
}

urls = [
    f"https://comunicaapi.pje.jus.br/api/v1/comunicacao?numeroDocumentoPrincipal={cpf}",
    f"https://comunicaapi.pje.jus.br/api/v1/comunicacao?numeroDocumentoPrincipal={cpf_formatted}",
    f"https://comunicaapi.pje.jus.br/api/v1/comunicacao?texto={cpf}",
    f"https://comunicaapi.pje.jus.br/api/v1/comunicacao?texto={urllib.parse.quote(cpf_formatted)}"
]

for u in urls:
    print(f"URL: {u}")
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            items = data.get("items", [])
            print(f"  -> Itens encontrados: {len(items)}")
            for it in items:
                np = it.get("numero_processo")
                dest = it.get("destinatario")
                dt = it.get("data_disponibilizacao")
                trib = it.get("siglaTribunal")
                orgao = it.get("nomeOrgao")
                tipo = it.get("tipoComunicacao")
                txt = it.get("texto", "")[:200]
                print(f"  📌 Processo: {np} | Tribunal: {trib} | Destinatário: {dest} | Data: {dt}")
                print(f"     Órgão: {orgao} | Tipo: {tipo}")
                print(f"     Trecho: {txt}\n")
    except Exception as e:
        print(f"  Erro: {e}")
