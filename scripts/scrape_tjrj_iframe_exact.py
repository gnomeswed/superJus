# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Navegando para TJRJ conspublica...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
    time.sleep(4)
    
    # Localizar frame #mainframe
    frame = page.frame_locator("iframe#mainframe")
    
    print("Clicando no elemento 'Por Nome' dentro do iframe...")
    frame.locator("text=Por Nome").click()
    time.sleep(2)
    
    print("Selecionando Origem no dropdown...")
    # Clicar no p-dropdown de Origem e apertar ArrowDown + Enter
    dropdown = frame.locator("p-dropdown[name='filtroOrigem1']")
    dropdown.click()
    time.sleep(1)
    page.keyboard.press("ArrowDown")
    time.sleep(0.5)
    page.keyboard.press("Enter")
    time.sleep(1)
    
    print("Preenchendo nome da parte: LUCAS DE SOUZA FREITAS...")
    inp_nome = frame.locator("input[placeholder*='nome da parte'], input[name='nomeParte']")
    inp_nome.fill("LUCAS DE SOUZA FREITAS")
    time.sleep(1)
    
    # Desmarcar procEmAndamento se marcado
    try:
        chk = frame.locator("input[name='procEmAndamento']")
        if chk.is_checked():
            chk.uncheck()
            print("Desmarcada a opção 'somente em andamento'")
    except Exception:
        pass
        
    time.sleep(1)
    
    print("Clicando no botão Pesquisar...")
    frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
    
    print("Aguardando 10 segundos para carregar lista de processos...")
    time.sleep(10)
    
    page.screenshot(path="tjrj_resultado_iframe_lucas.png")
    
    # Extrair texto do frame
    frame_element = page.query_selector("iframe#mainframe")
    real_frame = frame_element.content_frame()
    body_txt = real_frame.inner_text("body")
    
    out_file = r"C:\Projetos\Super Analista Jurídico\tjrj_resultado_lucas_iframe_sucesso.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(body_txt)
        
    print("=== RESULTADO OBTIDO DO TJRJ POR NOME ===")
    print(body_txt[:3500])
    
    browser.close()
