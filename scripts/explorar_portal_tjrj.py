# -*- coding: utf-8 -*-
"""Tentar achar página de consulta de processos no portal TJRJ."""
import sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    PROC = "0821248-17.2025.8.19.0031"
    RAW_DIR = Path(r"C:\Projetos\superJus\Clientes\Renan\03_Documentos_do_Processo\_raspagem_10_08_2026")

    # Aceitar cookies primeiro
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_context(viewport={"width": 1366, "height": 900}).new_page()

        page.goto("https://www.tjrj.jus.br/web/processo/pesquisa", timeout=60000)
        time.sleep(5)
        # Aceitar cookies
        try:
            page.evaluate("""() => {
                const btn = Array.from(document.querySelectorAll('button, a'))
                  .find(b => b.offsetWidth > 0 && (b.textContent || '').trim() === 'Aceitar');
                if (btn) btn.click();
            }""")
            time.sleep(3)
        except Exception:
            pass
        page.screenshot(path=str(RAW_DIR / "portal_tjrj.png"), full_page=True)

        # Listar todos os links visíveis
        links = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('a'))
              .filter(a => a.offsetWidth > 0 && a.href && /processo|consulta|pje/i.test(a.href))
              .slice(0, 30)
              .map(a => ({text: (a.innerText || '').trim().slice(0, 60), href: a.href}));
        }""")
        print("Links relevantes:")
        for l in links:
            print(f"  {l['text'][:60]:60} | {l['href'][:80]}")

        browser.close()


if __name__ == "__main__":
    main()
