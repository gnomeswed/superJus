# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== CHECAGEM AO VIVO — SEGUNDA-FEIRA 03/08/2026 (22:25 BRT) ===")

target_dir = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(target_dir, exist_ok=True)

lines_out = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()

    # ---- 1ª Instância: Ação Penal Búzios ----
    try:
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=60000)
        time.sleep(4)

        frame = page.frame_locator("iframe#mainframe")
        frame.locator("input[name='numeroProcesso']").fill("0023013-51.2021.8.19.0078")
        time.sleep(1)
        frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
        time.sleep(6)

        try:
            frame.locator("button:has-text('Todos Os Movimentos')").first.click()
            time.sleep(4)
        except Exception:
            pass

        real_frame = page.query_selector("iframe#mainframe").content_frame()
        txt = real_frame.inner_text("body")
        lines_out.append("=== ACAO PENAL BUZIOS (0023013-51.2021.8.19.0078) — 03/08/2026 22:25 ===")
        lines_out.append(txt)
    except Exception as e:
        lines_out.append(f"Erro Playwright 1a instancia: {e}")

    # ---- 2ª Instância: Habeas Corpus TJRJ ----
    try:
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=60000)
        time.sleep(4)

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
        time.sleep(8)

        try:
            frame.locator("button:has-text('Todos Os Movimentos')").first.click()
            time.sleep(4)
        except Exception:
            pass

        real_frame = page.query_selector("iframe#mainframe").content_frame()
        txt2 = real_frame.inner_text("body")
        lines_out.append("\n\n=== HABEAS CORPUS TJRJ (0029845-67.2026.8.19.0000) — 03/08/2026 22:25 ===")
        lines_out.append(txt2)
    except Exception as e:
        lines_out.append(f"\nErro Playwright 2a instancia: {e}")

    browser.close()

res_txt = "\n".join(lines_out)
target_file = os.path.join(target_dir, "tjrj_live_august3_night.txt")
with open(target_file, "w", encoding="utf-8") as f:
    f.write(res_txt)

print("SUCESSO: Captura salva em " + target_file)
