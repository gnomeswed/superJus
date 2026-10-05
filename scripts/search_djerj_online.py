# -*- coding: utf-8 -*-
import time
import os
from playwright.sync_api import sync_playwright

proc_num = "0023013-51.2021.8.19.0078"
proc_clean = "00230135120218190078"
target_file = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\djerj_online_search_29_07_2026.txt"

print("=== BUSCA DIRETA NO PORTAL DO DJERJ (29/07/2026 13h24) ===")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    # 1. Tentar portal de consulta DJERJ do TJRJ
    url_djerj = "https://www3.tjrj.jus.br/consultadjerj/consulta.aspx"
    print(f"Acessando {url_djerj}...")
    try:
        page.goto(url_djerj, timeout=30000)
        time.sleep(3)
        print("Página do DJERJ acessada com sucesso!")
        
        # Preencher pesquisa por número do processo ou nome
        proc_input = page.query_selector("input[id*='txtProcesso'], input[id*='Processo'], input[name*='Processo']")
        if proc_input:
            proc_input.fill(proc_num)
            time.sleep(1)
            btn = page.query_selector("input[type='submit'], button:has-text('Pesquisar'), input[value*='Pesquisar']")
            if btn:
                btn.click()
                time.sleep(5)
                
        body_txt = page.inner_text("body")
        print("Resultados obtidos no DJERJ:")
        print(body_txt[:3500])
        
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(body_txt)
    except Exception as e:
        print(f"Erro ao acessar {url_djerj}: {e}")
        
    browser.close()
