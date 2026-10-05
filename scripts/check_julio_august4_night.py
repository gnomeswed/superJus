# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== CHECAGEM AO VIVO TJRJ — TERÇA-FEIRA 04/08/2026 (18:38 BRT) ===")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()

    # ---- 1ª Instância: Ação Penal Búzios ----
    try:
        print("\n--- 1ª Instância: Ação Penal Búzios (0023013-51.2021.8.19.0078) ---")
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=15000)
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
        for l in lines[:25]:
            print(f"  {l}")
    except Exception as e:
        print(f"Erro Playwright 1a instancia: {e}")

    # ---- 2ª Instância: Habeas Corpus TJRJ ----
    try:
        print("\n--- 2ª Instância: Habeas Corpus TJRJ (0029845-67.2026.8.19.0000) ---")
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=15000)
        time.sleep(2)

        frame = page.frame_locator("iframe#mainframe")
        try:
            inp_origem = frame.locator("#filtroOrigem1")
            inp_origem.fill("Tribunal de Justiça")
            time.sleep(1)
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")
        except Exception:
            pass
        time.sleep(1)

        frame.locator("input[name='numeroProcesso']").fill("0029845-67.2026.8.19.0000")
        time.sleep(1)
        frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
        time.sleep(5)

        try:
            frame.locator("button:has-text('Todos Os Movimentos')").first.click()
            time.sleep(2)
        except Exception:
            pass

        real_frame = page.query_selector("iframe#mainframe").content_frame()
        txt2 = real_frame.inner_text("body")
        lines2 = [l.strip() for l in txt2.split('\n') if l.strip()]
        for l in lines2[:25]:
            print(f"  {l}")
    except Exception as e:
        print(f"Erro Playwright 2a instancia: {e}")

    browser.close()

print("\n=== CHECAGEM CONCLUÍDA ===")
