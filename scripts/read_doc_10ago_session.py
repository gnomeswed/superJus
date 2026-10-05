# -*- coding: utf-8 -*-
import sys, time, json, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

proc_fmt = "0808595-36.2026.8.19.0002"
doc_url = "https://tjrj.pje.jus.br/pje/ConsultaPublica/DetalheProcessoConsultaPublica/documentoSemLoginHTML.seam?ca=4a247d1cb6b5d70efb49632a1a9c2981bb17ad1d126a7141688df8af4889ac55d67699f5e5c3915cbfe2e31a6753fddcdaab9db4fbc6c8b0&idProcessoDoc=299734030"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
    ctx = browser.new_context(
        viewport={"width": 1400, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()
    url = "https://tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam"
    print("1. Abrindo consulta pública...")
    page.goto(url, timeout=35000, wait_until="domcontentloaded")
    time.sleep(2)
    page.fill("input[id*='inputNumeroProcesso']", proc_fmt)
    time.sleep(1)
    btn = page.query_selector("input[id*='searchProcessos'], button[id*='searchProcessos']")
    if btn:
        btn.click()
        time.sleep(4)
    
    link_detalhes = page.locator(f"a:has-text('{proc_fmt}'), a[title*='detalhes'], a:has-text('VER DETALHES')").first
    if link_detalhes.is_visible():
        with ctx.expect_page(timeout=15000) as new_page_info:
            link_detalhes.click()
            time.sleep(3)
        dp = new_page_info.value
        dp.wait_for_load_state("domcontentloaded")
        time.sleep(3)
        
        print("2. Abrindo documento de 10/08/2026 dentro da mesma sessão...")
        p_doc = ctx.new_page()
        p_doc.goto(doc_url, timeout=20000, wait_until="domcontentloaded")
        time.sleep(3)
        doc_text = p_doc.inner_text("body")
        print("\n========================================================")
        print("TEOR REAL DA DECISÃO DE 10/08/2026:")
        print("========================================================")
        print(doc_text)
        print("========================================================\n")
        with open(r"c:\Projetos\superJus\Clientes\Lucas_Dias_Oliveira\03_Documentos_do_Processo\decisao_10_08_2026_REAL.txt", "w", encoding="utf-8") as f:
            f.write(doc_text)
