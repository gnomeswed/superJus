import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page()
    t0 = time.time()
    print("Navigating with wait_until='commit'...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="commit", timeout=15000)
    print(f"Commit reached in {time.time() - t0:.2f}s!")
    time.sleep(3)
    print("Page title:", page.title())
    print("Looking for input...")
    inp = page.wait_for_selector('input[placeholder*="número do processo"]', timeout=15000)
    print("Input found:", inp)
    b.close()
