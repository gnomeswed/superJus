# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== CHECAGEM DIRETA DJERJ — 05/08/2026 ===")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()

    try:
        page.goto("https://www3.tjrj.jus.br/consultadjerj/consulta.aspx", wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

        # Look for search inputs
        inputs = page.query_selector_all("input")
        print(f"Inputs encontrados na página: {len(inputs)}")
        for inp in inputs:
            inp_id = inp.get_attribute("id") or ""
            inp_name = inp.get_attribute("name") or ""
            inp_type = inp.get_attribute("type") or ""
            if inp_type in ["text", "search"]:
                print(f"  • Input id='{inp_id}', name='{inp_name}'")

        # Fill process number in text input
        txt_input = page.query_selector("input[type='text']")
        if txt_input:
            txt_input.fill("0023013-51.2021.8.19.0078")
            time.sleep(1)
            btn = page.query_selector("input[type='submit'], button")
            if btn:
                btn.click()
                time.sleep(5)
                body_txt = page.evaluate("document.body.innerText")
                print("\n--- RESULTADO DJERJ HOJE ---")
                lines = [l.strip() for l in body_txt.split('\n') if l.strip()]
                for l in lines[:30]:
                    print(f"  {l}")

    except Exception as e:
        print(f"Erro na busca: {e}")

    browser.close()

print("\n=== FIM DA CONSULTA ===")
