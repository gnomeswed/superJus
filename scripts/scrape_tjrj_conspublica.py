# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Indo direto para https://www3.tjrj.jus.br/consultaprocessual/#/conspublica...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/conspublica", timeout=30000)
    time.sleep(3)
    
    # Inspecionar todos os links, botões e tabs no Angular app
    elements = page.query_selector_all("a, button, li, span, input")
    print(f"Elementos encontrados: {len(elements)}")
    
    for el in elements:
        t = el.inner_text().strip()
        if any(x in t.lower() for x in ['nome', 'oab', 'cpf', 'processo', 'pesquisar']):
            print(f"  Elemento: tag={el.evaluate('e => e.tagName')}, text='{t}'")
            if t.lower() == "por nome":
                print(">>> Clicando em 'Por Nome'! <<<")
                el.click()
                time.sleep(2)
                break

    # Verificar formulário visível agora
    inputs = page.query_selector_all("input")
    for inp in inputs:
        name = inp.get_attribute("name") or inp.get_attribute("placeholder") or inp.get_attribute("id")
        print(f"  Input visível: name={name}")

    inp_nome = page.query_selector("input[name='nomeParte']")
    if inp_nome:
        inp_nome.fill("LUCAS DE SOUZA FREITAS")
        print("Nome preenchido!")
        
        # Uncheck apenas em andamento para ver arquivados de 2017
        chk = page.query_selector("input[name='procEmAndamento']")
        if chk and chk.is_checked():
            chk.uncheck()
            
        btn_pesq = page.query_selector("button:has-text('Pesquisar')")
        if btn_pesq:
            btn_pesq.click()
            print("Pesquisa efetuada!")
            time.sleep(8)
            print("=== RESULTADOS DO TJRJ ===")
            print(page.inner_text("body")[:3000])

    browser.close()
