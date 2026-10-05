# -*- coding: utf-8 -*-
import sys, time, json, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

proc_fmt = "0808595-36.2026.8.19.0002"

print(f"🏛️ CONSULTA PJe 1G TJRJ AO VIVO — PROCESSO {proc_fmt} (LUCAS DIAS OLIVEIRA - TAXISTA)")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
    ctx = browser.new_context(
        viewport={"width": 1400, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()

    url = "https://tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam"
    print(f"1. Acessando {url}...")
    page.goto(url, timeout=35000, wait_until="domcontentloaded")
    time.sleep(2)

    print(f"2. Preenchendo número {proc_fmt}...")
    page.fill("input[id*='inputNumeroProcesso']", proc_fmt)
    time.sleep(1)

    btn = page.query_selector("input[id*='searchProcessos'], button[id*='searchProcessos']")
    if btn:
        btn.click()
        time.sleep(5)

    res_body = page.inner_text("body")
    print(f"3. Resposta da busca recebida ({len(res_body)} caracteres).")

    link_detalhes = page.locator(f"a:has-text('{proc_fmt}'), a[title*='detalhes'], a:has-text('VER DETALHES')").first
    
    if link_detalhes.is_visible():
        print("✓ Link de detalhes do processo localizado! Abrindo autos digitais...")
        with ctx.expect_page(timeout=15000) as new_page_info:
            link_detalhes.click()
            time.sleep(3)

        dp = new_page_info.value
        dp.wait_for_load_state("domcontentloaded")
        time.sleep(4)

        txt_detalhes = dp.inner_text("body")
        out_txt = r"c:\Projetos\superJus\Clientes\Lucas_Dias_Oliveira\03_Documentos_do_Processo\detalhes_pje_lucas_taxista_live.txt"
        with open(out_txt, "w", encoding="utf-8") as f:
            f.write(txt_detalhes)
        print(f"✅ Detalhes salvos com sucesso em: {out_txt}")
        print("\n--- ÚLTIMAS LINHAS EXTRAÍDAS DO PJe ---")
        lines = [l.strip() for l in txt_detalhes.splitlines() if l.strip()]
        for l in lines[-40:]:
            print(f"  • {l}")
    else:
        print("⚠️ Link de detalhes não encontrado diretamente na tabela.")
        print(res_body[:1000])

    browser.close()
