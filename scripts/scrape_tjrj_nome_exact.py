# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Navegando para o TJRJ conspublica...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/conspublica", timeout=30000)
    time.sleep(3)
    
    # Clicar na aba 'Por Nome'
    page.click("text=Por Nome")
    time.sleep(2)
    
    # Preencher input por placeholder/name
    inp_nome = page.query_selector("input[placeholder*='nome da parte'], input[name*='nome da parte']")
    if inp_nome:
        print("Preenchendo nome: LUCAS DE SOUZA FREITAS")
        inp_nome.fill("LUCAS DE SOUZA FREITAS")
        time.sleep(1)
        
        # Uncheck procEmAndamento
        chk = page.query_selector("input[name='procEmAndamento']")
        if chk and chk.is_checked():
            chk.uncheck()
            print("Unchecked procEmAndamento!")
            
        # Clicar no botão Pesquisar
        btn_pesq = page.query_selector("button:has-text('Pesquisar')")
        if btn_pesq:
            print("Clicando no botão Pesquisar...")
            btn_pesq.click()
            time.sleep(10)
            
            body_txt = page.inner_text("body")
            with open("resultado_lucas_tjrj_completo.txt", "w", encoding="utf-8") as f:
                f.write(body_txt)
                
            print("=== RESULTADO DA CONSULTA POR NOME ===")
            print(body_txt[:3000])

    browser.close()
