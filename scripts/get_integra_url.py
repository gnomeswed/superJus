# -*- coding: utf-8 -*-
import time
import os
from playwright.sync_api import sync_playwright

hc_num = "0046418-98.2017.8.19.0000"
target_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print(f"Acessando Habeas Corpus {hc_num} no TJRJ...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
    time.sleep(4)
    
    frame = page.frame_locator("iframe#mainframe")
    frame.locator("input[name='numeroProcesso']").fill(hc_num)
    time.sleep(1)
    frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
    time.sleep(6)
    
    real_frame = page.query_selector("iframe#mainframe").content_frame()
    
    # Inspecionar todos os links de inteiro teor
    links = real_frame.query_selector_all("a:has-text('Íntegra')")
    print(f"Total de links de Íntegra encontrados: {len(links)}")
    for l in links:
        href = l.get_attribute("href")
        onclick = l.get_attribute("onclick")
        txt = l.inner_text().strip()
        print(f"  Link: '{txt}' | href='{href}' | onclick='{onclick}'")
        
        # Clicar no link e esperar 4s
        l.click()
        time.sleep(4)
        
    # Verificar se abriu abas ou se mudou o conteúdo do frame
    all_pages = ctx.pages
    print(f"Total de abas abertas no navegador: {len(all_pages)}")
    for idx, p_item in enumerate(all_pages):
        print(f"--- Aba {idx}: {p_item.url} ---")
        p_txt = p_item.inner_text("body")
        print(p_txt[:2000])
        out_f = os.path.join(target_dir, f"integra_aba_{idx}.txt")
        with open(out_f, "w", encoding="utf-8") as f:
            f.write(p_txt)
            
    browser.close()
