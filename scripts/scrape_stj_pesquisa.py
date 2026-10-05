# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

target_url = "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroOrigem&termo=00230135120218190078&totalRegistrosPorPagina=40&aplicacao=processos.ea"

print(f"Abrindo STJ com Playwright e aguardando verificação CSID...")

with sync_playwright() as p:
    # Use launch with channel or args to look like normal Chrome
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled"]
    )
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 900}
    )
    page = ctx.new_page()
    
    # Remove navigator.webdriver flag
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        page.goto(target_url, timeout=60000)
        print("Página carregada, aguardando 15s pela verificação automática do STJ...")
        
        for i in range(6):
            time.sleep(3)
            current_title = page.title()
            print(f"[{i*3}s] Título atual: {current_title}")
            if "pesquisa" in current_title.lower() or "processo" in current_title.lower() or "superior" in current_title.lower():
                break
                
        time.sleep(3)
        page.screenshot(path="c:/Projetos/superJus/stj_resultado_decisao.png")
        
        body_text = page.inner_text("body")
        with open("c:/Projetos/superJus/stj_resultado_decisao.txt", "w", encoding="utf-8") as f:
            f.write(body_text)
            
        print(f"Finalizado! Texto gravado com {len(body_text)} caracteres.")
        
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        browser.close()
