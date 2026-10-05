# -*- coding: utf-8 -*-
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

from playwright.sync_api import sync_playwright

OUT_DIR = r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_varredura_01_09_2026"
os.makedirs(OUT_DIR, exist_ok=True)

url_direct = "https://www4.tjrj.jus.br/consultaProcessoDCP/ConsultaProcesso.aspx?N=2026.050.14194"

print(f"=== ACESSANDO DIRETAMENTE A 2ª INSTÂNCIA: {url_direct} ===", flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-dev-shm-usage"]
    )
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 900},
        locale="pt-BR"
    )
    page = ctx.new_page()

    page.goto(url_direct, timeout=45000, wait_until="domcontentloaded")
    time.sleep(6)

    # Clicar em listar todos os movimentos se houver
    try:
        page.evaluate("ListarMovimentos();")
        time.sleep(4)
    except Exception as e:
        print(f"Nota ListarMovimentos: {e}")

    txt = page.inner_text("body")
    with open(os.path.join(OUT_DIR, "2A_EXATO_DIRETO_01_09_2026.txt"), "w", encoding="utf-8") as f:
        f.write(txt)

    page.screenshot(path=os.path.join(OUT_DIR, "2A_screenshot_direct.png"), full_page=True)

    print("\n=======================================================")
    print("=== RESULTADO DIRETO 2ª INSTÂNCIA (01/09/2026) ===")
    print("=======================================================")
    for line in [l.strip() for l in txt.split('\n') if l.strip()]:
        print(f"  {line}")

    browser.close()

print("\n=== CONCLUÍDO COM SUCESSO ===", flush=True)
