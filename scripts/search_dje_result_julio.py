# -*- coding: utf-8 -*-
"""DJERJ Result.aspx — busca direta por processo — 13/08/2026"""
import time, sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')

PROC = "0023013-51.2021.8.19.0078"
DT_INI = "04/08/2026"
DT_FIM = "13/08/2026"

url = (f"https://www3.tjrj.jus.br/consultadje/Result.aspx"
       f"?dtInicio={DT_INI.replace('/', '%2F')}"
       f"&dtFim={DT_FIM.replace('/', '%2F')}"
       f"&txtPesq={PROC}"
       f"&tipoPesq=PROC")
print("URL:", url)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1366, "height": 900},
                              user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        time.sleep(8)
        body = page.evaluate("document.body.innerText")
        print("=== RESULTADO DJERJ ===")
        print(body[:5000])
        # links de íntegra
        links = page.evaluate("Array.from(document.querySelectorAll('a')).map(a => (a.textContent||'').trim()+' => '+(a.href||'')).filter(s=>s.length>15).slice(0,25)")
        print("=== LINKS ===")
        for l in links:
            print(l)
    except Exception as e:
        print(f"Erro: {e}")
    browser.close()
