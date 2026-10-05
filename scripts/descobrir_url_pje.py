# -*- coding: utf-8 -*-
"""Procurar URL atual do PJe TJRJ + tentar DataJud API."""
import sys, time, json
from pathlib import Path
from playwright.sync_api import sync_playwright


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    PROC = "0821248-17.2025.8.19.0031"

    # Tentar descobrir via Google
    searches = [
        "pje.tjrj.jus.br",
        "pje tj rj consulta publica",
        "tjrj pje consulta publica",
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        # Buscar no Google
        page = browser.new_context(viewport={"width": 1366, "height": 900}).new_page()
        for q in searches[:1]:
            try:
                page.goto(f"https://www.google.com/search?q={q.replace(' ', '+')}", timeout=30000)
                time.sleep(3)
                results = page.evaluate("""() => {
                    return Array.from(document.querySelectorAll('a'))
                      .filter(a => a.href && /pje|consulta|processo/i.test(a.href))
                      .slice(0, 10)
                      .map(a => ({text: a.innerText.slice(0, 80), href: a.href}));
                }""")
                print(f"\nResultados para '{q}':")
                for r in results:
                    print(f"  {r['text'][:60]:60} | {r['href'][:80]}")
            except Exception as e:
                print(f"  err: {e}")

        # Tentar URL conhecida do PJe 2.x do TJRJ
        pje_urls = [
            "https://pje-consulta.tjrj.jus.br/",
            "https://consulta.tjrj.jus.br/",
            "https://pje.tjrj.jus.br/consulta/",
            "https://www.tjrj.jus.br/pje",
            "https://portal.tjrj.jus.br/",
            "https://esaj.tjrj.jus.br/",
        ]
        for url in pje_urls:
            try:
                r = page.goto(url, timeout=20000, wait_until="domcontentloaded")
                print(f"\n{url} -> status {r.status if r else '?'}")
            except Exception as e:
                print(f"\n{url} -> ERR: {str(e)[:80]}")

        browser.close()


if __name__ == "__main__":
    main()
