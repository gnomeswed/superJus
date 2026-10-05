# -*- coding: utf-8 -*-
"""Inspeciona estrutura do portal DJERJ novo para achar a aba de busca por processo"""
import time, sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1366, "height": 900},
                              user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    page.goto("https://www3.tjrj.jus.br/consultadje/", wait_until="domcontentloaded", timeout=45000)
    time.sleep(6)
    # tabs/abas
    tabs = page.evaluate("""Array.from(document.querySelectorAll('a, button, li, .nav-link, .tab')).map(e => ({
        tag: e.tagName, id: e.id||'', cls: (e.className||'').toString().slice(0,50),
        txt: (e.textContent||'').trim().slice(0,60), href: e.getAttribute('href')||''
    })).filter(x => x.txt && x.txt.length > 1).slice(0, 80)""")
    for t in tabs:
        print(t)
    browser.close()
