# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== INTERATIVE PLAYWRIGHT SCRAPING — PJe CONSULTA PÚBLICA ===")

target_dir = r"c:\Projetos\superJus\Clientes\Leandro_Mecanico\scraping_2026-08-16"
os.makedirs(target_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})

    url = "https://tjrj.pje.jus.br/pje/ConsultaPublica/listView.seam"
    print(f"1. Navegando para {url}...")
    page.goto(url, wait_until="networkidle", timeout=30000)
    time.sleep(2)

    # Preencher o número do processo completo no campo correspondente
    inp_num = page.locator("input[id*='numProcesso-inputNumeroProcesso']").first
    if inp_num.is_visible():
        print("   • Campo numProcesso localizado!")
        inp_num.fill("0827233-23.2026.8.19.0001")
        time.sleep(1)

    # Procurar o botão Pesquisar
    btn_search = page.locator("input[id*='searchProcessos'], button[id*='searchProcessos']").first
    if btn_search.is_visible():
        print("   • Clicando no botão Pesquisar...")
        btn_search.click()
        time.sleep(5)

    # Salvar screenshot e texto
    ss = os.path.join(target_dir, "pje_consulta_interativa_resultado.png")
    page.screenshot(path=ss)
    print(f"   • Screenshot salvo: {ss}")

    txt = page.inner_text("body")
    out = os.path.join(target_dir, "pje_consulta_interativa_texto.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write(txt)

    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    print("\n--- RESULTADO OBTIDO NA BUSCA INTERATIVA ---")
    for l in lines[:30]:
        print(f"  • {l[:120]}")

    browser.close()

print("\n=== CONSULTA PÚBLICA INTERATIVA FINALIZADA ===")
