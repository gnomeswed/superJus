# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Navegando para TJRJ conspublica...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/conspublica", timeout=35000)
    time.sleep(4)
    
    # Clicar na aba Por Nome
    page.click("text=Por Nome")
    time.sleep(2)
    
    # Inspecionar selects e inputs visíveis na aba Nome
    selects = page.query_selector_all("select")
    print(f"Total de selects: {len(selects)}")
    for s in selects:
        s_id = s.get_attribute("id")
        s_name = s.get_attribute("name")
        print(f"  Select: id={s_id}, name={s_name}")
        # Tentar selecionar a 1ª opção válida (1ª Instância)
        try:
            s.select_option(index=1)
        except Exception:
            pass
            
    # Preencher Nome
    inp_nome = page.query_selector("input[placeholder*='nome da parte'], input[name*='nomeParte'], input[placeholder*='Nome']")
    if inp_nome:
        inp_nome.fill("LUCAS DE SOUZA FREITAS")
        print("Nome preenchido!")
        
    # Preencher Ano Inicial
    inp_ano_i = page.query_selector("input[placeholder*='ano inicial'], input[name*='anoInicial']")
    if inp_ano_i:
        inp_ano_i.fill("2015")
        print("Ano Inicial 2015 preenchido!")
        
    # Preencher Ano Final
    inp_ano_f = page.query_selector("input[placeholder*='Ano Final'], input[name*='anoFinal']")
    if inp_ano_f:
        inp_ano_f.fill("2020")
        print("Ano Final 2020 preenchido!")
        
    # Uncheck somente em andamento
    try:
        page.uncheck("input[name='procEmAndamento']", force=True)
    except Exception:
        pass
        
    time.sleep(1)
    
    # Disparar clique no botão Pesquisar dentro do form visível de nome
    frame_btns = page.query_selector_all("button")
    for b in frame_btns:
        if "pesquisar" in b.inner_text().lower() and b.is_visible():
            print("Clicando no botão visível Pesquisar...")
            b.click()
            break
            
    time.sleep(12)
    
    body_txt = page.inner_text("body")
    out_file = r"C:\Projetos\Super Analista Jurídico\tjrj_resultado_final_lucas.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(body_txt)
        
    print("=== RESULTADO DA BUSCA POR NOME LUCAS DE SOUZA FREITAS ===")
    print(body_txt[:3500])
    
    browser.close()
