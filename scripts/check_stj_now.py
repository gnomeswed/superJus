# -*- coding: utf-8 -*-
import time, sys, re, os
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

URL = "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo=202603112107&totalRegistrosPorPagina=40&aplicacao=processos.ea"

print("=== STJ HC 1.116.750/RJ — verificacao ao vivo ===")
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox","--disable-blink-features=AutomationControlled","--disable-dev-shm-usage"])
        ctx = browser.new_context(
            viewport={"width":1366,"height":900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            locale="pt-BR",
        )
        ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});")
        page = ctx.new_page()
        print("Navegando STJ...")
        page.goto(URL, wait_until="domcontentloaded", timeout=50000)
        time.sleep(7)
        print(f"URL final: {page.url}")
        txt = page.evaluate("document.body.innerText")
        print(f"Body chars: {len(txt)}")
        print(txt[:6000])
        print("\n--- BUSCA ULTIMA FASE ---")
        for kw in ["ULTIMA FASE", "CONCLUSOS", "GABINETE", "OG FERNANDES", "Decis", "1116750"]:
            idx = txt.upper().find(kw.upper())
            if idx != -1:
                print(f"[{kw}] ...{txt[max(0,idx-100):idx+350].replace(chr(10),' | ')}")
        html = page.content()
        if "sequencial" in html:
            m = re.findall(r'sequencial=\d+', html)
            print(f"sequenciais: {m[:5]}")
        # screenshot
        try:
            page.screenshot(path=r"C:\Projetos\superJus\_stj_now.png", full_page=True)
            print("screenshot ok")
        except: pass
        browser.close()
        print("=== FIM STJ ===")
except Exception as e:
    print(f"ERRO STJ: {e}")
    import traceback; traceback.print_exc()
