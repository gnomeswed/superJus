# -*- coding: utf-8 -*-
import time
import os
from playwright.sync_api import sync_playwright

proc_num = "0023013-51.2021.8.19.0078"
target_file = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\julio_tjrj_live_direct.txt"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print(f"Acessando processo do Júlio ({proc_num}) no TJRJ...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
    time.sleep(3)
    
    frame = page.frame_locator("iframe#mainframe")
    frame.locator("input[name='numeroProcesso']").fill(proc_num)
    time.sleep(1)
    frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
    time.sleep(6)
    
    real_frame = page.query_selector("iframe#mainframe").content_frame()
    tjrj_txt = real_frame.inner_text("body")
    
    print("=== ESPELHO DO PROCESSO DO JÚLIO PEREIRA MARCOS NO TJRJ ===")
    print(tjrj_txt[:3500])
    
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(tjrj_txt)
        
    print(f"Salvo em {target_file}")
    browser.close()
