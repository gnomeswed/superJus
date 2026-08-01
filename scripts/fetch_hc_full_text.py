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
    
    print(f"Acessando Habeas Corpus {hc_num} no TJRJ...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
    time.sleep(4)
    
    frame = page.frame_locator("iframe#mainframe")
    
    # Selecionar Origem 2ª Instância se necessário ou preencher direto o número
    inp_num = frame.locator("input[name='numeroProcesso']")
    inp_num.fill(hc_num)
    time.sleep(1)
    
    btn = frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first
    btn.click()
    print("Botão Pesquisar disparado...")
    time.sleep(8)
    
    real_frame = page.query_selector("iframe#mainframe").content_frame()
    hc_txt = real_frame.inner_text("body")
    
    print("=== ESPELHO DO HABEAS CORPUS DE LUCAS DE SOUZA FREITAS ===")
    print(hc_txt[:3500])
    
    out_file = os.path.join(target_dir, "habeas_corpus_2017_lucas_completo.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(hc_txt)
        
    print(f"Salvo com sucesso em {out_file}")
    browser.close()
