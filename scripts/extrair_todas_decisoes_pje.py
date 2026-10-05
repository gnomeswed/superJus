# -*- coding: utf-8 -*-
import sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
proc_fmt = "0821248-17.2025.8.19.0031"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = ctx.new_page()

    page.goto("https://tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam", timeout=40000)
    time.sleep(2)

    page.fill("input[id*='inputNumeroProcesso']", proc_fmt)
    page.click("input[id*='searchProcessos'], button[id*='searchProcessos']")
    time.sleep(4)

    with ctx.expect_page(timeout=15000) as new_page_info:
        page.locator(f"a:has-text('{proc_fmt}')").first.click()
        time.sleep(2)

    dp = new_page_info.value
    dp.wait_for_load_state("domcontentloaded")
    time.sleep(3)

    # Click on DECISÃO links
    dec_links = dp.locator("a:has-text('DECISÃO')")
    count = dec_links.count()
    print(f"Total de links de decisão: {count}")
    
    for i in range(count):
        link = dec_links.nth(i)
        link_text = link.inner_text().strip()
        print(f"\n--- Clicando no link [{i}]: {link_text} ---")
        try:
            with ctx.expect_page(timeout=6000) as doc_page_info:
                link.click()
            doc_page = doc_page_info.value
            doc_page.wait_for_load_state("domcontentloaded")
            time.sleep(3)
            txt = doc_page.inner_text("body")
            print(f"Tamanho do texto: {len(txt)}")
            out_file = rf"c:\Projetos\superJus\Clientes\Renan\03_Documentos_do_Processo\decisao_{i}.txt"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(txt)
            print(f"Salvo em: {out_file}")
            # Mostrar trechos com antecedentes ou evasão
            for l in txt.splitlines():
                if any(k in l.lower() for k in ["evas", "fuga", "vep", "antecedent", "reincid", "processo", "vara", "comarca", "condenad"]):
                    print("  •", l.strip()[:180])
            doc_page.close()
        except Exception as e:
            print(f"Erro ao abrir link [{i}]: {e}")

    browser.close()
