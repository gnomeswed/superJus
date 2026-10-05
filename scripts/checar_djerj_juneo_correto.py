# -*- coding: utf-8 -*-
"""
SUPERJUS — CHECAGEM CORRETA NO DJERJ / TJRJ PARA PASTOR JUNEO
"""

import sys, time, json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

proc_fmt = "0810659-95.2026.8.19.0203"
nome = "Juneo Luciano de Oliveira"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 1280, "height": 900})

    print("1. Acessando https://www3.tjrj.jus.br/consultaprocessual/#/consultadjerj...")
    try:
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultadjerj", timeout=30000)
        time.sleep(5)
        
        # Procurar campos no frame_locator("iframe#mainframe")
        frame = page.frame_locator("iframe#mainframe")
        
        print("Preenchendo processo no DJERJ...")
        inp_proc = frame.locator("input[id*='txtProcesso'], input[name*='Processo'], input[id*='Processo']").first
        if inp_proc.is_visible():
            inp_proc.fill(proc_fmt)
            time.sleep(1)
            btn = frame.locator("input[type='submit'], button:has-text('Pesquisar'), input[value*='Pesquisar']").first
            if btn.is_visible():
                btn.click()
                time.sleep(6)
                
            res_txt = frame.locator("body").inner_text()
            print("--- RESULTADO DJERJ PROCESSO ---")
            print(res_txt[:3000])
        else:
            print("Campo txtProcesso não visível no frame.")
            print(frame.locator("body").inner_text()[:1000])
            
    except Exception as e:
        print(f"Erro DJERJ: {e}")

    browser.close()
