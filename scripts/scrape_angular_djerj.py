# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Acessando https://www3.tjrj.jus.br/consultaprocessual/#/consultadjerj...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultadjerj", timeout=30000)
    time.sleep(4)
    
    print("Inner text da página Angular DJERJ:")
    print(page.inner_text("body")[:2000])
    
    frame = page.frame_locator("iframe#mainframe")
    try:
        frame_text = frame.locator("body").inner_text()
        print("\nInner text do iframe#mainframe:")
        print(frame_text[:2000])
    except Exception as e:
        print(f"Erro no iframe: {e}")
        
    browser.close()
