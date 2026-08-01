# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Acessando Portal TJRJ...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=30000, wait_until="domcontentloaded")
    time.sleep(3)
    
    iframe_el = page.query_selector("iframe#mainframe")
    if iframe_el:
        frame = iframe_el.content_frame()
        if frame:
            print("Procurando o elemento 'Por Nome'...")
            # Clicar no link 'Por Nome'
            frame.click("text=Por Nome")
            time.sleep(2)
            
            print("Preenchendo nome da parte: LUCAS DE SOUZA FREITAS...")
            frame.fill("input[name='nomeParte']", "LUCAS DE SOUZA FREITAS")
            time.sleep(1)
            
            # Clicar no botão de Pesquisar da aba nome
            print("Clicando no botão Pesquisar...")
            frame.click("button:has-text('Pesquisar')")
            
            time.sleep(10)
            
            page.screenshot(path="tjrj_resultado_nome_sucesso.png")
            body_txt = frame.inner_text("body")
            
            with open("tjrj_resultado_nome_sucesso.txt", "w", encoding="utf-8") as f:
                f.write(body_txt)
                
            print("=== CONTEÚDO DA BUSCA DE PROCESSOS DO LUCAS DE SOUZA FREITAS ===")
            print(body_txt[:3000])

    browser.close()
