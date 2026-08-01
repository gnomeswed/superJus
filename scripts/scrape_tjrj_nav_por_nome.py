# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Navegando para o TJRJ consulta pública...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
    time.sleep(4)
    
    # Obter o frame interno #mainframe
    frame = page.frame_locator("iframe#mainframe")
    
    print("Clicando exatamente no id #nav-porNome...")
    frame.locator("#nav-porNome").click()
    time.sleep(2)
    
    print("Selecionando a Origem (1ª Instância)...")
    # Clicar no dropdown de origem e mandar seta para baixo + enter
    origem_dd = frame.locator("p-dropdown[name='filtroOrigem1']")
    origem_dd.click()
    time.sleep(1)
    page.keyboard.press("ArrowDown")
    time.sleep(0.5)
    page.keyboard.press("Enter")
    time.sleep(1)
    
    print("Preenchendo o Nome da Parte: LUCAS DE SOUZA FREITAS...")
    frame.locator("input[name='nomeParte']").fill("LUCAS DE SOUZA FREITAS")
    time.sleep(1)
    
    print("Preenchendo Anos: 2015 a 2020...")
    try:
        frame.locator("input[name='anoInicial1']").fill("2015")
        frame.locator("input[name='anoFinal1']").fill("2020")
    except Exception as e:
        print("Aviso nos anos:", e)
        
    # Uncheck procEmAndamento se marcado
    try:
        chk = frame.locator("input[name='procEmAndamento']")
        if chk.is_checked():
            chk.uncheck()
    except Exception:
        pass
        
    time.sleep(1)
    
    print("Clicando no botão Pesquisar (#botaoPesquisarProcesso)...")
    frame.locator("#botaoPesquisarProcesso").click()
    
    print("Aguardando 12 segundos para a resposta com a lista de processos...")
    time.sleep(12)
    
    page.screenshot(path="tjrj_sucesso_lucas_2017.png")
    
    real_frame = page.query_selector("iframe#mainframe").content_frame()
    body_txt = real_frame.inner_text("body")
    
    out_file = r"C:\Projetos\Super Analista Jurídico\tjrj_lucas_2017_sucesso.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(body_txt)
        
    print("=== PROCESSO(S) ENCONTRADO(S) PARA LUCAS DE SOUZA FREITAS ===")
    print(body_txt[:3500])
    
    browser.close()
