# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Acessando TJRJ conspublica...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/conspublica", timeout=35000)
    time.sleep(4)
    
    print("Clicando na aba 'Por Nome'...")
    page.click("text=Por Nome")
    time.sleep(2)
    
    print("Focando no dropdown Origem...")
    # Clicar no p-dropdown de Origem e usar teclado para selecionar a primeira opção
    dropdown = page.query_selector("p-dropdown[name='filtroOrigem1']")
    if dropdown:
        dropdown.click()
        time.sleep(1)
        page.keyboard.press("ArrowDown")
        time.sleep(0.5)
        page.keyboard.press("Enter")
        print("Origem selecionada via teclado!")
    else:
        print("Dropdown name=filtroOrigem1 não encontrado por selector simples.")
        
    time.sleep(1)
    
    print("Preenchendo nome: LUCAS DE SOUZA FREITAS...")
    page.fill("input[name='nomeParte']", "LUCAS DE SOUZA FREITAS")
    time.sleep(1)
    
    # Desmarcar somente em andamento
    try:
        page.uncheck("input[name='procEmAndamento']", force=True)
        print("Desmarcado procEmAndamento!")
    except Exception:
        pass
        
    time.sleep(1)
    
    print("Clicando no botão Pesquisar...")
    btn = page.query_selector("#botaoPesquisarProcesso, button:has-text('Pesquisar')")
    if btn:
        btn.click()
        print("Botão Pesquisar clicado com sucesso!")
        
    time.sleep(12)
    
    page.screenshot(path="tjrj_resultado_primeng.png")
    body_txt = page.inner_text("body")
    
    out_file = r"C:\Projetos\Super Analista Jurídico\tjrj_resultado_lucas_primeng.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(body_txt)
        
    print("=== CONTEÚDO FINAL DOS PROCESSOS DO LUCAS DE SOUZA FREITAS ===")
    print(body_txt[:3500])
    
    browser.close()
