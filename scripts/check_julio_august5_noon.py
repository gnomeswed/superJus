# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== CHECAGEM AO VIVO — QUARTA-FEIRA 05/08/2026 (11:38 BRT) ===")

target_dir = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\analises_e_automacoes_ia\Consultas_e_Logs_Automacoes"
os.makedirs(target_dir, exist_ok=True)

lines_out = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()

    # ---- 1ª Instância: Ação Penal Búzios ----
    try:
        print("Consultando TJRJ 1ª Instância (Búzios)...")
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

        frame = page.frame_locator("iframe#mainframe")
        frame.locator("input[name='numeroProcesso']").fill("0023013-51.2021.8.19.0078")
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
        lines_out.append("=== ACAO PENAL BUZIOS (0023013-51.2021.8.19.0078) — 05/08/2026 11:38 ===")
        lines_out.append(txt)
    except Exception as e:
        lines_out.append(f"Erro Playwright 1a instancia: {e}")

    # ---- 2ª Instância: Habeas Corpus TJRJ ----
    try:
        print("Consultando TJRJ 2ª Instância (HC)...")
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

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
            time.sleep(3)
        except Exception:
            pass

        real_frame = page.query_selector("iframe#mainframe").content_frame()
        txt2 = real_frame.inner_text("body")
        lines_out.append("\n\n=== HABEAS CORPUS TJRJ (0029845-67.2026.8.19.0000) — 05/08/2026 11:38 ===")
        lines_out.append(txt2)
    except Exception as e:
        lines_out.append(f"\nErro Playwright 2a instancia: {e}")

    browser.close()

res_txt = "\n".join(lines_out)
target_file = os.path.join(target_dir, "tjrj_live_august5_noon.txt")
with open(target_file, "w", encoding="utf-8") as f:
    f.write(res_txt)

print("SUCESSO: Captura salva em " + target_file)
