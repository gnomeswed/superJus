# -*- coding: utf-8 -*-
import time
import json
import urllib.request
import urllib.parse
import sys
import os
import re
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

target_dir = r"c:\Projetos\superJus\Clientes\Rodrigo_Nobrega"

processos = [
    ("0800060-52.2023.8.19.0058", "Saquarema 1 - Roubo Majorado"),
    ("0800262-29.2023.8.19.0058", "Saquarema 2 - Roubo e Flagrante"),
    ("0801082-93.2023.8.19.0043", "Piraí - Roubo Majorado"),
    ("0809172-80.2023.8.19.0014", "Campos - Tráfico e Armas")
]

print("=== EXTRAINDO SENTENÇAS E ACÓRDÃOS DO TJRJ ===")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 900}
    )
    page = context.new_page()

    for np, desc in processos:
        print(f"\n--- Consultando {np} ({desc}) ---")
        p_dir = os.path.join(target_dir, "processos", np, "sentencas_e_acordaos")
        os.makedirs(p_dir, exist_ok=True)
        
        # Consultar portal de jurisprudência
        url_busca = f"https://www3.tjrj.jus.br/jurisprudencia/#/pesquisa-livre?termo={np}"
        try:
            page.goto(url_busca, wait_until="domcontentloaded", timeout=25000)
            time.sleep(4)
            
            txt_jur = page.inner_text("body")
            page.screenshot(path=os.path.join(p_dir, "resultado_jurisprudencia.png"))
            
            with open(os.path.join(p_dir, "jurisprudencia_acordao.txt"), "w", encoding="utf-8") as f:
                f.write(txt_jur)
                
            print(f"  • Jurisprudência capturada ({len(txt_jur)} chars)")
            lines = [l.strip() for l in txt_jur.splitlines() if l.strip()]
            for l in lines[:15]:
                print(f"    -> {l[:110]}")
        except Exception as e:
            print(f"  ❌ Erro ao consultar {np}: {e}")

    browser.close()

print("\n=== CONCLUÍDO ===")
