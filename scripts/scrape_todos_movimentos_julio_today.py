# -*- coding: utf-8 -*-
import os
import sys
import time
import logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
sys.stdout.reconfigure(encoding="utf-8")

proc_num = "0023013-51.2021.8.19.0078"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    url_portal = "https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica"
    page.goto(url_portal, timeout=30000, wait_until="domcontentloaded")
    time.sleep(3)
    
    iframe_el = page.wait_for_selector("iframe#mainframe", timeout=15000)
    if iframe_el:
        frame = iframe_el.content_frame()
        if frame:
            frame.query_selector("input[name='numeroProcesso']").fill(proc_num)
            btns = frame.query_selector_all("button")
            btn = [b for b in btns if any(w in b.inner_text().lower() for w in ["pesquisar", "buscar", "consultar"])][0]
            btn.click()
            time.sleep(5)
            
            # Clicar em 'Todos Os Movimentos'
            link_movs = frame.query_selector("a:has-text('Todos Os Movimentos'), button:has-text('Todos Os Movimentos')")
            if link_movs:
                logging.info("Clicando em Todos Os Movimentos...")
                link_movs.click()
                time.sleep(4)
                
            txt_all = frame.inner_text("body")
            print("\n=== TODOS OS MOVIMENTOS HOJE (07/08/2026) ===")
            print(txt_all[:4000])
            
            with open("julio_todos_movimentos_07_08_2026.txt", "w", encoding="utf-8") as f:
                f.write(txt_all)

    browser.close()
