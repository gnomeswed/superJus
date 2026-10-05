# -*- coding: utf-8 -*-
"""Debug 2: inspecionar botões/links visíveis após carregar o processo no TJRJ."""
import sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

PROC = "0011857-95.2024.8.19.0002"


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        fr = page.query_selector("iframe#mainframe").content_frame()
        time.sleep(2)

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
        print(f"URL após pesquisar: {fr.url}")

        html = fr.evaluate("() => document.documentElement.outerHTML")
        open(r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_raspagem_10_08_2026\frame_full.html", "w", encoding="utf-8").write(html)

        botoes = fr.evaluate("""() => {
            const all = Array.from(document.querySelectorAll('a, button, [role=button], .clickable, span[ng-click], div[ng-click]'));
            return all.filter(el => el.offsetWidth > 0 && el.offsetHeight > 0).map(el => ({
                tag: el.tagName,
                text: (el.textContent || '').trim().slice(0, 60),
                title: el.getAttribute('title'),
                aria: el.getAttribute('aria-label'),
                classes: el.className.slice(0, 80),
            }));
        }""")
        print(f"\n{len(botoes)} elementos clicáveis visíveis:")
        for b in botoes[:40]:
            print(" ", b)
        if len(botoes) > 40:
            print(f"  ... +{len(botoes)-40}")

        movs_text = fr.evaluate("""() => {
            const body = document.body.innerText;
            const matches = body.match(/\\d{2}\\/\\d{2}\\/\\d{4}[^\\n]{0,200}/g) || [];
            return matches.slice(0, 20);
        }""")
        print(f"\nDatas encontradas no body: {len(movs_text)}")
        for m in movs_text[:10]:
            print(" ", m[:120])

        browser.close()


if __name__ == "__main__":
    main()
