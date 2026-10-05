# -*- coding: utf-8 -*-
"""DJERJ novo — trigger jQuery no botão + captura console/alerts"""
import time, sys
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

    logs = []
    page.on("console", lambda m: logs.append(f"[{m.type}] {m.text[:200]}"))
    page.on("dialog", lambda d: (logs.append(f"[dialog] {d.message[:200]}"), d.accept()))
    reqs = []
    page.on("request", lambda r: reqs.append((r.resource_type, r.method, r.url)))

    try:
        page.goto("https://www3.tjrj.jus.br/consultadje/", wait_until="domcontentloaded", timeout=45000)
        time.sleep(6)
        page.click("#abas-processo-tab")
        time.sleep(2)
        page.fill("#procDtInicio", DT_INI)
        page.fill("#procDtFim", DT_FIM)
        page.fill("#numProcesso", PROC)
        time.sleep(1)
        # disparar via jQuery
        r = page.evaluate("""() => {
            if (window.jQuery) {
                jQuery('#procBtnPesquisar').trigger('click');
                return 'jquery trigger ok';
            }
            return 'no jquery';
        }""")
        print(r)
        time.sleep(15)
        print("=== CONSOLE ===")
        for l in logs[-20:]:
            print(l)
        print("=== REQUISIÇÕES (pós-clique) ===")
        for rt, m, u in reqs:
            if rt in ("xhr", "fetch") or "api" in u.lower() or "search" in u.lower():
                print(f"  {rt} {m} {u[:180]}")
        body = page.evaluate("document.body.innerText")
        print("=== BODY (procurando resultado) ===")
        for marker in ["Nenhum", "nenhum", "Registro", "0023013", "Publicação", "Data da"]:
            idx = body.find(marker)
            if idx != -1:
                print(body[max(0,idx-200):idx+2500])
                break
        else:
            print(body[-2000:])
    except Exception as e:
        print(f"Erro: {e}")
    browser.close()
