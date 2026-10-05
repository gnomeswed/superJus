# -*- coding: utf-8 -*-
"""Probe: estado DOM da aba Processo no consultadje"""
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
    page.evaluate("document.querySelector('#abas-processo-tab').click()")
    time.sleep(3)
    info = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button, input[type=submit], input[type=button], a.btn'))
            .filter(b => b.offsetParent !== null)
            .map(b => ({tag: b.tagName, name: b.name||'', id: b.id||'', txt: (b.textContent||b.value||'').trim().slice(0,30), type: b.type||''}));
        const inputs = Array.from(document.querySelectorAll('#pills-processo input, #pills-processo select'))
            .map(i => ({name: i.name||'', id: i.id||'', vis: i.offsetParent !== null, type: i.type||''}));
        return {btns, inputs};
    }""")
    print("=== BOTÕES VISÍVEIS ===")
    for b in info["btns"]:
        print(b)
    print("=== INPUTS ABA PROCESSO ===")
    for i in info["inputs"]:
        print(i)
    browser.close()
