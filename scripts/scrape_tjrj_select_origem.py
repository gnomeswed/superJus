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
    
    # 1. Selecionar Origem
    print("Selecionando a Origem (1ª Instância)...")
    # Procurar o dropdown de origem ou clicar no elemento de origem
    origem_el = page.query_selector("p-dropdown[name='filtroOrigem1'], div:has-text('Origem'), p-dropdown")
    if origem_el:
        origem_el.click()
        time.sleep(1)
        # Clicar na opção 1ª Instância / Primeiro Grau
        op = page.query_selector("li:has-text('1ª Instância'), li:has-text('Primeira Instância'), li:has-text('1ª INSTANCIA'), p-dropdownitem:first-child")
        if op:
            op.click()
            print("Origem '1ª Instância' selecionada!")
        else:
            page.click("text=1ª Instância")
            print("Clicado text 1ª Instância!")
            
    time.sleep(1)
    
    # 2. Preencher Nome da parte
    inp_nome = page.query_selector("input[placeholder*='nome da parte'], input[name*='nomeParte'], input[placeholder*='Nome']")
    if inp_nome:
        inp_nome.fill("LUCAS DE SOUZA FREITAS")
        print("Nome preenchido!")
        
    # 3. Preencher Anos 2015 a 2020
    inp_i = page.query_selector("input[placeholder*='ano inicial'], input[name*='anoInicial']")
    if inp_i:
        inp_i.fill("2015")
    inp_f = page.query_selector("input[placeholder*='Ano Final'], input[name*='anoFinal']")
    if inp_f:
        inp_f.fill("2020")
        
    # Uncheck procEmAndamento
    try:
        page.uncheck("input[name='procEmAndamento']", force=True)
    except Exception:
        pass
        
    time.sleep(1)
    
    # 4. Clicar no botão Pesquisar
    print("Clicando no botão Pesquisar...")
    page.evaluate("() => { const b = document.querySelector('#botaoPesquisarProcesso') || Array.from(document.querySelectorAll('button')).find(x => x.textContent.toLowerCase().includes('pesquisar')); if(b) b.click(); }")
    
    time.sleep(12)
    
    body_txt = page.inner_text("body")
    out_file = r"C:\Projetos\Super Analista Jurídico\tjrj_resultado_origem_lucas.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(body_txt)
        
    print("=== RESULTADO OBTIDO DO TJRJ ===")
    print(body_txt[:3500])
    
    browser.close()
