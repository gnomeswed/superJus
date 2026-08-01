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
    frame.locator("input[name='numeroProcesso']").fill(hc_num)
    time.sleep(1)
    frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
    time.sleep(6)
    
    real_frame = page.query_selector("iframe#mainframe").content_frame()
    
    # 1. Clicar em Listar todos os personagens
    try:
        print("Clicando em 'Listar todos os personagens' no HC...")
        frame.locator("text=Listar todos os personagens").click()
        time.sleep(3)
        pers_txt = real_frame.inner_text("body")
        print("=== PERSONAGENS HC ===")
        print(pers_txt[:2000])
    except Exception as e:
        print("Aviso personagens HC:", e)
        pers_txt = ""
        
    # 2. Clicar na Íntegra do Julgamento Monocrático
    try:
        print("Clicando na Íntegra do Julgamento Monocrático...")
        integra_link = frame.locator("text=Julg. Monocrático").first
        if integra_link.is_visible():
            integra_link.click()
            time.sleep(4)
            integra_txt = real_frame.inner_text("body")
            print("=== ÍNTEGRA DO JULGAMENTO MONOCRÁTICO ===")
            print(integra_txt[:3500])
        else:
            integra_txt = "Link não visível"
    except Exception as e:
        print("Aviso íntegra:", e)
        integra_txt = str(e)
        
    out_file = os.path.join(target_dir, "inteiro_teor_hc_lucas_2017.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("=== PERSONAGENS ===\n" + pers_txt + "\n\n=== ÍNTEGRA DO DECISÃO ===\n" + integra_txt)
        
    print(f"Salvo em {out_file}")
    browser.close()
