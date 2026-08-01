# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Acessando a home do TJRJ (https://www.tjrj.jus.br)...")
    page.goto("https://www.tjrj.jus.br", timeout=35000)
    time.sleep(4)
    
    links = page.query_selector_all("a")
    print(f"Total de links na home do TJRJ: {len(links)}")
    
    djerj_links = []
    for a in links:
        href = a.get_attribute("href") or ""
        txt = a.inner_text().strip()
        if "diario" in href.lower() or "djerj" in href.lower() or "diário" in txt.lower() or "djerj" in txt.lower():
            djerj_links.append((txt, href))
            
    print("\nLinks relacionados ao Diário Oficial / DJERJ na home do TJRJ:")
    for txt, href in djerj_links:
        print(f" - {txt} => {href}")
        
    browser.close()
