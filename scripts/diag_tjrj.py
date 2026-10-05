import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = b.new_context(
        viewport={"width": 1366, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        locale="pt-BR"
    )
    page = ctx.new_page()
    page.goto('https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica', wait_until='networkidle', timeout=40000)
    time.sleep(3)
    page.screenshot(path="c:/Projetos/superJus/tjrj_portal_snap.png")
    print("Page title:", page.title())
    print("Page URL:", page.url)
    print("Frames count:", len(page.frames))
    for i, f in enumerate(page.frames):
        print(f"Frame {i}: name='{f.name}' url='{f.url}'")
    
    # Check elements in page
    inputs = page.query_selector_all('input')
    print("Page inputs count:", len(inputs))
    for inp in inputs:
        print("  input:", inp.get_attribute("name"), inp.get_attribute("id"), inp.get_attribute("placeholder"))

    # If iframe exists
    if len(page.frames) > 1:
        f = page.frames[1]
        f_inputs = f.query_selector_all('input')
        print("Frame 1 inputs count:", len(f_inputs))
        for inp in f_inputs:
            print("  frame input:", inp.get_attribute("name"), inp.get_attribute("id"), inp.get_attribute("placeholder"))

    b.close()
