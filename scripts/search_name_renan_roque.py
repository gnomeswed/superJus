# -*- coding: utf-8 -*-
import sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    ctx = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    )
    page = ctx.new_page()

    print("1. Acessando consulta por nome no TJRJ...")
    page.goto('https://www3.tjrj.jus.br/consultaprocessual/#/conspublica', timeout=40000)
    time.sleep(3)
    page.click('text=Por Nome')
    time.sleep(2)
    
    inp = page.locator("input[placeholder*='nome da parte'], input[name*='nome da parte']").first
    if inp.is_visible():
        print("2. Preenchendo 'RENAN ROQUE'...")
        inp.fill('RENAN ROQUE')
        time.sleep(1)
        
        chk = page.locator("input[name='procEmAndamento']").first
        if chk.is_visible() and chk.is_checked():
            chk.uncheck()
            
        btn = page.locator("button:has-text('Pesquisar')").first
        if btn.is_visible():
            btn.click()
            time.sleep(8)
            body = page.inner_text('body')
            print("--- RESULTADO DA BUSCA POR NOME ---")
            lines = [l.strip() for l in body.splitlines() if l.strip()]
            for l in lines:
                if any(k in l.upper() for k in ["PROCESSO", "VARA", "COMARCA", "RENAN", "ROQUE", "REGISTRO", "NÃO FORAM", "RESULTADO"]):
                    print(f"  • {l}")
    browser.close()
