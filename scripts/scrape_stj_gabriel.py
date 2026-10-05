# -*- coding: utf-8 -*-
import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        locale="pt-BR"
    )
    page = ctx.new_page()

    # 1. Busca por OAB no STJ
    url_oab = "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaOab&termo=RJ203902"
    print(f"Navegando para busca por OAB RJ203902 no STJ...")
    try:
        page.goto(url_oab, timeout=30000, wait_until="domcontentloaded")
        time.sleep(5)
        txt = page.inner_text("body")
        print(f"Resposta OAB RJ203902 ({len(txt)} chars):")
        for line in txt.splitlines()[:25]:
            if line.strip():
                print("  •", line.strip())
    except Exception as e:
        print("Erro OAB:", e)

    # 2. Busca por Nome no STJ
    url_nome = "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNomeParteAdvogado&termo=GABRIEL+ALVES+GUIMARAES"
    print(f"\nNavegando para busca por Nome no STJ...")
    try:
        page.goto(url_nome, timeout=30000, wait_until="domcontentloaded")
        time.sleep(5)
        txt_nome = page.inner_text("body")
        print(f"Resposta Nome GABRIEL ALVES GUIMARAES ({len(txt_nome)} chars):")
        for line in txt_nome.splitlines()[:25]:
            if line.strip():
                print("  •", line.strip())
    except Exception as e:
        print("Erro Nome:", e)

    browser.close()
