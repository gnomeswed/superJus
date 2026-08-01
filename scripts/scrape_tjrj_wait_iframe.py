# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Navegando para o TJRJ...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=40000)
    time.sleep(5)
    
    # Aguardar o iframe #mainframe carregar a URL interna
    iframe_handle = page.wait_for_selector("iframe#mainframe", timeout=20000)
    if iframe_handle:
        frame = iframe_handle.content_frame()
        print("Iframe #mainframe localizado! URL do frame:", frame.url)
        time.sleep(3)
        
        # Procurar radios
        radios = frame.query_selector_all("input[type='radio']")
        print(f"Total de radio buttons no frame: {len(radios)}")
        for r in radios:
            r_id = r.get_attribute("id")
            r_val = r.get_attribute("value")
            print(f"  Radio ID: {r_id}, Value: {r_val}")
            if r_id == "consultanome" or r_val == "NOME":
                print(">>> Clicando no radio consultanome! <<<")
                r.click()
                time.sleep(2)
                
                # Preencher nome da parte
                inp_nome = frame.query_selector("input[name='nomeParte']")
                if inp_nome:
                    inp_nome.fill("LUCAS DE SOUZA FREITAS")
                    print("Nome preenchido com sucesso: LUCAS DE SOUZA FREITAS")
                    time.sleep(1)
                    
                    # Uncheck somente em andamento
                    chk = frame.query_selector("input[name='procEmAndamento']")
                    if chk and chk.is_checked():
                        chk.uncheck()
                        print("Desmarcada a opção 'somente em andamento'")
                        
                    # Clicar no botão Pesquisar
                    btn_pesq = frame.query_selector("button:has-text('Pesquisar')")
                    if btn_pesq:
                        btn_pesq.click()
                        print("Botão PESQUISAR clicado!")
                        time.sleep(10)
                        
                        body_txt = frame.inner_text("body")
                        print("=== CONTEÚDO DOS PROCESSOS ENCONTRADOS ===")
                        print(body_txt[:4000])

    browser.close()
