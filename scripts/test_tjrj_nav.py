import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
    )
    ctx = b.new_context(
        viewport={"width": 1366, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        locale="pt-BR"
    )
    page = ctx.new_page()
    page.goto('https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica', wait_until='networkidle', timeout=30000)
    time.sleep(5)
    print('Frames count:', len(page.frames))
    for i, f in enumerate(page.frames):
        print(f'Frame {i}: name="{f.name}" url="{f.url}"')
    iframes = page.evaluate('Array.from(document.querySelectorAll("iframe")).map(i => ({id: i.id, name: i.name, src: i.src}))')
    print('iframes in DOM:', iframes)
    inputs = page.evaluate('Array.from(document.querySelectorAll("input")).map(i => ({id: i.id, name: i.name, placeholder: i.placeholder}))')
    print('inputs in DOM:', inputs)
    b.close()
