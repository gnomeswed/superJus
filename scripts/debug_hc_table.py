# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== EXPLORAR TABELA RESULTADO HC TJRJ — 03/08/2026 ===")

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
    frame.locator("input[name='numeroProcesso']").fill("0029845-67.2026.8.19.0000")
    time.sleep(1)
    frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
    time.sleep(8)

    real_frame = page.query_selector("iframe#mainframe").content_frame()

    # Descobrir elementos clicáveis na tabela
    try:
        links = real_frame.locator("table a")
        n = links.count()
        lines_out.append(f"[DEBUG] Links na tabela: {n}")
        for i in range(min(n, 10)):
            txt = links.nth(i).inner_text(timeout=3000)
            href = links.nth(i).get_attribute("href")
            lines_out.append(f"  - Link {i}: '{txt}' href={href}")
    except Exception as e:
        lines_out.append(f"Sem links na tabela: {e}")

    # Ver HTML da tabela
    try:
        html = real_frame.locator("table").first.inner_html()
        lines_out.append("\n[DEBUG] HTML tabela:\n" + html[:4000])
    except Exception as e:
        lines_out.append(f"HTML tabela erro: {e}")

    browser.close()

res_txt = "\n".join(lines_out)
target_file = os.path.join(target_dir, "tjrj_hc_table_debug.txt")
with open(target_file, "w", encoding="utf-8") as f:
    f.write(res_txt)

print("SUCESSO: Debug salvo em " + target_file)
