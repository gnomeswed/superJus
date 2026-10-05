# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Acessando TJRJ conspublica...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
    time.sleep(4)
    
    frame = page.frame_locator("iframe#mainframe")
    
    print("1. Clicando na aba #nav-porNome...")
    frame.locator("#nav-porNome").click()
    time.sleep(2)
    
    print("2. Selecionando Origem no primeiro p-dropdown dentro de #porNome...")
    dropdown = frame.locator("#porNome p-dropdown").first
    dropdown.click()
    time.sleep(1)
    page.keyboard.press("ArrowDown")
    time.sleep(0.5)
    page.keyboard.press("Enter")
    time.sleep(1)
    
    print("3. Preenchendo nomeParte com LUCAS DE SOUZA FREITAS...")
    frame.locator("#porNome input[name='nomeParte']").fill("LUCAS DE SOUZA FREITAS")
    time.sleep(1)
    
    # Desmarcar procEmAndamento se marcada
    try:
        chk = frame.locator("#porNome input[name='procEmAndamento']")
        if chk.is_checked():
            chk.uncheck()
            print("Desmarcada opção procEmAndamento!")
    except Exception:
        pass
        
    time.sleep(1)
    
    print("4. Clicando no botão Pesquisar...")
    frame.locator("#porNome button").first.click()
    
    print("5. Aguardando 12 segundos para a resposta com a lista de processos...")
    time.sleep(12)
    
    page.screenshot(path="tjrj_resultado_lucas_definitivo.png")
    
    real_frame = page.query_selector("iframe#mainframe").content_frame()
    body_txt = real_frame.inner_text("body")
    
    out_file = r"C:\Projetos\superJus\tjrj_lucas_resultado_definitivo.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(body_txt)
        
    print("=== PROCESSO(S) ENCONTRADO(S) DE LUCAS DE SOUZA FREITAS ===")
    print(body_txt[:3500])
    
    browser.close()
