# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

proc_num = "0023013-51.2021.8.19.0078"
target_file = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\tjrj_live_check_now.txt"

print("Acessando TJRJ ao vivo em tempo real (domcontentloaded)...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=60000)
    time.sleep(4)
    
    frame = page.frame_locator("iframe#mainframe")
    frame.locator("input[name='numeroProcesso']").fill(proc_num)
    time.sleep(1)
    frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
    time.sleep(6)
    
    try:
        frame.locator("button:has-text('Todos Os Movimentos')").first.click()
        time.sleep(4)
    except Exception as e:
        print("Aviso ao clicar em Todos Os Movimentos:", e)
    
    real_frame = page.query_selector("iframe#mainframe").content_frame()
    movs_txt = real_frame.inner_text("body")
    
    print("=== MOVIMENTAÇÕES TJRJ AO VIVO ===")
    print(movs_txt[:4000])
    
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(movs_txt)
        
    browser.close()
