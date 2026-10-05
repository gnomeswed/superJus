# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

proc_num = "0004301-33.2018.8.19.0073"

print(f"=== CONSULTANDO DETALHES DA APELAÇÃO NO TJRJ AO VIVO: {proc_num} ===")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1366, "height": 900}, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    url = "https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica"
    page.goto(url, timeout=40000, wait_until="domcontentloaded")
    time.sleep(3)
    
    frame_el = page.wait_for_selector("iframe#mainframe", timeout=20000)
    frame = frame_el.content_frame()
    
    # Preencher número do processo
    frame.locator("input[name='numeroProcesso']").fill(proc_num)
    time.sleep(1)
    frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
    time.sleep(6)
    
    # Localizar a linha da Apelação (2026.050.10760) ou classe APELAÇÃO e clicar
    print("Localizando link da Apelação (2026.050.10760)...")
    
    # Capturar texto inicial da tabela
    body_table = frame.inner_text("body")
    print("\n--- RESULTADO DA TABELA INICIAL ---")
    print(body_table[:1000])
    
    # Clicar no link de Apelação
    # O TJRJ renderiza linhas na tabela com links
    link_apelacao = frame.locator("tr:has-text('APELAÇÃO'), tr:has-text('2026.050.10760'), a:has-text('2026.050.10760')").first
    if link_apelacao:
        print("Clicando no registro da Apelação...")
        link_apelacao.click()
        time.sleep(6)
        
        detail_txt = frame.inner_text("body")
        print("\n================ DETALHES COMPLETOS DA APELAÇÃO HOJE (01/10/2026) ================")
        print(detail_txt)
        print("==================================================================================\n")
        
        out_file = r"c:\Projetos\superJus\Clientes\Daniel_Ferreira_Lima\02_Movimentacoes\detalhes_apelacao_01_10_2026.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(detail_txt)
        print(f"Salvo em {out_file}")
    else:
        print("Link da apelação não localizado.")
        
    browser.close()
