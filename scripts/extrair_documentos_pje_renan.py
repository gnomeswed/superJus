# -*- coding: utf-8 -*-
import sys, time, re, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

proc_fmt = "0821248-17.2025.8.19.0031"
print(f"📖 EXTRAINDO DECISÕES E ANTECEDENTES DO PJe — PROCESSO {proc_fmt}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
    ctx = browser.new_context(
        viewport={"width": 1400, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()

    url = "https://tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam"
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
        with ctx.expect_page(timeout=15000) as new_page_info:
            link_detalhes.click()
            time.sleep(3)

        dp = new_page_info.value
        dp.wait_for_load_state("domcontentloaded")
        time.sleep(4)

        # Encontrar links de documentos
        doc_links = dp.locator("a:has-text('SENTENÇA'), a:has-text('DECISÃO'), a[title*='Visualizar']")
        count = doc_links.count()
        print(f"Encontrados {count} elementos de decisão/documento.")
        
        # Coletar todo o HTML da página de detalhes para análise de atributos e IDs de documentos
        html = dp.content()
        with open(r"c:\Projetos\superJus\Clientes\Renan\03_Documentos_do_Processo\pje_detalhe_completo.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("HTML da página salvo.")
        
        # Procurar por números de processos anteriores no HTML (ex: 00... ou 08...)
        matches = set(re.findall(r"\b0\d{6}-\d{2}\.\d{4}\.8\.19\.\d{4}\b", html))
        print(f"\nNúmeros CNJ encontrados no HTML: {matches}")
        
        # Procurar menções a VEP ou Execução
        for line in html.splitlines():
            if any(k in line.lower() for k in ["execu", "vep", "evas", "fuga", "reincid", "fac"]):
                clean_l = re.sub(r"<[^>]+>", " ", line).strip()
                if len(clean_l) > 10:
                    print(f"  • {clean_l[:200]}")

    browser.close()
