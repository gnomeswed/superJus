# -*- coding: utf-8 -*-
"""Clicar em Acessar PJe e capturar nova URL/aba."""
import sys, time, json
from pathlib import Path
from playwright.sync_api import sync_playwright


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    PROC = "0821248-17.2025.8.19.0031"
    RAW_DIR = Path(r"C:\Projetos\superJus\Clientes\Renan\03_Documentos_do_Processo\_raspagem_10_08_2026")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=60000)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        time.sleep(2)
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
        time.sleep(10)
        # Clicar no DIV "Acessar PJe"
        clicked = fr.evaluate("""() => {
            const alvo = Array.from(document.querySelectorAll('div, button, a'))
              .find(el => el.offsetWidth > 0 && (el.textContent || '').trim() === 'Acessar PJe');
            if (alvo) { alvo.click(); return true; }
            return false;
        }""")
        print(f"Clicou: {clicked}")
        time.sleep(15)

        # Listar todas as abas abertas
        print(f"\nTotal de abas: {len(ctx.pages)}")
        for i, pg in enumerate(ctx.pages):
            print(f"  Aba {i}: {pg.url}")
            if "pje" in pg.url.lower() or pg != page:
                print(f"     >>> Esta é a nova aba")
                time.sleep(5)
                try:
                    body = pg.inner_text("body")
                    print(f"     Body (1500 chars): {body[:1500]}")
                    pg.screenshot(path=str(RAW_DIR / "pje_nova_aba.png"), full_page=True)
                except Exception as e:
                    print(f"     err: {e}")
        browser.close()


if __name__ == "__main__":
    main()
