# -*- coding: utf-8 -*-
import time
import os
from playwright.sync_api import sync_playwright

proc_num = "0000253-78.2017.8.19.0004"
hc_num = "0046418-98.2017.8.19.0000"

target_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print(f"1. Acessando processo {proc_num} no TJRJ...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
    time.sleep(3)
    
    frame = page.frame_locator("iframe#mainframe")
    frame.locator("input[name='numeroProcesso']").fill(proc_num)
    time.sleep(1)
    frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
    time.sleep(5)
    
    # Clicar em Todos Os Movimentos
    print("Clicando no botão 'Todos Os Movimentos'...")
    frame.locator("button:has-text('Todos Os Movimentos')").first.click()
    time.sleep(4)
    
    real_frame = page.query_selector("iframe#mainframe").content_frame()
    movs_text = real_frame.inner_text("body")
    
    print("=== TODOS OS MOVIMENTOS DO PROCESSO DE 2017 DA 2ª VARA CRIMINAL DE NITERÓI ===")
    print(movs_text[:3500])
    
    out_mov_file = os.path.join(target_dir, "todos_movimentos_processo_2017_lucas.txt")
    with open(out_mov_file, "w", encoding="utf-8") as f:
        f.write(movs_text)
        
    print(f"Salvo em {out_mov_file}")
    
    # 2. Consultar o HC 0046418-98.2017.8.19.0000 de 2ª Instância
    print(f"2. Acessando HC de 2ª Instância {hc_num}...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
    time.sleep(3)
    
    frame2 = page.frame_locator("iframe#mainframe")
    frame2.locator("input[name='numeroProcesso']").fill(hc_num)
    time.sleep(1)
    frame2.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
    time.sleep(5)
    
    real_frame2 = page.query_selector("iframe#mainframe").content_frame()
    hc_text = real_frame2.inner_text("body")
    
    print("=== TEXTO DO HABEAS CORPUS DE 2ª INSTÂNCIA ===")
    print(hc_text[:3500])
    
    out_hc_file = os.path.join(target_dir, "hc_2017_lucas_tjrj.txt")
    with open(out_hc_file, "w", encoding="utf-8") as f:
        f.write(hc_text)
        
    print(f"HC salvo em {out_hc_file}")
    browser.close()
