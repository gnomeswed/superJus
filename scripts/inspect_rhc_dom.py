# -*- coding: utf-8 -*-
"""Inspecionar o DOM da tabela de resultados do TJRJ."""
import os, sys, time, json, logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
sys.stdout.reconfigure(encoding="utf-8")
os.environ["PYTHONIOENCODING"] = "utf-8"

PROC = "0029845-67.2026.8.19.0000"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 850},
    )
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
    time.sleep(3)
    iframe_el = page.wait_for_selector("iframe#mainframe", timeout=20000)
    frame = iframe_el.content_frame()

    inp = frame.query_selector("input[name='numeroProcesso']")
    inp.fill(PROC)
    btns = frame.query_selector_all("button")
    btn = None
    for b in btns:
        if "pesquisar" in b.inner_text().lower():
            btn = b; break
    if not btn and btns: btn = btns[0]
    btn.click()
    time.sleep(6)

    # Inspecionar HTML da linha do RHC
    html = frame.evaluate("""() => {
        const rows = document.querySelectorAll('tr');
        for (const tr of rows) {
            if (tr.innerText.includes('RECURSO ORDINARIO')) {
                return tr.outerHTML;
            }
        }
        return 'NAO ENCONTRADO';
    }""")
    print("=== HTML da linha do RHC ===")
    print(html[:3000])

    browser.close()