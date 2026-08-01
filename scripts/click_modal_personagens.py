# -*- coding: utf-8 -*-
import time
import os
from playwright.sync_api import sync_playwright

proc_num = "0000253-78.2017.8.19.0004"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print(f"Acessando processo {proc_num}...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
    time.sleep(3)
    
    frame = page.frame_locator("iframe#mainframe")
    frame.locator("input[name='numeroProcesso']").fill(proc_num)
    time.sleep(1)
    frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
    time.sleep(5)
    
    # Clicar em Listar todos os personagens
    print("Clicando no elemento 'Listar todos os personagens'...")
    frame.locator("text=Listar todos os personagens").click()
    time.sleep(3)
    
    real_frame = page.query_selector("iframe#mainframe").content_frame()
    
    # Tirar screenshot
    page.screenshot(path="personagens_modal.png")
    
    txt_modal = real_frame.inner_text("body")
    print("=== DADOS DO MODAL DE PERSONAGENS ===")
    print(txt_modal)
    
    # Clicar em Todos os Movimentos
    print("Clicando no elemento 'Todos Os Movimentos'...")
    frame.locator("text=Todos Os Movimentos").click()
    time.sleep(4)
    
    txt_movs = real_frame.inner_text("body")
    print("=== DADOS DE TODOS OS MOVIMENTOS ===")
    print(txt_movs[:3500])
    
    out_file = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo\movimentos_e_personagens_2017.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("=== PERSONAGENS ===\n" + txt_modal + "\n\n=== MOVIMENTOS ===\n" + txt_movs)
        
    print(f"Salvo em {out_file}")
    browser.close()
