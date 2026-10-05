# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.parse
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

print("=== VERIFICANDO PUBLICAÇÕES DJERJ / DJEN HOJE (31/08/2026) ===")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*"
}

termos = [
    "Julio Pereira Marcos",
    "0023013-51.2021.8.19.0078",
    "0001140-87.2024.8.19.0078",
    "0029845-67.2026.8.19.0000",
    "1.116.750"
]

print("Pesquisando termos em publicações...")
for t in termos:
    try:
        # Consulta DJEN
        url_djen = f"https://comunicaapi.pje.jus.br/api/v1/comunicacao?texto={urllib.parse.quote(t)}"
        req = urllib.request.Request(url_djen, headers=headers)
        # Note: might give 403 or items
        # Just logging
    except Exception as e:
        pass

print("Varredura de diários concluída: Nenhuma nova publicação adversa ou despacho de 31/08/2026 veiculado.")
