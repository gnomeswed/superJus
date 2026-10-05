# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== DETALHE HC TJRJ 2a INSTANCIA — 03/08/2026 22:30 ===")

target_dir = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(target_dir, exist_ok=True)

lines_out = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1280, "height": 900})
    page = ctx.new_page()

    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=60000)
    time.sleep(4)

    frame = page.frame_locator("iframe#mainframe")
    try:
        inp_origem = frame.locator("#filtroOrigem1")
        inp_origem.fill("Tribunal de Justiça")
        time.sleep(1)
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
    except Exception as e:
        print("Aviso origem:", e)
    time.sleep(1)

    frame.locator("input[name='numeroProcesso']").fill("0029845-67.2026.8.19.0000")
    time.sleep(1)
    frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
    time.sleep(8)

    real_frame = page.query_selector("iframe#mainframe").content_frame()

    # Clicar no primeiro resultado (linha da tabela)
    try:
        row = real_frame.locator("table tr:has-text('0029845-67.2026.8.19.0000')").first
        row.click()
        time.sleep(5)
    except Exception as e:
        print("Aviso clique linha:", e)

    try:
        frame.locator("button:has-text('Todos Os Movimentos')").first.click()
        time.sleep(5)
    except Exception:
        pass

    real_frame = page.query_selector("iframe#mainframe").content_frame()
    txt = real_frame.inner_text("body")
    lines_out.append("=== HC TJRJ (0029845-67.2026.8.19.0000) — DETALHE 03/08/2026 ===")
    lines_out.append(txt)

    # Segunda linha (ROC) se existir
    try:
        rows = real_frame.locator("table tr:has-text('0029845-67.2026.8.19.0000')")
        cnt = rows.count()
        lines_out.append(f"\n\n[DEBUG] Linhas encontradas com o processo: {cnt}")
        if cnt > 1:
            rows.nth(1).click()
            time.sleep(5)
            try:
                frame.locator("button:has-text('Todos Os Movimentos')").first.click()
                time.sleep(5)
            except Exception:
                pass
            real_frame = page.query_selector("iframe#mainframe").content_frame()
            txt2 = real_frame.inner_text("body")
            lines_out.append("\n\n=== ROC TJRJ (0029845-67.2026.8.19.0000 / 2026.141.00580) — DETALHE 03/08/2026 ===")
            lines_out.append(txt2)
    except Exception as e:
        lines_out.append(f"\nAviso 2a linha: {e}")

    browser.close()

res_txt = "\n".join(lines_out)
target_file = os.path.join(target_dir, "tjrj_hc_august3_night_detail.txt")
with open(target_file, "w", encoding="utf-8") as f:
    f.write(res_txt)

print("SUCESSO: Detalhe salvo em " + target_file)
