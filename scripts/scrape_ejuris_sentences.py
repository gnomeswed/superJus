# -*- coding: utf-8 -*-
import time
import os
import sys
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

target_dir = r"c:\Projetos\superJus\Clientes\Rodrigo_Nobrega"

processos = [
    ("0800060-52.2023.8.19.0058", "Saquarema 1 - Roubo Majorado"),
    ("0800262-29.2023.8.19.0058", "Saquarema 2 - Flagrante e Roubo"),
    ("0801082-93.2023.8.19.0043", "Piraí - Roubo Majorado"),
    ("0809172-80.2023.8.19.0014", "Campos - Tráfico")
]

print("=== CONSULTANDO E-JURIS DO TJRJ (ACÓRDÃOS E EMENTAS) ===")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 900}
    )
    page = context.new_page()

    for np, desc in processos:
        print(f"\n--- Buscando no E-JURIS: {np} ({desc}) ---")
        p_dir = os.path.join(target_dir, "processos", np, "sentencas_e_acordaos")
        os.makedirs(p_dir, exist_ok=True)
        
        url_ejuris = "http://www4.tjrj.jus.br/EJURIS/ConsultarJurisprudencia.aspx"
        try:
            page.goto(url_ejuris, wait_until="domcontentloaded", timeout=25000)
            time.sleep(2)
            
            # Preencher campo de texto livre com o número do processo
            inp = page.query_selector("input[id*='txtTextoPesquisa'], input[name*='txtTextoPesquisa'], input[type='text']")
            if inp:
                inp.fill(np)
                time.sleep(1)
                
            btn = page.query_selector("input[id*='btnPesquisar'], input[value*='Pesquisar'], button:has-text('Pesquisar')")
            if btn:
                btn.click()
                time.sleep(6)
                
            ejuris_txt = page.inner_text("body")
            page.screenshot(path=os.path.join(p_dir, "ejuris_resultado.png"))
            
            with open(os.path.join(p_dir, "acordao_ejuris_integra.txt"), "w", encoding="utf-8") as f:
                f.write(ejuris_txt)
                
            print(f"  • Resultado E-JURIS capturado ({len(ejuris_txt)} caracteres)")
            for l in [line.strip() for line in ejuris_txt.splitlines() if line.strip()][:20]:
                print(f"    [E-JURIS] {l[:120]}")
                
        except Exception as e:
            print(f"  ❌ Erro E-JURIS em {np}: {e}")

    browser.close()

print("\n=== CONSULTA E-JURIS CONCLUÍDA ===")
