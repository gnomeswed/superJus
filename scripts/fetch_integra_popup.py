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
    
    # Capturar popup ao clicar no link do Inteiro Teor
    try:
        print("Clicando na Íntegra e aguardando popup...")
        with page.expect_popup(timeout=15000) as popup_info:
            frame.locator("text=Julg. Monocrático").first.click()
        popup = popup_info.value
        popup.wait_for_load_state("domcontentloaded")
        time.sleep(3)
        integra_txt = popup.inner_text("body")
        print("=== BINGO! TEXTO COMPLETO DO DECISÃO MONOCRÁTICA ===")
        print(integra_txt)
    except Exception as e:
        print("Erro popup:", e)
        integra_txt = str(e)
        
    out_file = os.path.join(target_dir, "decisao_monocratica_hc_lucas_2017.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(integra_txt)
        
    print(f"Salvo em {out_file}")
    browser.close()
