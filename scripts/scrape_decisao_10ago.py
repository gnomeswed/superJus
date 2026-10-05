# -*- coding: utf-8 -*-
import sys, time, json, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

proc_fmt = "0808595-36.2026.8.19.0002"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
    ctx = browser.new_context(
        viewport={"width": 1400, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()

    url = "https://tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam"
    print("1. Acessando PJe...")
    page.goto(url, timeout=40000, wait_until="domcontentloaded")
    time.sleep(2)

    page.fill("input[id*='inputNumeroProcesso']", proc_fmt)
    time.sleep(1)

    btn = page.query_selector("input[id*='searchProcessos'], button[id*='searchProcessos']")
    if btn:
        btn.click()
        time.sleep(5)

    link_detalhes = page.locator(f"a:has-text('{proc_fmt}'), a[title*='detalhes'], a:has-text('VER DETALHES')").first
    if link_detalhes.is_visible():
        print("2. Abrindo detalhes...")
        with ctx.expect_page(timeout=15000) as new_page_info:
            link_detalhes.click()
            time.sleep(3)

        dp = new_page_info.value
        dp.wait_for_load_state("domcontentloaded")
        time.sleep(4)

        # Let's find the document links in dp
        links = dp.locator("a").all()
        print(f"Total links na página de detalhes: {len(links)}")
        doc_10ago_links = []
        for l in links:
            t = l.inner_text().strip()
            title = l.get_attribute("title") or ""
            onclick = l.get_attribute("onclick") or ""
            href = l.get_attribute("href") or ""
            if "10/08" in t or "10/08" in title or "DECIS" in t or "VISUALIZAR" in t:
                print(f"LINK: text='{t}' | title='{title}' | onclick='{onclick[:60]}' | href='{href[:60]}'")
                doc_10ago_links.append(l)

        # Also let's inspect the entire HTML of the table of documents
        docs_table = dp.locator("table[id*='documentos'], div[id*='documentos'], table[id*='processoDocumentoGrid']").first
        if docs_table.is_visible():
            print("Tabela de documentos encontrada!")
            html_content = docs_table.inner_html()
            with open(r"c:\Projetos\superJus\Clientes\Lucas_Dias_Oliveira\03_Documentos_do_Processo\tabela_docs.html", "w", encoding="utf-8") as f:
                f.write(html_content)
            print("HTML da tabela de documentos salvo.")

        # Let's try clicking the first link near 10/08/2026
        target_link = dp.locator("tr:has-text('10/08/2026') a:has-text('VISUALIZAR'), tr:has-text('10/08/2026') a").first
        if target_link.is_visible():
            print("3. Clicando no link da decisão de 10/08...")
            # PJe usually opens document in a popup or new tab or iframe
            try:
                with ctx.expect_page(timeout=8000) as p_doc:
                    target_link.click()
                    time.sleep(2)
                p_doc_val = p_doc.value
                p_doc_val.wait_for_load_state("domcontentloaded")
                time.sleep(3)
                txt = p_doc_val.inner_text("body")
                print("--- CONTEÚDO DA DECISÃO DE 10/08/2026 ---")
                print(txt[:3000])
                with open(r"c:\Projetos\superJus\Clientes\Lucas_Dias_Oliveira\03_Documentos_do_Processo\decisao_10_08_2026.txt", "w", encoding="utf-8") as f:
                    f.write(txt)
            except Exception as e:
                print(f"Não abriu popup direto: {e}")
                # check if modal or iframe appeared on dp
                time.sleep(3)
                txt_dp = dp.inner_text("body")
                with open(r"c:\Projetos\superJus\Clientes\Lucas_Dias_Oliveira\03_Documentos_do_Processo\dp_after_click.txt", "w", encoding="utf-8") as f:
                    f.write(txt_dp)
                print("Página principal salva após clique.")
