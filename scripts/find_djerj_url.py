# -*- coding: utf-8 -*-
import time
import os
from playwright.sync_api import sync_playwright

proc_num = "0023013-51.2021.8.19.0078"
target_file = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\djerj_search_portal_out.txt"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    # Acessar a busca do DJERJ através da consulta pública do TJRJ
    print("Acessando consulta processual do TJRJ para verificar atalho do DJERJ...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
    time.sleep(3)
    
    frame = page.frame_locator("iframe#mainframe")
    frame.locator("input[name='numeroProcesso']").fill(proc_num)
    time.sleep(1)
    frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
    time.sleep(5)
    
    # Verificar se o link de publicações/DJERJ está presente no espelho
    real_frame = page.query_selector("iframe#mainframe").content_frame()
    
    # Tentar clicar em Publicações ou DJERJ se houver
    pub_links = real_frame.query_selector_all("a:has-text('Publicação'), a:has-text('DJERJ'), a:has-text('Diário')")
    print(f"Links de publicação/DJERJ encontrados na página do processo: {len(pub_links)}")
    for link in pub_links:
        print("  - Link text:", link.inner_text(), " | href:", link.get_attribute("href"))
        
    full_text = real_frame.inner_text("body")
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(full_text)
        
    print(f"Resultado salvo em {target_file}")
    browser.close()
