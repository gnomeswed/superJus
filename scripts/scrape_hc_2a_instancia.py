# -*- coding: utf-8 -*-
import time
import os
from playwright.sync_api import sync_playwright

hc_num = "0046418-98.2017.8.19.0000"
target_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print(f"Acessando Habeas Corpus {hc_num} na 2ª Instância do TJRJ...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
    time.sleep(4)
    
    frame = page.frame_locator("iframe#mainframe")
    
    print("1. Selecionando Origem: Tribunal de Justiça (2ª Instância)...")
    try:
        inp_origem = frame.locator("#filtroOrigem1")
        inp_origem.fill("Tribunal de Justiça")
        time.sleep(1)
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
    except Exception as e:
        print("Aviso origem:", e)
        
    time.sleep(1)
    
    print(f"2. Preenchendo número do HC: {hc_num}...")
    frame.locator("input[name='numeroProcesso']").fill(hc_num)
    time.sleep(1)
    
    print("3. Clicando no botão Pesquisar...")
    frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
    
    print("Aguardando 10 segundos...")
    time.sleep(10)
    
    real_frame = page.query_selector("iframe#mainframe").content_frame()
    hc_txt = real_frame.inner_text("body")
    
    print("=== ESPELHO DO HABEAS CORPUS DA 2ª INSTÂNCIA ===")
    print(hc_txt[:3500])
    
    out_file = os.path.join(target_dir, "hc_2017_lucas_2a_instancia.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(hc_txt)
        
    print(f"Salvo em {out_file}")
    browser.close()
