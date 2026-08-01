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
    
    real_frame = page.query_selector("iframe#mainframe").content_frame()
    
    # Procurar links no frame
    links = real_frame.query_selector_all("a")
    print(f"Total de links no frame: {len(links)}")
    for l in links:
        txt = l.inner_text().strip()
        print(f"  Link: '{txt}'")
        if "personagens" in txt.lower():
            print(">>> Clicando no link Personagens... <<<")
            l.click()
            time.sleep(4)
            break
            
    body_txt = real_frame.inner_text("body")
    print("=== TEXTO DOS PERSONAGENS DO PROCESSO 2017 ===")
    print(body_txt[:3500])
    
    out_file = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo\personagens_processo_2017.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(body_txt)
    print(f"Salvo em {out_file}")
    
    browser.close()
