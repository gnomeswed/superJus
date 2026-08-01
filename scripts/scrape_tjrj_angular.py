# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context()
    page = ctx.new_page()
    
    print("Acessando TJRJ...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=30000)
    time.sleep(3)
    
    # Inspecionar todos os iframes e elementos
    frames = page.frames
    print(f"Total de frames: {len(frames)}")
    
    for idx, f in enumerate(frames):
        print(f"Frame {idx}: URL={f.url}")
        try:
            # Procurar radios / abas no frame
            radios = f.query_selector_all("input[type='radio']")
            for r in radios:
                val = r.get_attribute("value")
                id_attr = r.get_attribute("id")
                print(f"  Radio: id={id_attr}, val={val}")
                if val == "NOME" or id_attr == "consultanome":
                    print("--> Clicando radio NOME!")
                    f.evaluate("(el) => el.click()", r)
                    time.sleep(2)
                    
                    # Preencher nome
                    inp_nome = f.query_selector("input[name='nomeParte']")
                    if inp_nome:
                        inp_nome.fill("LUCAS DE SOUZA FREITAS")
                        print("Nome preenchido!")
                        time.sleep(1)
                        
                        # Clicar pesquisar
                        btn = f.query_selector("button:has-text('Pesquisar')")
                        if btn:
                            btn.click()
                            print("Botão Pesquisar clicado!")
                            time.sleep(8)
                            print("=== RESULTADO ===")
                            print(f.inner_text("body")[:2000])
        except Exception as e:
            print(f"Erro no frame {idx}: {e}")

    browser.close()
