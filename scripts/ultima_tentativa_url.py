# -*- coding: utf-8 -*-
"""Última tentativa: Portal de Busca do TJRJ (lista de processos do dia)."""
import sys, time, re
from pathlib import Path
from playwright.sync_api import sync_playwright


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    PROC = "0821248-17.2025.8.19.0031"

    # Lista de URLs do diário / busca alternativa
    urls = [
        "https://dje-consulta.tjrj.jus.br/consultaDiario",
        "https://www3.tjrj.jus.br/dje/",
        "https://www.tjrj.jus.br/dje",
        "https://www3.tjrj.jus.br/sisdiweb/",
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        for url in urls:
            page = browser.new_context(viewport={"width": 1366, "height": 900}).new_page()
            try:
                page.goto(url, timeout=30000, wait_until="domcontentloaded")
                time.sleep(5)
                print(f"\n>>> {url}")
                print(f"   Status/Title: {page.title()[:80]}")
                print(f"   URL final: {page.url}")
            except Exception as e:
                print(f"\n>>> {url}")
                print(f"   ERR: {str(e)[:80]}")
            page.close()
        browser.close()


if __name__ == "__main__":
    main()
