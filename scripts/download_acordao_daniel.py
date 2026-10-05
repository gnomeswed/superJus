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
    
    link = frame.locator("a:has-text('2026.050.10760')").first
    if link:
        link.click()
        time.sleep(4)
        
        # Clicar no link do Acórdão
        acordao_link = frame.locator("a:has-text('Acórdão'), a:has-text('24/09/2026')").first
        if acordao_link:
            print("Clicando no link do Acórdão...")
            # Pode abrir popup ou navegar
            with page.expect_popup() as popup_info:
                try:
                    acordao_link.click(timeout=5000)
                    popup = popup_info.value
                    popup.wait_for_load_state()
                    txt_acordao = popup.inner_text("body")
                    print("\n=== TEOR DO ACÓRDÃO ===")
                    print(txt_acordao[:3000])
                    with open(r"c:\Projetos\superJus\Clientes\Daniel_Ferreira_Lima\03_Documentos_do_Processo\acordao_apelacao_24_09_2026.txt", "w", encoding="utf-8") as f:
                        f.write(txt_acordao)
                except Exception as e:
                    print(f"Não abriu popup direto: {e}")
                    # Tenta ver se abriu no mesmo frame
                    txt_frame = frame.inner_text("body")
                    with open(r"c:\Projetos\superJus\Clientes\Daniel_Ferreira_Lima\03_Documentos_do_Processo\acordao_apelacao_24_09_2026.txt", "w", encoding="utf-8") as f:
                        f.write(txt_frame)
                        
    browser.close()
