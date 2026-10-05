# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

proc_num = "0023013-51.2021.8.19.0078"
target_file = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\tjrj_live_august1_2026.txt"

print("Acessando TJRJ ao vivo via Playwright (channel=chrome / headless=False)...")

lines_out = []
try:
    with sync_playwright() as p:
        # Launch using standard chromium browser
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-gpu"])
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        page = ctx.new_page()
        
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=60000)
        time.sleep(4)
        
        frame = page.frame_locator("iframe#mainframe")
        frame.locator("input[name='numeroProcesso']").fill(proc_num)
        time.sleep(1)
        frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
        time.sleep(6)
        
        try:
            frame.locator("button:has-text('Todos Os Movimentos')").first.click()
            time.sleep(4)
        except Exception as e:
            print("Aviso no botão todos os movimentos:", e)
        
        real_frame = page.query_selector("iframe#mainframe").content_frame()
        movs_txt = real_frame.inner_text("body")
        
        lines_out.append("=== CAPTURA AO VIVO DO PORTAL TJRJ — PROCESSO 0023013-51.2021.8.19.0078 ===")
        lines_out.append(movs_txt)
        
        browser.close()
except Exception as e:
    lines_out.append(f"Erro Playwright TJRJ: {e}")

res = "\n".join(lines_out)
os.makedirs(os.path.dirname(target_file), exist_ok=True)
with open(target_file, "w", encoding="utf-8") as f:
    f.write(res)

print("SUCESSO: Resultado salvo em " + target_file)
