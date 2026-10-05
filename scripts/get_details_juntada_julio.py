# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== EXTRAINDO DETALHES DA JUNTADA DE HOJE (04/08/2026) ===")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()

    try:
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

        frame = page.frame_locator("iframe#mainframe")
        frame.locator("input[name='numeroProcesso']").fill("0023013-51.2021.8.19.0078")
        time.sleep(1)
        frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
        time.sleep(5)

        # Try to click "Todos os Movimentos"
        try:
            frame.locator("button:has-text('Todos Os Movimentos')").first.click()
            time.sleep(3)
        except Exception:
            pass

        real_frame = page.query_selector("iframe#mainframe").content_frame()
        
        # Take a screenshot for inspection
        screenshot_path = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\analises_e_automacoes_ia\paginas_renderizadas\juntada_04082026.png"
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        page.screenshot(path=screenshot_path)
        print(f"Screenshot salva em: {screenshot_path}")

        # Extract all table rows or elements in movement area
        mov_elements = real_frame.query_selector_all("tr, div.movimento, div.row, li")
        print("\n--- ELEMENTOS DA MOVIMENTAÇÃO DE HOJE (04/08/2026) ---")
        found = False
        for el in mov_elements:
            txt = el.inner_text().strip()
            if "04/08/2026" in txt or "Juntada" in txt:
                print(f"• {txt}")
                found = True
                
                # Check for links or clickable icons inside this element
                links = el.query_selector_all("a, button, img, i")
                for link in links:
                    title = link.get_attribute("title") or link.get_attribute("href") or link.inner_text()
                    if title:
                        print(f"   [Link/Ícone]: {title}")

        if not found:
            print("Buscando texto completo no frame:")
            txt_all = real_frame.inner_text("body")
            print(txt_all[:2000])

    except Exception as e:
        print(f"Erro ao extrair detalhes: {e}")

    browser.close()

print("\n=== EXTRAÇÃO CONCLUÍDA ===")
