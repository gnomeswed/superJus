# -*- coding: utf-8 -*-
"""
SUPERJUS — BAIXAR / EXTRAIR ATA DA AUDIÊNCIA E DESPACHO DE ONTEM (03/09/2026) DO PASTOR JUNEO
"""

import sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

proc_fmt = "0810659-95.2026.8.19.0203"

print("=" * 80)
print(f"📖 ABRINDO ATA DA AUDIÊNCIA E DESPACHO DE 03/09/2026 NO PJe...")
print("=" * 80)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
    ctx = browser.new_context(
        viewport={"width": 1400, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()

    url = "https://tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam"
    page.goto(url, timeout=25000, wait_until="domcontentloaded")
    time.sleep(2)

    page.fill("input[id*='inputNumeroProcesso']", proc_fmt)
    time.sleep(1)
    btn = page.query_selector("input[id*='searchProcessos'], button[id*='searchProcessos']")
    if btn:
        btn.click()
        time.sleep(4)

    link_detalhes = page.locator("a:has-text('0810659-95.2026.8.19.0203'), a[title*='detalhes'], a:has-text('VER DETALHES')").first
    with ctx.expect_page() as new_page_info:
        link_detalhes.click()
        time.sleep(4)

    dp = new_page_info.value
    dp.wait_for_load_state("domcontentloaded")
    time.sleep(3)

    # Procurar links de documentos anexos na tabela de documentos
    doc_links = dp.locator("a:has-text('DESPACHO'), a:has-text('Ata da Audiência'), a[title*='Visualizar']")
    count = doc_links.count()
    print(f"Links de documentos encontrados: {count}")

    # Tentar extrair o conteúdo do despacho clicando ou abrindo popup
    for i in range(min(count, 3)):
        try:
            dl = doc_links.nth(i)
            txt_btn = dl.inner_text()
            print(f"\nTentando abrir documento {i+1}: {txt_btn}")
            
            with ctx.expect_page(timeout=10000) as doc_page_info:
                dl.click()
                time.sleep(3)
                
            p_doc = doc_page_info.value
            p_doc.wait_for_load_state("domcontentloaded")
            time.sleep(2)
            txt_c = p_doc.inner_text("body")
            print(f"Texto do documento {i+1} capturado ({len(txt_c)} chars):")
            print(txt_c[:1500])
            with open(rf"c:\Projetos\superJus\Clientes\Pastor_Juneo\doc_{i+1}_03_09_2026.txt", "w", encoding="utf-8") as f:
                f.write(txt_c)
        except Exception as e:
            print(f"Erro ao abrir doc {i+1}: {e}")

    browser.close()

print("\n" + "=" * 80)
print("Fim da extração de documentos.")
print("=" * 80)
