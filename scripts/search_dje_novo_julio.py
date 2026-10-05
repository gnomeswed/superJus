# -*- coding: utf-8 -*-
"""DJERJ novo — busca por processo usando id do botão — 13/08/2026"""
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
    try:
        page.goto("https://www3.tjrj.jus.br/consultadje/", wait_until="domcontentloaded", timeout=45000)
        time.sleep(6)
        # aba processo
        page.click("#abas-processo-tab")
        time.sleep(2)
        # preencher com fill real
        page.fill("#procDtInicio", DT_INI)
        page.fill("#procDtFim", DT_FIM)
        page.fill("#numProcesso", PROC)
        time.sleep(1)
        # clicar no botão pelo id
        page.click("#procBtnPesquisar")
        time.sleep(15)
        body = page.evaluate("document.body.innerText")
        # procurar resultados
        for marker in ["Resultado", "Nenhum", "nenhum", "Não foi", "Processo", "Publicação"]:
            idx = body.find(marker)
            if idx != -1:
                print(f"=== [{marker}] @ {idx} ===")
                print(body[max(0,idx-150):idx+3500])
                print("---")
                break
        else:
            print("=== BODY FIM ===")
            print(body[-3000:])
    except Exception as e:
        print(f"Erro: {e}")
    browser.close()
