# -*- coding: utf-8 -*-
"""Busca no novo portal DJERJ (consultadje) por publicações do processo 0023013-51.2021.8.19.0078"""
import time, sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')

PROC = "0023013-51.2021.8.19.0078"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1366, "height": 900},
                              user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    try:
        page.goto("https://www3.tjrj.jus.br/consultadje/", wait_until="domcontentloaded", timeout=45000)
        time.sleep(6)
        print("=== TITULO ===")
        print(await_title := page.title())
        print("=== BODY (início) ===")
        body = page.evaluate("document.body.innerText")
        print(body[:2000])
        # lista de inputs
        inputs = page.evaluate("Array.from(document.querySelectorAll('input, select, button')).map(e => (e.tagName+'|'+(e.name||e.id||'')+'|'+(e.textContent||'').trim()).slice(0,90))")
        print("=== INPUTS ===")
        for i in inputs[:40]:
            print(" ", i)
    except Exception as e:
        print(f"Erro: {e}")
    browser.close()
