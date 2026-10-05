# -*- coding: utf-8 -*-
"""Tentar URL direta do PJe para consulta pública."""
import sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    PROC = "0821248-17.2025.8.19.0031"
    RAW_DIR = Path(r"C:\Projetos\superJus\Clientes\Renan\03_Documentos_do_Processo\_raspagem_10_08_2026")

    urls = [
        f"https://pje.tjrj.jus.br/pje/ConsultaPublica/ConsultaPublica/detalheProcessoPublico.seam?numeroProcesso={PROC.replace('-','').replace('.','')}",
        f"https://pje.tjrj.jus.br/pje/ConsultaPublica/ConsultaPublica/detalheProcessoPublico.seam?numeroProcesso={PROC}",
        "https://pje.tjrj.jus.br/pje/login.seam",
        "https://pje.tjrj.jus.br/pje/",
        "https://www.tjrj.jus.br/web/processo/pesquisa",
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        for url in urls:
            page = browser.new_context(viewport={"width": 1366, "height": 900}).new_page()
            try:
                page.goto(url, timeout=30000, wait_until="domcontentloaded")
                time.sleep(5)
                print(f"\n>>> {url}")
                print(f"   Final URL: {page.url}")
                print(f"   Title: {page.title()[:80]}")
                body = page.inner_text("body")[:500]
                print(f"   Body: {body}")
                screenshot_name = f"pje_test_{abs(hash(url)) % 1000}.png"
                page.screenshot(path=str(RAW_DIR / screenshot_name), full_page=True)
            except Exception as e:
                print(f"\n>>> {url}")
                print(f"   ERR: {e}")
            page.close()
        browser.close()


if __name__ == "__main__":
    main()
