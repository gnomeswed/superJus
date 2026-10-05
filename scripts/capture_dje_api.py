# -*- coding: utf-8 -*-
"""Captura chamadas de rede do DJERJ novo ao pesquisar por processo"""
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

    captured = []
    def on_response(resp):
        url = resp.url
        if any(k in url.lower() for k in ["api", "search", "busca", "processo", "consulta", "json", "service"]):
            try:
                ct = resp.headers.get("content-type", "")
                if "json" in ct or "text" in ct:
                    body = resp.text() if resp.status < 400 else ""
                    captured.append({"url": url, "status": resp.status, "body": body[:3000]})
            except Exception:
                pass
    page.on("response", on_response)

    try:
        page.goto("https://www3.tjrj.jus.br/consultadje/", wait_until="domcontentloaded", timeout=45000)
        time.sleep(6)
        # Aba Processo
        page.evaluate("document.querySelector('#abas-processo-tab').click()")
        time.sleep(2)
        # Preencher
        page.evaluate("""(args) => {
            const setVal = (sel, val) => {
                const el = document.querySelector(sel);
                if (!el) return false;
                el.value = val;
                el.dispatchEvent(new Event('input', {bubbles:true}));
                el.dispatchEvent(new Event('change', {bubbles:true}));
                return true;
            };
            setVal("input[name='procDtInicio']", args.ini);
            setVal("input[name='procDtFim']", args.fim);
            setVal("input[name='numProcesso']", args.proc);
        }""", {"ini": DT_INI, "fim": DT_FIM, "proc": PROC})
        time.sleep(1)
        # Clicar pesquisar (procurar por texto)
        page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const b = btns.find(x => (x.textContent||'').trim().toUpperCase() === 'PESQUISAR' && x.offsetParent !== null);
            if (b) { b.click(); return 'ok'; }
            return 'not found';
        }""")
        time.sleep(15)
        print("=== CHAMADAS DE REDE CAPTURADAS ===")
        for c in captured:
            print(f"\n[{c['status']}] {c['url']}")
            if c['body']:
                print(c['body'][:2000])
        print("\n=== BODY PÁGINA (fim) ===")
        body = page.evaluate("document.body.innerText")
        idx = body.find("PESQUISAR")
        print(body[max(0,idx-200):idx+3000])
    except Exception as e:
        print(f"Erro: {e}")
    browser.close()
