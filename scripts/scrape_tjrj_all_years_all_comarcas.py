# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Navegando para o TJRJ conspublica...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
    time.sleep(4)
    
    frame = page.frame_locator("iframe#mainframe")
    
    print("1. Clicando na aba #nav-porNome...")
    frame.locator("#nav-porNome").click()
    time.sleep(2)
    
    print("2. Preenchendo Origem em #porNome #filtroOrigem1...")
    frame.locator("#porNome #filtroOrigem1").fill("1ª Instância")
    time.sleep(1)
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    time.sleep(1)
    
    print("3. Preenchendo Nome da Parte em #porNome #nomeParte (sem restringir anos/comarca)...")
    frame.locator("#porNome #nomeParte").fill("LUCAS DE SOUZA FREITAS")
    time.sleep(1)
    
    # Desmarcar somente em andamento para buscar processos arquivados/antigos
    try:
        chk = frame.locator("#porNome #procEmAndamento2")
        if chk.is_checked():
            chk.uncheck()
            print("Desmarcado 'Somente em andamento'")
    except Exception as e:
        print("Aviso checkbox:", e)
        
    time.sleep(1)
    
    print("4. Clicando no botão Pesquisar em #porNome #botaoPesquisarProcesso...")
    frame.locator("#porNome #botaoPesquisarProcesso").click()
    
    print("5. Aguardando 15 segundos para carregar TODOS os processos do TJRJ de Lucas de Souza Freitas...")
    time.sleep(15)
    
    page.screenshot(path="tjrj_resultado_todos_lucas.png")
    
    real_frame = page.query_selector("iframe#mainframe").content_frame()
    body_txt = real_frame.inner_text("body")
    
    out_file = r"C:\Projetos\superJus\tjrj_lucas_todos_processos.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(body_txt)
        
    print("=== RESULTADO FINAL DE TODOS OS PROCESSOS DE LUCAS DE SOUZA FREITAS ===")
    print(body_txt[:4000])
    
    browser.close()
