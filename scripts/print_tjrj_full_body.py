import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=60000)
    time.sleep(8)
    print("Full body text:\n")
    print(page.inner_text("body"))
    browser.close()
