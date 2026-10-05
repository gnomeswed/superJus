# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== DETALHE HC / ROC TJRJ — 03/08/2026 ===")

target_dir = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(target_dir, exist_ok=True)

lines_out = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1280, "height": 900})
    page = ctx.new_page()

    def busca_e_abre(rotulo):
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=60000)
        time.sleep(4)
        frame = page.frame_locator("iframe#mainframe")
        frame.locator("input[name='numeroProcesso']").fill("0029845-67.2026.8.19.0000")
        time.sleep(1)
        frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
        time.sleep(8)
        real_frame = page.query_selector("iframe#mainframe").content_frame()

        links = real_frame.locator("table a")
        n = links.count()
        target = None
        for i in range(n):
            t = links.nth(i).inner_text(timeout=3000)
            if rotulo in t:
                target = i
                break
        if target is None:
            return f"[{rotulo}] link não encontrado"
        with page.expect_popup(timeout=15000) as popup_info:
            links.nth(target).click()
        popup = popup_info.value
        popup.wait_for_load_state("domcontentloaded")
        time.sleep(6)
        try:
            popup.locator("button:has-text('Todos Os Movimentos')").first.click(timeout=8000)
            time.sleep(4)
        except Exception:
            pass
        txt = popup.inner_text("body")
        return txt

    try:
        lines_out.append("=== HC TJRJ (0029845-67.2026.8.19.0000) (2026.059.10770) — DETALHE 03/08/2026 ===")
        lines_out.append(busca_e_abre("2026.059.10770"))
    except Exception as e:
        lines_out.append(f"Erro HC: {e}")

    try:
        lines_out.append("\n\n=== ROC TJRJ (0029845-67.2026.8.19.0000) (2026.141.00580) — DETALHE 03/08/2026 ===")
        lines_out.append(busca_e_abre("2026.141.00580"))
    except Exception as e:
        lines_out.append(f"\nErro ROC: {e}")

    browser.close()

res_txt = "\n".join(lines_out)
target_file = os.path.join(target_dir, "tjrj_hc_roc_august3_detail.txt")
with open(target_file, "w", encoding="utf-8") as f:
    f.write(res_txt)

print("SUCESSO: Salvo em " + target_file)
