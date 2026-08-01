# -*- coding: utf-8 -*-
import time
import os
from playwright.sync_api import sync_playwright

target_file = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\djerj_online_exact_results.txt"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Acessando portal principal do TJRJ para localizar a busca do DJERJ...")
    page.goto("https://www3.tjrj.jus.br/consultadjerj/", timeout=35000)
    time.sleep(4)
    
    # Imprimir URL final e formulários
    print("URL Final:", page.url)
    inputs = page.query_selector_all("input")
    print(f"Total de campos de busca encontrados: {len(inputs)}")
    
    body_text = page.inner_text("body")
    print("Conteúdo da página do DJERJ:")
    print(body_text[:2000])
    
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(f"URL: {page.url}\n\n" + body_text)
        
    browser.close()
