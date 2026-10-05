# -*- coding: utf-8 -*-
import time, os, sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

nome = "RENAN RODRIGUES DE SOUZA"
print(f"=== BUSCA NO PORTAL TJRJ POR NOME VIA IFRAME: {nome} ===")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
    ctx = browser.new_context(
        viewport={"width": 1366, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()

    try:
        print("1. Navegando para o TJRJ consulta pública...")
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=40000, wait_until="domcontentloaded")
        time.sleep(5)

        # Esperar iframe#mainframe
        page.wait_for_selector("iframe#mainframe", timeout=25000)
        frame = page.frame_locator("iframe#mainframe")

        print("2. Clicando em #nav-porNome...")
        frame.locator("#nav-porNome").click()
        time.sleep(2)

        print("3. Preenchendo nome da parte...")
        frame.locator("input[name='nomeParte']").fill(nome)
        time.sleep(1)

        # Desmarcar somente em andamento se existir
        try:
            chk = frame.locator("input[name='procEmAndamento']")
            if chk.is_checked():
                chk.uncheck()
        except Exception:
            pass

        print("4. Clicando em pesquisar...")
        btn = frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first
        btn.click()

        print("5. Aguardando resultados (12s)...")
        time.sleep(12)

        real_frame = page.query_selector("iframe#mainframe").content_frame()
        body_text = real_frame.inner_text("body")
        print(f"6. Resposta obtida ({len(body_text)} chars):")

        out_txt = r"c:\Projetos\superJus\Clientes\Renan\03_Documentos_do_Processo\tjrj_portal_busca_nome.txt"
        with open(out_txt, "w", encoding="utf-8") as f:
            f.write(body_text)
        print("Salvo em:", out_txt)

        lines = [l.strip() for l in body_text.splitlines() if l.strip()]
        for l in lines[:50]:
            print(f"  [TJRJ] {l}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        browser.close()
