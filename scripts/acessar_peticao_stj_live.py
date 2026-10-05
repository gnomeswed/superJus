# -*- coding: utf-8 -*-
import sys
import time
import os
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

num_reg = "202603112107"
url = f"https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo={num_reg}&totalRegistrosPorPagina=40&aplicacao=processos.ea"

print(f"Acessando STJ para buscar a petição 1025001/2026: {url}")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
    )
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36",
        locale="pt-BR"
    )
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        time.sleep(6)
        
        # Salvar screenshot inicial
        page.screenshot(path="c:/Projetos/superJus/stj_pagina_inicial.png")
        
        # Procurar elemento da aba Petições
        print("Buscando aba Petições...")
        peticoes_tab = page.locator("text=Petições, a:has-text('Petições'), li:has-text('Petições')")
        if peticoes_tab.count() > 0:
            print("Clicando na aba Petições...")
            peticoes_tab.first.click()
            time.sleep(5)
            page.screenshot(path="c:/Projetos/superJus/stj_aba_peticoes.png")
        
        body_text = page.inner_text("body")
        print("\n=== TRECHO DO TEXTO NA ABA ===")
        for line in body_text.splitlines():
            l_strip = line.strip()
            if l_strip and any(k in l_strip.lower() for k in ["1025001", "razões", "razoes", "petição", "peticao", "gabriel", "16:01", "documento"]):
                print(">>", l_strip)
                
        # Procurar links específicos de download ou visualização
        links = page.eval_on_selector_all("a", "elements => elements.map(e => ({text: e.innerText.trim(), href: e.href, onclick: e.getAttribute('onclick')}))")
        print("\n=== LINKS RELACIONADOS A PETIÇÃO / DOCUMENTO ===")
        matching_links = []
        for l in links:
            t = (l.get("text") or "") + " " + (l.get("href") or "") + " " + (str(l.get("onclick")) or "")
            if any(k in t.lower() for k in ["1025001", "peticao", "petição", "documento", "download", "visualizar", "pdf"]):
                matching_links.append(l)
                print(l)
                
        # Se houver link direto ou onclick para ver a petição, tentar clicar ou navegar
        for l in matching_links:
            if "1025001" in str(l) or "peticao" in str(l).lower():
                print(f"\nTentando acessar link: {l}")
                
    except Exception as e:
        print(f"Erro ao acessar STJ: {e}")
    finally:
        browser.close()

print("\n=== FIM DA CONSULTA ===")
