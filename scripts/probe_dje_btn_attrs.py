# -*- coding: utf-8 -*-
"""Inspeciona atributos do botão procBtnPesquisar e HTML da aba Processo"""
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
    info = page.evaluate("""() => {
        const btn = document.querySelector('#procBtnPesquisar');
        const attrs = {};
        for (const a of btn.attributes) attrs[a.name] = a.value;
        // eventos jquery
        const ev = jQuery ? (jQuery._data(btn, 'events') || {}) : {};
        const evNames = Object.keys(ev);
        // html da aba
        const aba = document.querySelector('#pills-processo');
        return {
            attrs: attrs,
            evNames: evNames,
            abaHtml: aba ? aba.outerHTML.slice(0, 2500) : 'no #pills-processo'
        };
    }""")
    print("=== ATRIBUTOS BOTÃO ===")
    for k, v in info["attrs"].items():
        print(f"  {k}={v}")
    print("=== EVENTOS JQUERY ===")
    print(info["evNames"])
    print("=== HTML ABA PROCESSO ===")
    print(info["abaHtml"])
    browser.close()
