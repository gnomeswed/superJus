# -*- coding: utf-8 -*-
import sys, time, json, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

proc_fmt = "0808595-36.2026.8.19.0002"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
    ctx = browser.new_context(viewport={"width": 1400, "height": 900})
    page = ctx.new_page()

    url = "https://tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam"
    page.goto(url, timeout=35000, wait_until="domcontentloaded")
    time.sleep(2)

    page.fill("input[id*='inputNumeroProcesso']", proc_fmt)
    time.sleep(1)

    btn = page.query_selector("input[id*='searchProcessos'], button[id*='searchProcessos']")
    if btn:
        btn.click()
        time.sleep(5)

    link_detalhes = page.locator(f"a:has-text('{proc_fmt}'), a[title*='detalhes'], a:has-text('VER DETALHES')").first
    
    if link_detalhes.is_visible():
        with ctx.expect_page(timeout=15000) as new_page_info:
            link_detalhes.click()
            time.sleep(3)

        dp = new_page_info.value
        dp.wait_for_load_state("domcontentloaded")
        time.sleep(4)

        # Look for the document of 10/08/2026
        # Let's find all document links
        docs = dp.locator("a[onclick*='abrirDocumento'], a:has-text('DECISÃO'), a:has-text('10/08/2026')").all()
        print(f"Links encontrados: {len(docs)}")
        
        # Let's find all elements in the documents table
        rows = dp.locator("tr").all()
        for r in rows:
            txt = r.inner_text()
            if "10/08/2026" in txt or "DECISÃO" in txt or "INDEFER" in txt.upper() or "REVOG" in txt.upper():
                print(f"LINHA: {txt}")

        # Let's try clicking the first decision of 10/08/2026 to see the text
        dec_btn = dp.locator("tr:has-text('10/08/2026') a").first
        if dec_btn.is_visible():
            print("Clicando na decisão de 10/08/2026...")
            try:
                with ctx.expect_page(timeout=10000) as doc_page_info:
                    dec_btn.click()
                    time.sleep(2)
                doc_p = doc_page_info.value
                doc_p.wait_for_load_state("domcontentloaded")
                time.sleep(3)
                print("Texto da Decisão de 10/08/2026:")
                print(doc_p.inner_text("body")[:3000])
            except Exception as e:
                print(f"Não abriu popup direto: {e}")
                # check if it opened in an iframe or same page
                frames = dp.frames
                print(f"Frames: {len(frames)}")
                for f in frames:
                    print(f"Frame text: {f.inner_text('body')[:500]}")
