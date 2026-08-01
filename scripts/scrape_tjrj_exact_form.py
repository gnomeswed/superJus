# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Acessando Portal TJRJ para Consulta por Nome Parte (LUCAS DE SOUZA FREITAS)...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=30000, wait_until="domcontentloaded")
    time.sleep(3)
    
    iframe_el = page.query_selector("iframe#mainframe")
    if iframe_el:
        frame = iframe_el.content_frame()
        if frame:
            # 1. Clicar no radio / aba "Por Nome"
            por_nome_tab = frame.query_selector("input[value='NOME'], label:has-text('Por Nome'), span:has-text('Por Nome')")
            if por_nome_tab:
                por_nome_tab.click()
                time.sleep(1)
            else:
                frame.evaluate("""() => {
                    const el = Array.from(document.querySelectorAll('*')).find(e => e.textContent && e.textContent.trim() === 'Por Nome');
                    if (el) el.click();
                }""")
                time.sleep(1)
                
            # 2. Preencher nomeParte
            inp_nome = frame.query_selector("input[name='nomeParte']")
            if inp_nome:
                print("Preenchendo nomeParte: LUCAS DE SOUZA FREITAS")
                inp_nome.fill("LUCAS DE SOUZA FREITAS")
                
            # 3. Preencher anoInicial e anoFinal
            inp_ano_i = frame.query_selector("input[name='anoInicial1']")
            if inp_ano_i:
                inp_ano_i.fill("2015")
            inp_ano_f = frame.query_selector("input[name='anoFinal1']")
            if inp_ano_f:
                inp_ano_f.fill("2020")
                
            # Uncheck procEmAndamento se existir para trazer arquivados
            chk = frame.query_selector("input[name='procEmAndamento']")
            if chk and chk.is_checked():
                chk.uncheck()
                
            time.sleep(1)
            
            # Clicar botão pesquisar
            frame.evaluate("""() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const btn = btns.find(b => b.textContent && b.textContent.trim().toLowerCase().includes('pesquisar'));
                if (btn) btn.click();
            }""")
            
            print("Pesquisa enviada! Aguardando resultados do TJRJ...")
            time.sleep(10)
            
            page.screenshot(path="tjrj_resultado_lucas_2017.png")
            body_txt = frame.inner_text("body")
            
            with open("tjrj_resultado_lucas_2017.txt", "w", encoding="utf-8") as f:
                f.write(body_txt)
                
            print("=== CONTEÚDO DA RESPOSTA DO TJRJ ===")
            print(body_txt[:2000])

    browser.close()
