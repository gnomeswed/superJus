# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Acessando TJRJ conspublica...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/conspublica", timeout=35000)
    time.sleep(3)
    
    print("Clicando na aba 'Por Nome'...")
    page.click("text=Por Nome")
    time.sleep(2)
    
    print("Preenchendo nome: LUCAS DE SOUZA FREITAS...")
    page.fill("input[placeholder='Informe o nome da parte']", "LUCAS DE SOUZA FREITAS")
    time.sleep(1)
    
    # Desmarcar procEmAndamento se marcada
    try:
        page.uncheck("input[name='procEmAndamento']", force=True)
        print("Desmarcada a opção 'somente em andamento'")
    except Exception:
        pass
        
    time.sleep(1)
    
    # Clicar no botão #botaoPesquisarProcesso via JS evaluate
    print("Disparando o clique no #botaoPesquisarProcesso...")
    page.evaluate("() => { const b = document.querySelector('#botaoPesquisarProcesso'); if(b) b.click(); }")
    
    print("Aguardando carregamento da lista de processos do Lucas...")
    time.sleep(10)
    
    page.screenshot(path="resultado_lucas_tjrj.png")
    body_txt = page.inner_text("body")
    
    out_file = r"C:\Projetos\Super Analista Jurídico\resultado_lucas_tjrj.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(body_txt)
        
    print("=== RESULTADO DA BUSCA DE PROCESSOS DO LUCAS DE SOUZA FREITAS ===")
    print(body_txt[:3500])
    
    browser.close()
