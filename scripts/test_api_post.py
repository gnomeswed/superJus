# -*- coding: utf-8 -*-
"""POST na API de movimentos do TJRJ."""
import sys, time, json, urllib.request, urllib.error
from playwright.sync_api import sync_playwright


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    PROC = "0011857-95.2024.8.19.0002"

    cookies = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        time.sleep(3)
        cookies_list = ctx.cookies()
        cookies = {c["name"]: c["value"] for c in cookies_list}
        # Capturar a request POST original que o Angular faz
        captured = {}
        def on_request(req):
            if "/api/processos/por-numero/movimentos" in req.url:
                captured["url"] = req.url
                captured["method"] = req.method
                captured["headers"] = dict(req.headers)
                captured["post_data"] = req.post_data
        page.on("request", on_request)

        # Trigger a request carregando processo
        fr = page.query_selector("iframe#mainframe").content_frame()
        fr.evaluate(f"""() => {{
            const inp = Array.from(document.querySelectorAll('input'))
              .find(i => i.name === 'numeroProcesso' || i.id === 'numeroProcesso');
            if (inp) {{
              inp.value = '{PROC}';
              inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
              inp.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        }}""")
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
              .find(b => b.offsetWidth > 0 && b.textContent.toLowerCase().includes('pesquisar'));
            if (btn) btn.click();
        }""")
        time.sleep(8)
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
              .find(b => (b.textContent || '').toLowerCase().includes('todos os movimentos'));
            if (btn) btn.click();
        }""")
        time.sleep(15)
        browser.close()

    print(f"Captured request:")
    print(f"  url: {captured.get('url')}")
    print(f"  method: {captured.get('method')}")
    print(f"  post_data: {captured.get('post_data', 'NONE')!r}")
    print(f"  headers:")
    for k, v in (captured.get('headers') or {}).items():
        print(f"    {k}: {v[:120]}")


if __name__ == "__main__":
    main()
