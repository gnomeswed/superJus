# -*- coding: utf-8 -*-
"""Capturar o payload real da API de movimentos que o portal TJRJ usa."""
import os, sys, time, json, logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
sys.stdout.reconfigure(encoding="utf-8")
os.environ["PYTHONIOENCODING"] = "utf-8"

PROC = "0023013-51.2021.8.19.0078"
captured = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 850},
    )
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # Capturar requests de movimentos e da API em geral
    def on_request(req):
        if "api" in req.url or "movimento" in req.url:
            body = None
            try:
                body = req.post_data
            except Exception:
                pass
            captured.append({"url": req.url, "method": req.method, "body": body})

    page.on("request", on_request)

    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
    time.sleep(3)
    iframe_el = page.wait_for_selector("iframe#mainframe", timeout=20000)
    frame = iframe_el.content_frame()
    inp = frame.query_selector("input[name='numeroProcesso']")
    inp.fill(PROC)
    btns = frame.query_selector_all("button")
    btn = None
    for b in btns:
        if "pesquisar" in b.inner_text().lower() or "buscar" in b.inner_text().lower():
            btn = b; break
    if not btn and btns: btn = btns[0]
    btn.click()
    time.sleep(6)

    # Mostrar o que capturamos
    print(f"=== {len(captured)} requests de movimentos capturados ===")
    for c in captured:
        print(f"\nURL: {c['url']}")
        print(f"METHOD: {c['method']}")
        print(f"BODY: {c['body']}")

    # Salvar o body do primeiro POST pra reproduzir
    if captured:
        for c in captured:
            if c["method"] == "POST" and c["body"]:
                with open(r"C:\Projetos\superJus\scripts\payload_movimentos_julio.json", "w", encoding="utf-8") as f:
                    f.write(c["body"])
                print(f"\n[OK] Payload salvo em scripts/payload_movimentos_julio.json")

    browser.close()