# -*- coding: utf-8 -*-
"""Extrai o código do handler jQuery do botão procBtnPesquisar"""
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
    page.click("#abas-processo-tab")
    time.sleep(2)
    code = page.evaluate("""() => {
        const btn = document.querySelector('#procBtnPesquisar');
        const ev = jQuery._data(btn, 'events');
        if (!ev || !ev.click) return 'no handlers';
        return ev.click.map(h => h.handler.toString()).join('\\n\\n---\\n\\n');
    }""")
    print("=== HANDLER JQUERY DO BOTÃO ===")
    print(code[:6000])
    browser.close()
