# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Iniciando consulta TJRJ para Lucas de Souza Freitas...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/conspublica", timeout=35000)
    time.sleep(3)
    
    # Clicar na aba Por Nome
    page.click("text=Por Nome")
    time.sleep(2)
    
    # Preencher input
    inp = page.query_selector("input[placeholder='Informe o nome da parte']")
    if inp:
        inp.fill("LUCAS DE SOUZA FREITAS")
        print("Nome preenchido!")
        
    # Uncheck procEmAndamento se visivel
    chk = page.query_selector("input[name='procEmAndamento']")
    if chk and chk.is_checked():
        chk.uncheck()
        print("Opção 'Somente em andamento' desmarcada!")
        
    # Clicar no botão Pesquisar dentro do form de nome
    btns = page.query_selector_all("button")
    for b in btns:
        if "pesquisar" in b.inner_text().lower():
            b.click()
            print("Botão Pesquisar clicado!")
            break
            
    time.sleep(10)
    
    txt = page.inner_text("body")
    print(f"Resultado final extraído ({len(txt)} caracteres):")
    print("-" * 50)
    print(txt[:2500])
    
    out_file = r"C:\Projetos\Super Analista Jurídico\tjrj_resultado_lucas_completo.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(txt)
    print(f"Salvo em {out_file}")
    
    browser.close()
