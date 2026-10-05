import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    print("Acessando...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=60000)
    time.sleep(5)
    print("URL atual:", page.url)
    print("Título:", page.title())
    print("Texto do body:\n", page.inner_text("body")[:500])
    browser.close()
