# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Navegando para a busca por NOME no TJRJ...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=30000, wait_until="domcontentloaded")
    time.sleep(3)
    
    iframe_el = page.query_selector("iframe#mainframe")
    if iframe_el:
        frame = iframe_el.content_frame()
        if frame:
            # Clicar na opção "Por Nome"
            labels = frame.query_selector_all("label, span, a, input")
            for l in labels:
                if "por nome" in l.inner_text().lower():
                    print("Clicando na aba 'Por Nome'...")
                    l.click()
                    time.sleep(2)
                    break
            
            # Buscar campo de input de nome
            inputs = frame.query_selector_all("input")
            print(f"Inputs no formulário: {len(inputs)}")
            for inp in inputs:
                inp_type = inp.get_attribute("type")
                inp_name = inp.get_attribute("name") or inp.get_attribute("id") or inp.get_attribute("placeholder")
                print(f"  Input: {inp_name} ({inp_type})")
                
            # Preencher o nome
            name_input = frame.query_selector("input[type='text']")
            if name_input:
                name_input.fill("LUCAS DE SOUZA FREITAS")
                time.sleep(1)
                
                # Clicar em Pesquisar
                btns = frame.query_selector_all("button")
                for b in btns:
                    if "pesquisar" in b.inner_text().lower():
                        print("Clicando em Pesquisar por Nome...")
                        b.click()
                        time.sleep(6)
                        break
                        
            # Extrair texto do resultado
            res_txt = frame.inner_text("body")
            print("=== RESULTADO DA BUSCA POR NOME ===")
            print(res_txt[:1500])

    browser.close()
