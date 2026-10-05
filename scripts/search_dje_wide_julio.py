# -*- coding: utf-8 -*-
"""DJERJ Result.aspx — varredura ampla — Búzios 01/08-13/08 + HC 0029845 01/08-13/08"""
import time, sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')

SEARCHES = [
    ("Búzios 01-13/08", "0023013-51.2021.8.19.0078", "01/08/2026", "13/08/2026"),
    ("HC 2ª inst 01-13/08", "0029845-67.2026.8.19.0000", "01/08/2026", "13/08/2026"),
    ("Búzios 13/08", "0023013-51.2021.8.19.0078", "13/08/2026", "13/08/2026"),
    ("HC 13/08", "0029845-67.2026.8.19.0000", "13/08/2026", "13/08/2026"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1366, "height": 900},
                              user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    for rotulo, proc, dt_ini, dt_fim in SEARCHES:
        url = (f"https://www3.tjrj.jus.br/consultadje/Result.aspx"
               f"?dtInicio={dt_ini.replace('/', '%2F')}"
               f"&dtFim={dt_fim.replace('/', '%2F')}"
               f"&txtPesq={proc}&tipoPesq=PROC")
        print(f"\n{'='*60}\n=== {rotulo} ===\nURL: {url}")
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            time.sleep(6)
            body = page.evaluate("document.body.innerText")
            # extrair resultado
            if "Não foram encontradas" in body:
                print(">>> NENHUMA PUBLICAÇÃO")
            else:
                print(">>> POSSÍVEL PUBLICAÇÃO:")
                idx = body.find("0023013")
                if idx == -1: idx = body.find("0029845")
                print(body[max(0,idx-300):idx+2500])
                links = page.evaluate("Array.from(document.querySelectorAll('a')).map(a => (a.textContent||'').trim()+' => '+(a.href||'')).filter(s=>s.length>15).slice(0,15)")
                for l in links:
                    print("LINK:", l)
        except Exception as e:
            print(f"Erro: {e}")
    browser.close()
