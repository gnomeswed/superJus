# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Acessando TJRJ conspublica...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000)
    time.sleep(4)
    
    frame = page.frame_locator("iframe#mainframe")
    
    print("1. Clicando no tab #nav-porNome...")
    frame.locator("#nav-porNome").click()
    time.sleep(2)
    
    print("2. Preenchendo Origem: 1ª Instância...")
    inp_origem = frame.locator("#filtroOrigem1")
    inp_origem.fill("1ª Instância")
    time.sleep(1)
    
    print("3. Selecionando 1ª Instância...")
    item_origem = frame.locator("#itemAutocompletefiltroOrigem10")
    if item_origem.is_visible():
        item_origem.click()
    else:
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
    time.sleep(1)
    
    print("4. Preenchendo Nome da Parte: RODRIGO DUARTE DE SOUZA...")
    inp_nome = frame.locator("#porNome input[name='nomeParte'], input[name='nomeParte']")
    inp_nome.fill("RODRIGO DUARTE DE SOUZA")
    time.sleep(1)
    
    # Desmarcar somente em andamento para trazer todos
    try:
        chk = frame.locator("#porNome input[name='procEmAndamento'], input[name='procEmAndamento']").first
        if chk.is_checked():
            chk.uncheck()
            print("Desmarcado 'Somente em andamento'")
    except Exception as e:
        print("Aviso no checkbox:", e)
        
    time.sleep(1)
    
    print("5. Clicando no botão Pesquisar...")
    btn_pesq = frame.locator("#porNome #botaoPesquisarProcesso, #botaoPesquisarProcesso").first
    btn_pesq.click()
    
    print("6. Aguardando carregar resultado...")
    time.sleep(12)
    
    page.screenshot(path="c:/Projetos/superJus/tjrj_resultado_rodrigo.png")
    
    real_frame = page.query_selector("iframe#mainframe").content_frame()
    body_txt = real_frame.inner_text("body")
    
    with open("c:/Projetos/superJus/resultado_rodrigo_duarte_tjrj.txt", "w", encoding="utf-8") as f:
        f.write(body_txt)
        
    print("Resultado salvo em resultado_rodrigo_duarte_tjrj.txt")
    browser.close()
