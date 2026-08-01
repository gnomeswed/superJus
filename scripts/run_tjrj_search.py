# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://www3.tjrj.jus.br/consultaprocessual/#/conspublica', timeout=30000)
    time.sleep(3)
    page.click('text=Por Nome')
    time.sleep(2)
    inputs = page.query_selector_all('input')
    for i in inputs:
        ph = i.get_attribute('placeholder') or ''
        nm = i.get_attribute('name') or ''
        if 'nome' in ph.lower() or 'nome' in nm.lower():
            print(f'Input achado: ph="{ph}", nm="{nm}"')
            i.fill('LUCAS DE SOUZA FREITAS')
            break
            
    page.click('button:has-text("Pesquisar")')
    time.sleep(8)
    txt = page.inner_text('body')
    print(f'Tamanho do texto extraído: {len(txt)}')
    
    out_file = r"C:\Projetos\Super Analista Jurídico\tjrj_lucas_search_output.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(txt)
    print(f"Salvo em {out_file}")
    browser.close()
