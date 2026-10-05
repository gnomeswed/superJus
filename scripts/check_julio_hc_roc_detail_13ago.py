# -*- coding: utf-8 -*-
"""Detalhe HC / ROC TJRJ 2ª instância — verificação ao vivo 13/08/2026
Fase atual do RHC pode revelar se voltou do STJ ou aguarda julgamento."""
import time, os, sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')

print("=== DETALHE HC / ROC TJRJ (iframe) — 13/08/2026 ===")
target_dir = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(target_dir, exist_ok=True)
lines_out = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1366, "height": 900},
                              user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

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

        links.nth(target).click()
        time.sleep(8)
        real_frame = page.query_selector("iframe#mainframe").content_frame()
        try:
            real_frame.locator("button:has-text('Todos Os Movimentos')").first.click(timeout=8000)
            time.sleep(5)
        except Exception:
            pass
        return real_frame.inner_text("body")

    try:
        lines_out.append("=== HC TJRJ (0029845-67.2026.8.19.0000) (2026.059.10770) — DETALHE 13/08/2026 ===")
        lines_out.append(busca_e_abre("2026.059.10770"))
    except Exception as e:
        lines_out.append(f"Erro HC: {e}")

    try:
        lines_out.append("\n\n=== ROC TJRJ (0029845-67.2026.8.19.0000) (2026.141.00580) — DETALHE 13/08/2026 ===")
        lines_out.append(busca_e_abre("2026.141.00580"))
    except Exception as e:
        lines_out.append(f"\nErro ROC: {e}")

    browser.close()

res_txt = "\n".join(lines_out)
target_file = os.path.join(target_dir, "tjrj_hc_roc_august13_detail.txt")
with open(target_file, "w", encoding="utf-8") as f:
    f.write(res_txt)
print("SUCESSO: Salvo em " + target_file)
