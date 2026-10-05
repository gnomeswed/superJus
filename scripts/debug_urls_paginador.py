# -*- coding: utf-8 -*-
"""Tentar várias URLs e procurar paginador 500."""
import sys, time
from playwright.sync_api import sync_playwright


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    PROC = "0011857-95.2024.8.19.0002"

    urls_to_try = [
        "https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica",
        "https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica/porNumero",
        "https://www3.tjrj.jus.br/consultaprocessual/#/consultapublicap",
        "https://www3.tjrj.jus.br/consultaprocessual/",
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_context(viewport={"width": 1366, "height": 900}).new_page()

        for url in urls_to_try:
            try:
                page.goto(url, timeout=30000, wait_until="domcontentloaded")
                time.sleep(3)
                print(f"\n>>> URL: {url}")
                print(f"   Page URL final: {page.url}")
                try:
                    page.wait_for_selector("iframe#mainframe", timeout=10000)
                    fr = page.query_selector("iframe#mainframe").content_frame()
                    paginador = fr.evaluate("""() => {
                        const all = Array.from(document.querySelectorAll('select, span, div, button'))
                          .filter(el => el.offsetWidth > 0);
                        return all
                          .map(el => ({tag: el.tagName, text: (el.textContent||'').trim().slice(0,30), classes: el.className.slice(0,40)}))
                          .filter(x => /^500|\\b500\\b/.test(x.text));
                    }""")
                    if paginador:
                        print(f"   ✓ Paginador 500 encontrado: {paginador[:3]}")
                    else:
                        print(f"   Sem paginador 500 visível")
                except Exception as e:
                    print(f"   err: {e}")
            except Exception as e:
                print(f">>> URL: {url} - ERRO: {e}")
        browser.close()


if __name__ == "__main__":
    main()
