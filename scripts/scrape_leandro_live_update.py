# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== SCRAPING EM TEMPO REAL TJRJ — LEANDRO DA SILVA (0827233-23.2026.8.19.0001) ===")

target_dir = r"c:\Projetos\superJus\Clientes\Leandro_Mecanico\scraping_2026-08-16"
os.makedirs(target_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 1280, "height": 800})

    try:
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

        frame = page.frame_locator("iframe#mainframe")
        frame.locator("input[name='numeroProcesso']").fill("0827233-23.2026.8.19.0001")
        time.sleep(1)
        frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
        time.sleep(5)

        try:
            frame.locator("button:has-text('Todos Os Movimentos')").first.click()
            time.sleep(3)
        except Exception:
            pass

        real_frame = page.query_selector("iframe#mainframe").content_frame()
        txt = real_frame.inner_text("body")

        novo_txt = os.path.join(target_dir, "tjrj_live_leandro_16_08_2026.txt")
        with open(novo_txt, "w", encoding="utf-8") as f:
            f.write(txt)

        print(f"✅ Extrato salvo com sucesso em: {novo_txt}\n")

        lines = txt.split('\n')
        print("--- ÚLTIMAS MOVIMENTAÇÕES CAPTURADAS NA CONSULTA AO VIVO ---")
        for i, l in enumerate(lines[:40], start=1):
            if l.strip():
                print(f"  {i:02d}. {l.strip()[:120]}")

    except Exception as e:
        print(f"Erro no scraping ao vivo: {e}")

    browser.close()

print("\n=== SCRAPING CONCLUÍDO ===")
