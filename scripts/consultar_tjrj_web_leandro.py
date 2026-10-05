# -*- coding: utf-8 -*-
"""
Scraping do portal público TJRJ para pegar os textos integrais dos despachos e decisões de Leandro
Processo: 0827233-23.2026.8.19.0001
"""
import time, os, sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

print("=== SCRAPING TJRJ CONSULTA PROCESSUAL — LEANDRO DA SILVA ===", flush=True)

target_file = r"c:\Projetos\superJus\Clientes\Leandro_Mecanico\tjrj_live_leandro_04_09_2026.txt"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 1400, "height": 900})

    try:
        print("1. Acessando portal TJRJ...", flush=True)
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

        print("2. Preenchendo número...", flush=True)
        frame = page.frame_locator("iframe#mainframe")
        frame.locator("input[name='numeroProcesso']").fill("0827233-23.2026.8.19.0001")
        time.sleep(1)
        frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
        time.sleep(5)

        try:
            btn_todos = frame.locator("button:has-text('Todos Os Movimentos')").first
            if btn_todos.is_visible():
                btn_todos.click()
                time.sleep(3)
        except Exception as e:
            print(f"Aviso ao clicar em todos os movimentos: {e}", flush=True)

        real_frame = page.query_selector("iframe#mainframe").content_frame()
        txt = real_frame.inner_text("body")

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(txt)

        print(f"✅ Extrato salvo com sucesso em: {target_file}", flush=True)

        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        print(f"\n--- ÚLTIMAS 50 LINHAS DA CONSULTA TJRJ ({len(lines)} linhas no total) ---", flush=True)
        for i, l in enumerate(lines[:50], start=1):
            print(f"  {i:02d}. {l}", flush=True)

    except Exception as e:
        print(f"Erro no scraping ao vivo: {e}", flush=True)

    browser.close()

print("\n=== FIM ===", flush=True)
