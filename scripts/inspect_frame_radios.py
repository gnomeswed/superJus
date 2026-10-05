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
    page.goto('https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica', wait_until='commit', timeout=30000)
    frame_el = page.wait_for_selector("iframe#mainframe", timeout=30000)
    frame = frame_el.content_frame()
    time.sleep(3)

    radios = frame.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('input[type="radio"], input[type="checkbox"], label'));
        return els.map(el => ({
            tag: el.tagName,
            type: el.type,
            name: el.name,
            id: el.id,
            for: el.getAttribute('for'),
            text: el.innerText || el.textContent
        }));
    }""")
    print("Radios and labels inside frame:")
    for r in radios:
        if any(w in str(r).lower() for w in ['origem', 'instancia', 'instância', 'segunda', 'primeira', 'radio']):
            print(r)

    b.close()
