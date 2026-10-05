# -*- coding: utf-8 -*-
import sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
proc_fmt = "0821248-17.2025.8.19.0031"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = ctx.new_page()

    url = "https://tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam"
    page.goto(url, timeout=40000)
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

    # Click on the SENTENÇA link
    sent_link = dp.locator("a:has-text('SENTENÇA')").first
    print("Sentenca link text:", sent_link.inner_text())
    
    # Listen for new page or popup
    try:
        with ctx.expect_page(timeout=8000) as doc_page_info:
            sent_link.click()
        doc_page = doc_page_info.value
        doc_page.wait_for_load_state("domcontentloaded")
        time.sleep(4)
        print("Popup aberto! URL:", doc_page.url)
        txt = doc_page.inner_text("body")
        print("Texto do documento (primeiros 1500 chars):")
        print(txt[:1500])
        with open(r"c:\Projetos\superJus\Clientes\Renan\03_Documentos_do_Processo\texto_sentenca_live.txt", "w", encoding="utf-8") as f:
            f.write(txt)
    except Exception as e:
        print("Não abriu popup nova. Verificando se abriu modal/iframe na mesma página:", e)
        time.sleep(3)
        txt_dp = dp.inner_text("body")
        for f in dp.frames:
            print("Frame:", f.url)
            f_txt = f.inner_text("body")
            if "SENTENÇA" in f_txt:
                print("Encontrado no frame:", f_txt[:1000])

    browser.close()
