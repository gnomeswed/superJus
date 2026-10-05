# -*- coding: utf-8 -*-
"""
SUPERJUS — TENTATIVA DE VISUALIZAR DESPACHOS DO PJe DE LEANDRO
Processo: 0827233-23.2026.8.19.0001
"""
import sys, time, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

proc_fmt = "0827233-23.2026.8.19.0001"

print("=" * 85, flush=True)
print(f"🏛️ ABRINDO DOCUMENTOS PJe 1G TJRJ — PROCESSO {proc_fmt} (LEANDRO)", flush=True)
print("=" * 85, flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
    ctx = browser.new_context(
        viewport={"width": 1400, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()

    url = "https://tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam"
    print(f"1. Acessando {url}...", flush=True)
    page.goto(url, timeout=30000, wait_until="domcontentloaded")
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

        # Localizar links/botões de visualização de documentos
        doc_links = dp.query_selector_all("a:has-text('VISUALIZAR DOCUMENTOS'), a[title*='documento'], a[title*='Documento']")
        print(f"Total de links de documentos encontrados: {len(doc_links)}", flush=True)

        # Clicar no primeiro documento (o mais recente - Despacho de 02/09/2026)
        if doc_links:
            print("Tentando abrir o primeiro documento (mais recente)...", flush=True)
            try:
                with ctx.expect_page(timeout=8000) as doc_page_info:
                    doc_links[0].click()
                    time.sleep(3)
                doc_p = doc_page_info.value
                doc_p.wait_for_load_state("domcontentloaded")
                time.sleep(3)
                doc_txt = doc_p.inner_text("body")
                print("Texto do documento recente capturado:\n", flush=True)
                print(doc_txt[:1000], flush=True)
                out_doc = r"c:\Projetos\superJus\Clientes\Leandro_Mecanico\ultimo_despacho_pje_02_09_2026.txt"
                with open(out_doc, "w", encoding="utf-8") as f:
                    f.write(doc_txt)
            except Exception as e:
                print(f"Não abriu nova aba ou precisa de certidão/segredo: {e}", flush=True)
                # Tentar ver se abriu modal ou iframe
                modals = dp.query_selector_all(".modal, iframe, div[id*='documento']")
                print(f"Modals/iframes encontrados: {len(modals)}", flush=True)
    browser.close()

print("\n=== CONCLUÍDO ===", flush=True)
