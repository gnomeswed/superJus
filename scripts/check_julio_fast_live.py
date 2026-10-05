# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== CHECAGEM RÁPIDA DE MOVIMENTAÇÕES TJRJ — 05/08/2026 (16:48 BRT) ===")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()

    try:
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=12000)
        time.sleep(2)

        frame = page.frame_locator("iframe#mainframe")
        frame.locator("input[name='numeroProcesso']").fill("0023013-51.2021.8.19.0078")
        time.sleep(1)
        frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
        time.sleep(4)

        try:
            frame.locator("button:has-text('Todos Os Movimentos')").first.click()
            time.sleep(2)
        except Exception:
            pass

        real_frame = page.query_selector("iframe#mainframe").content_frame()
        txt = real_frame.inner_text("body")
        lines = [l.strip() for l in txt.split('\n') if l.strip()]
        
        print("\n📌 Movimentações Recentes (Ação Penal Búzios):")
        in_mov = False
        mov_count = 0
        for l in lines:
            if "Movimentação" in l or "Tipo do Movimento" in l:
                in_mov = True
            if in_mov:
                print(f"  • {l}")
                mov_count += 1
                if mov_count > 25:
                    break

    except Exception as e:
        print(f"Erro: {e}")

    browser.close()

print("\n=== FIM DA CHECAGEM ===")
