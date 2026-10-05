# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== CHECAGEM AO VIVO DE FINAL DE EXPEDIENTE — SEGUNDA-FEIRA (03/08/2026 - 17:13h) ===")

target_file = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\tjrj_live_august3_evening.txt"

lines_out = []
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        page = ctx.new_page()
        
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
        
        lines_out.append("=== AÇÃO PENAL BÚZIOS (0023013-51.2021.8.19.0078) — FIM DE EXPEDIENTE 03/08/2026 ===")
        lines_out.append(txt)
        
        browser.close()
except Exception as e:
    lines_out.append(f"Erro Playwright TJRJ: {e}")

res_txt = "\n".join(lines_out)
os.makedirs(os.path.dirname(target_file), exist_ok=True)
with open(target_file, "w", encoding="utf-8") as f:
    f.write(res_txt)

print("SUCESSO: Captura salva em " + target_file)
