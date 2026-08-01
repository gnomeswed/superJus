# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Acessando TJRJ conspublica...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
    time.sleep(4)
    
    frame = page.frame_locator("iframe#mainframe")
    
    print("1. Clicando no tab #nav-porNome...")
    frame.locator("#nav-porNome").click()
    time.sleep(2)
    
    # Inspecionar todo o HTML do pane #porNome ou do frame
    html_content = page.query_selector("iframe#mainframe").content_frame().inner_html("#porNome")
    print(f"HTML de #porNome ({len(html_content)} caracteres):")
    print(html_content[:2000])
    
    out_file = r"C:\Projetos\Super Analista Jurídico\por_nome_pane.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Salvo em {out_file}")
    
    browser.close()
