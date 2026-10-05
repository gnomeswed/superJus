# -*- coding: utf-8 -*-
import time
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    page = browser.new_page()
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=40000)
    time.sleep(3)
    
    frame_el = page.wait_for_selector("iframe#mainframe", timeout=20000)
    frame = frame_el.content_frame()
    
    frame.locator("input[name='numeroProcesso']").fill("0004301-33.2018.8.19.0073")
    frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
    time.sleep(5)
    
    # Encontrar todos os links na tabela de resultados
    links = frame.locator("a").all()
    print(f"Total de links encontrados: {len(links)}")
    
    target_link = None
    for l in links:
        txt = l.inner_text().strip()
        if "2026.050.10760" in txt or "APELAÇÃO" in txt:
            print(f"Link alvo encontrado: '{txt}'")
            target_link = l
            break
            
    if target_link:
        target_link.click()
        time.sleep(5)
        
        detail_txt = frame.inner_text("body")
        print("\n=== TEOR DA APELAÇÃO NO TJRJ HOJE (01/10/2026) ===")
        print(detail_txt)
        
        with open(r"c:\Projetos\superJus\Clientes\Daniel_Ferreira_Lima\02_Movimentacoes\detalhes_apelacao_hoje_01_10_2026.txt", "w", encoding="utf-8") as f:
            f.write(detail_txt)
    else:
        print("Link 2026.050.10760 não encontrado entre os elementos <a>.")
        # Imprime o HTML da tabela
        print(frame.locator("table").inner_html() if frame.locator("table").count() > 0 else "Sem tabela")
        
    browser.close()
