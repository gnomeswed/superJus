# -*- coding: utf-8 -*-
"""Procurar endpoint para baixar atos assinados digitalmente."""
import sys, time, json
from playwright.sync_api import sync_playwright


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()

        api_calls = []
        def on_req(req):
            api_calls.append((req.method, req.url, req.post_data or ""))
        page.on("request", on_req)

        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=60000)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        time.sleep(3)
        fr = page.query_selector("iframe#mainframe").content_frame()
        fr.evaluate("""() => {
            const inp = Array.from(document.querySelectorAll('input'))
              .find(i => i.name === 'numeroProcesso' || i.id === 'numeroProcesso');
            if (inp) {
              inp.value = '0011857-95.2024.8.19.0002';
              inp.dispatchEvent(new Event('input', { bubbles: true }));
              inp.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }""")
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
              .find(b => b.offsetWidth > 0 && b.textContent.toLowerCase().includes('pesquisar'));
            if (btn) btn.click();
        }""")
        time.sleep(10)
        # Expandir
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
              .find(b => (b.textContent || '').toLowerCase().includes('todos os movimentos'));
            if (btn) btn.click();
        }""")
        time.sleep(15)

        # Clicar "Visualizar Ato Assinado Digitalmente"
        clicked = fr.evaluate("""() => {
            const alvo = Array.from(document.querySelectorAll('a, button'))
              .find(el => el.offsetWidth > 0 && (el.textContent || '').trim() === 'Visualizar Ato Assinado Digitalmente');
            if (alvo) { alvo.click(); return true; }
            return false;
        }""")
        print(f"Clicou: {clicked}")
        time.sleep(10)

        # Listar todas requests feitas durante a ação
        print(f"\n{len(api_calls)} requests capturadas:")
        for m, u, b in api_calls[-15:]:
            print(f"  {m} {u[:120]}")
            if b and len(b) < 200:
                print(f"    body: {b}")

        browser.close()


if __name__ == "__main__":
    main()
