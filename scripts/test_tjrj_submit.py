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
    time.sleep(3)

    buttons = page.evaluate('Array.from(document.querySelectorAll("button")).map(b => ({text: b.innerText.trim(), class: b.className, type: b.type}))')
    print('Buttons:', buttons)

    # Let's fill the input
    inp_selector = 'input[placeholder*="número do processo"]'
    page.fill(inp_selector, '0023013-51.2021.8.19.0078')
    time.sleep(1)

    # Click Pesquisar
    page.click('button:has-text("Pesquisar")')
    print('Clicked Pesquisar, waiting 10s...')
    time.sleep(10)

    print('Current URL:', page.url)
    print('Frames now:', len(page.frames))
    for i, f in enumerate(page.frames):
        print(f'Frame {i}: name="{f.name}" url="{f.url}"')

    iframes = page.evaluate('Array.from(document.querySelectorAll("iframe")).map(i => ({id: i.id, name: i.name, src: i.src}))')
    print('iframes now:', iframes)

    print('Body snippet:', page.evaluate('document.body.innerText')[:1000])

    b.close()
