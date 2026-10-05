# -*- coding: utf-8 -*-
"""DJERJ novo — captura XHR/fetch do botão Pesquisar (aba Processo)"""
import time, sys, json
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')

PROC = "0023013-51.2021.8.19.0078"
DT_INI = "04/08/2026"
DT_FIM = "13/08/2026"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1366, "height": 900},
                              user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    xhrs = []
    def on_request(req):
        if req.resource_type in ("xhr", "fetch"):
            xhrs.append({"url": req.url, "method": req.method, "post": (req.post_data or "")[:2000]})
    page.on("request", on_request)

    try:
        page.goto("https://www3.tjrj.jus.br/consultadje/", wait_until="domcontentloaded", timeout=45000)
        time.sleep(6)
        page.click("#abas-processo-tab")
        time.sleep(2)
        page.fill("#procDtInicio", DT_INI)
        page.fill("#procDtFim", DT_FIM)
        page.fill("#numProcesso", PROC)
        time.sleep(1)
        page.click("#procBtnPesquisar")
        time.sleep(12)
        print("=== XHR/FETCH CAPTURADOS ===")
        for x in xhrs:
            print(f"\n[{x['method']}] {x['url']}")
            if x["post"]:
                print("POST:", x["post"][:1500])
        print("\n=== BODY FIM ===")
        body = page.evaluate("document.body.innerText")
        # procurar grid de resultado
        idx = body.find("grid")
        if idx == -1: idx = body.find("Tabela")
        print(body[max(0,idx-300):idx+4000] if idx != -1 else body[-2500:])
    except Exception as e:
        print(f"Erro: {e}")
    browser.close()
