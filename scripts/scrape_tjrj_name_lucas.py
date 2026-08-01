# -*- coding: utf-8 -*-
import time
import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Acessando portal de consulta pública do TJRJ por NOME...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=30000, wait_until="domcontentloaded")
    time.sleep(3)
    
    iframe_el = page.query_selector("iframe#mainframe")
    if iframe_el:
        frame = iframe_el.content_frame()
        if frame:
            # Buscar radio button ou tab para pesquisa por nome de parte
            print("Preenchendo formulário...")
            # Tirar screenshot ou inspecionar formulário
            page.screenshot(path="tjrj_form.png")
            
            # Tentar preencher campo de busca ou selecionar por nome
            body_txt = frame.inner_text("body")
            print("Texto do frame:", body_txt[:600])

    browser.close()
