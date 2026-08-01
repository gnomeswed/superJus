# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print("Iniciando raspagem no Portal TJRJ para Lucas de Souza Freitas...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=30000, wait_until="domcontentloaded")
    time.sleep(3)
    
    iframe_el = page.query_selector("iframe#mainframe")
    if iframe_el:
        frame = iframe_el.content_frame()
        if frame:
            # Buscar link / aba de busca por nome
            frame.evaluate("""() => {
                const elements = Array.from(document.querySelectorAll('*'));
                const el = elements.find(e => e.textContent && e.textContent.trim().toLowerCase() === 'por nome');
                if (el) el.click();
            }""")
            time.sleep(2)
            
            # Preencher campo de nome
            name_input = frame.query_selector("input[type='text']")
            if name_input:
                name_input.fill("LUCAS DE SOUZA FREITAS")
                time.sleep(1)
                
                # Clicar no botão Pesquisar
                frame.evaluate("""() => {
                    const btns = Array.from(document.querySelectorAll('button'));
                    const btn = btns.find(b => b.textContent && b.textContent.trim().toLowerCase().includes('pesquisar'));
                    if (btn) btn.click();
                }""")
                print("Aguardando carregamento da pesquisa por nome...")
                time.sleep(8)
                
                page.screenshot(path="tjrj_resultado_nome.png")
                body_text = frame.inner_text("body")
                
                with open("tjrj_resultado_nome.txt", "w", encoding="utf-8") as f:
                    f.write(body_text)
                    
                print("Resultado extraído e salvo em tjrj_resultado_nome.txt!")
                print(body_text[:1500])

    browser.close()
