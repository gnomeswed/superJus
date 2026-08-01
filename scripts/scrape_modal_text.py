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
    print("Clicando em 'Listar todos os personagens'...")
    frame.locator("text=Listar todos os personagens").click()
    time.sleep(3)
    
    real_frame = page.query_selector("iframe#mainframe").content_frame()
    
    # Extrair texto do modal
    modal_el = real_frame.query_selector(".modal-content, .modal-body, div[role='dialog']")
    if modal_el:
        modal_txt = modal_el.inner_text()
        print("=== CONTEÚDO ENCONTRADO NO MODAL DE PERSONAGENS ===")
        print(modal_txt)
    else:
        modal_txt = real_frame.inner_text("body")
        print("=== BODY TEXT APÓS ABRIR MODAL ===")
        print(modal_txt)
        
    out_file = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo\qualificacao_modal_lucas_2017.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(modal_txt)
        
    print(f"Salvo em {out_file}")
    
    # Fechar modal
    try:
        real_frame.click(".modal-header button, button.close, text=Fechar")
        time.sleep(2)
    except Exception:
        pass
        
    # Clicar em Todos os Movimentos
    print("Clicando em 'Todos Os Movimentos'...")
    frame.locator("text=Todos Os Movimentos").click()
    time.sleep(4)
    
    # Extrair texto do modal de movimentos
    modal_mov_el = real_frame.query_selector(".modal-content, .modal-body, div[role='dialog']")
    if modal_mov_el:
        mov_txt = modal_mov_el.inner_text()
    else:
        mov_txt = real_frame.inner_text("body")
        
    out_mov_file = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo\todos_movimentos_lucas_2017.txt"
    with open(out_mov_file, "w", encoding="utf-8") as f:
        f.write(mov_txt)
        
    print(f"Movimentos salvos em {out_mov_file}")
    browser.close()
