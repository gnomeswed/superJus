# -*- coding: utf-8 -*-
"""
Consulta da Execução Penal (VEP / SEEU) de Lucas de Souza Freitas referente ao processo de 2019
"""
import os
import sys
import time
import json

sys.stdout.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

from playwright.sync_api import sync_playwright

OUT_DIR = r"C:\Projetos\superJus\Clientes\Lucas_Freitas\05_Processos_Anteriores\Processos_2019"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1280, "height": 800}, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = ctx.new_page()

    # 1. Consulta por Nome na VEP (Competência: Execução Penal)
    print(">> Acessando TJRJ Consulta Pública...", flush=True)
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
    time.sleep(4)
    frame = page.frame_locator("iframe#mainframe")

    frame.locator("#nav-porNome").click()
    time.sleep(2)

    frame.locator("#porNome #filtroOrigem1").fill("1ª Instância")
    time.sleep(1)
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    time.sleep(1)

    frame.locator("#porNome #filtroComarca1").fill("Capital")
    time.sleep(1)
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    time.sleep(1)

    frame.locator("#porNome #filtroCompetencia1").fill("Execuções Penais")
    time.sleep(1)
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    time.sleep(1)

    frame.locator("#porNome #nomeParte").fill("Lucas de Souza Freitas")
    time.sleep(1)

    frame.locator("#porNome #anoInicial1").fill("2017")
    frame.locator("#porNome #anoFinal1").fill("2026")
    time.sleep(1)

    try:
        chk = frame.locator("#porNome #procEmAndamento2").first
        if chk.is_checked():
            chk.uncheck()
    except:
        pass

    time.sleep(1)
    frame.locator("#porNome button").first.click()
    print("Aguardando resposta da VEP...")
    time.sleep(12)

    real_frame = page.query_selector("iframe#mainframe").content_frame()
    body_txt = real_frame.inner_text("body")
    with open(os.path.join(OUT_DIR, "vep_resultado_lucas.txt"), "w", encoding="utf-8") as f:
        f.write(body_txt)
    page.screenshot(path=os.path.join(OUT_DIR, "vep_resultado.png"), full_page=True)

    print("\n--- Resultado na VEP (Execuções Penais): ---")
    for line in [l.strip() for l in body_txt.split('\n') if l.strip()][:30]:
        print(f"  {line}")

    browser.close()
