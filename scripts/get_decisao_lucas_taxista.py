# -*- coding: utf-8 -*-
import sys, time, json, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

proc_fmt = "0808595-36.2026.8.19.0002"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
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

        # Clicar no documento da decisão de 10/08/2026
        # Procurar linha que tenha 10/08/2026
        row = dp.locator("tr:has-text('10/08/2026')").first
        print("Linha de 10/08/2026 encontrada:")
        print(row.inner_text())

        # Clicar no link de visualização
        btn_doc = row.locator("a:has-text('VISUALIZAR'), a[title*='Visualizar'], a").first
        if btn_doc.is_visible():
            with ctx.expect_page(timeout=15000) as doc_page_info:
                btn_doc.click()
                time.sleep(3)
            doc_p = doc_page_info.value
            doc_p.wait_for_load_state("domcontentloaded")
            time.sleep(4)
            decisao_txt = doc_p.inner_text("body")
            out_file = r"c:\Projetos\superJus\Clientes\Lucas_Dias_Oliveira\03_Documentos_do_Processo\decisao_liberdade_10_08_2026.txt"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(decisao_txt)
            print(f"Decisão salva em: {out_file}")
            print("\n=== CONTEÚDO DA DECISÃO DE 10/08/2026 ===")
            print(decisao_txt[:2000])

    browser.close()
