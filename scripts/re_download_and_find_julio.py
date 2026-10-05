# -*- coding: utf-8 -*-
import time
import os
import sys
import urllib.request
import ssl
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== RE-DOWNLOAD E BUSCA DE PÁGINA EXATA — 05/08/2026 ===")

output_dir = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\Diarios_Oficiais\Novos_Downloads_Teste"
os.makedirs(output_dir, exist_ok=True)

# 1. Baixar novamente o PDF oficial do DJERJ de 29/07/2026 (ou 04/08/05/08 se disponível)
headers = {'User-Agent': 'Mozilla/5.0'}
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Vamos usar Playwright para realizar a busca direta no Portal do DJERJ e extrair o PDF/Extrato de publicação novo
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx_browser = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx_browser.new_page()

    # ---- Teste no Portal do TJRJ Segunda Instância (HC 0029845-67.2026.8.19.0000) ----
    print("\n1. Baixando extrato completo de publicações do HC no TJRJ...")
    try:
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
        txt = real_frame.inner_text("body")

        novo_arquivo_hc = os.path.join(output_dir, "NOVO_EXTRATO_PUBLICACES_HC_0029845-67.2026.txt")
        with open(novo_arquivo_hc, "w", encoding="utf-8") as f:
            f.write(txt)

        print(f"✅ Novo arquivo salvo: {novo_arquivo_hc}")

        # Localizar trechos de publicações no novo arquivo
        lines = txt.split('\n')
        print("\n--- LOCALIZADOR DE PÁGINAS / MOVIMENTOS DE PUBLICAÇÃO NO NOVO ARQUIVO ---")
        page_counter = 1
        for i, l in enumerate(lines):
            if "PAGINA" in l.upper() or "PÁGINA" in l.upper():
                page_counter += 1
            if "PUBLICAÇÃO" in l.upper() or "PUBLICACAO" in l.upper() or "DJEN" in l.upper() or "DJERJ" in l.upper():
                print(f"📍 [Encontrado na linha {i+1}]: {l.strip()}")
                # Print context
                for ctx_line in lines[max(0, i-1):min(len(lines), i+4)]:
                    print(f"      {ctx_line.strip()}")
                print("-" * 50)

    except Exception as e:
        print(f"Erro ao re-baixar HC: {e}")

    # ---- Teste na 1ª Instância (Ação Penal 0023013-51.2021.8.19.0078) ----
    print("\n2. Baixando extrato completo da 1ª Instância (Búzios)...")
    try:
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
        txt_ap = real_frame.inner_text("body")

        novo_arquivo_ap = os.path.join(output_dir, "NOVO_EXTRATO_PUBLICACES_AP_0023013-51.2021.txt")
        with open(novo_arquivo_ap, "w", encoding="utf-8") as f:
            f.write(txt_ap)

        print(f"✅ Novo arquivo salvo: {novo_arquivo_ap}")

        lines_ap = txt_ap.split('\n')
        print("\n--- LOCALIZADOR DE PUBLICAÇÃO NO NOVO ARQUIVO DA AÇÃO PENAL ---")
        for i, l in enumerate(lines_ap):
            if "PUBLICAÇÃO" in l.upper() or "PUBLICACAO" in l.upper() or "04/08/2026" in l or "29/07/2026" in l:
                print(f"📍 [Encontrado na linha {i+1}]: {l.strip()}")
                for ctx_line in lines_ap[max(0, i-1):min(len(lines_ap), i+4)]:
                    print(f"      {ctx_line.strip()}")
                print("-" * 50)

    except Exception as e:
        print(f"Erro ao re-baixar Ação Penal: {e}")

    browser.close()

print("\n=== RE-DOWNLOAD E LOCALIZAÇÃO CONCLUÍDOS ===")
