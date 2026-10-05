# -*- coding: utf-8 -*-
"""
SUPERJUS — EXTRAÇÃO COMPLETA DOS DETALHES E MOVIMENTOS PJe (PASTOR JUNEO)
Acessa os autos digitais de 0810659-95.2026.8.19.0203 no PJe
"""

import sys, time, json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

proc_fmt = "0810659-95.2026.8.19.0203"

print("=" * 85)
print(f"🚀 EXTRAINDO DETALHES COMPLETOS DO PROCESSO {proc_fmt} NO PJe...")
print("=" * 85)

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
        time.sleep(5)

    # Clicar no link do processo ou "VER DETALHES DO PROCESSO"
    link_detalhes = page.locator("a:has-text('0810659-95.2026.8.19.0203'), a[title*='detalhes'], a:has-text('VER DETALHES')").first
    
    # Pode abrir em nova aba ou popup
    with ctx.expect_page() as new_page_info:
        print("✓ Clicando para abrir detalhes do processo...")
        link_detalhes.click()
        time.sleep(5)

    detalhe_page = new_page_info.value
    detalhe_page.wait_for_load_state("domcontentloaded")
    time.sleep(4)

    print("✓ Página de detalhes carregada com sucesso!")
    txt_detalhes = detalhe_page.inner_text("body")
    
    # Salvar o texto completo
    out_txt = r"c:\Projetos\superJus\Clientes\Pastor_Juneo\detalhes_completos_pje_04_09_2026.txt"
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(txt_detalhes)
        
    print(f"\nSalvo em {out_txt} ({len(txt_detalhes)} caracteres)")
    print("\n--- LINHAS CAPTURADAS DOS AUTOS ---")
    lines = [l.strip() for l in txt_detalhes.splitlines() if l.strip()]
    for l in lines[:60]:
        print(f"  • {l}")

    browser.close()

print("\n" + "=" * 85)
print("Extração concluída!")
print("=" * 85)
