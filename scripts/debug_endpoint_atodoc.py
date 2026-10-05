# -*- coding: utf-8 -*-
"""Tentar baixar ato assinado via codDocAtoAssinadoDig."""
import sys, time, json
from playwright.sync_api import sync_playwright


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    CODDOC = "00040DF0471596FA840B9A2859155C450A0DC51A61584251"  # Decisão 17/06/2026

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()

        api_calls = []
        def on_req(req):
            api_calls.append((req.method, req.url))
        page.on("request", on_req)

        # Tentar várias URLs comuns
        urls_to_try = [
            f"https://www3.tjrj.jus.br/consultaprocessual/api/atos/{CODDOC}",
            f"https://www3.tjrj.jus.br/consultaprocessual/api/atos/baixar/{CODDOC}",
            f"https://www3.tjrj.jus.br/consultaprocessual/api/documentos/{CODDOC}",
            f"https://www3.tjrj.jus.br/consultaprocessual/api/documento/download/{CODDOC}",
            f"https://www3.tjrj.jus.br/consultaprocessual/api/atos-assinados/{CODDOC}/pdf",
            f"https://www3.tjrj.jus.br/consultaprocessual/api/atos-assinados/{CODDOC}",
        ]

        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=60000)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        time.sleep(3)

        for url in urls_to_try:
            try:
                result = page.evaluate(f"""async (url) => {{
                    const r = await fetch(url, {{credentials: 'include'}});
                    return {{
                        status: r.status,
                        content_type: r.headers.get('content-type'),
                        body_sample: (await r.text()).slice(0, 300),
                    }};
                }}""", url)
                print(f"  {result['status']}  {url[:80]}")
                if result['status'] != 404:
                    print(f"     CT: {result['content_type']}")
                    print(f"     Body: {result['body_sample'][:200]!r}")
            except Exception as e:
                print(f"  ERR {url[:60]}: {e}")

        browser.close()


if __name__ == "__main__":
    main()
