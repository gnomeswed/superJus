import time
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

print("Iniciando Playwright com timeout estendido de 90 segundos...")
t0 = time.time()
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
    )
    ctx = browser.new_context(
        viewport={"width": 1366, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()
    try:
        print("Tentando carregar https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica...")
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="load", timeout=90000)
        print(f"Sucesso ao carregar TJRJ em {time.time() - t0:.2f}s!")
        print("Título:", page.title())
        page.wait_for_selector('input[placeholder*="número do processo"]', timeout=20000)
        print("Input localizado!")
    except Exception as e:
        print(f"Erro após {time.time() - t0:.2f}s: {e}")
    browser.close()
