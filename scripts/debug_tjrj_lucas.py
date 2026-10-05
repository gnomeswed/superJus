# -*- coding: utf-8 -*-
"""Debug: ver o que acontece após clicar 'Todos Os Movimentos' no TJRJ."""
import sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

PROC = "0011857-95.2024.8.19.0002"


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()

        navs = []
        page.on("framenavigated", lambda fr: navs.append((fr.url, time.time())))

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
        time.sleep(8)

        info_antes = fr.evaluate("""() => {
            const candidates = Array.from(document.querySelectorAll('a, button, span, div'))
              .filter(b => (b.textContent || '').toLowerCase().includes('todos os movimentos'));
            return candidates.map(c => ({
                tag: c.tagName,
                text: (c.textContent || '').trim().slice(0, 80),
                href: c.getAttribute('href'),
                onclick: c.getAttribute('onclick') ? 'YES' : 'NO',
                visible: c.offsetWidth > 0 && c.offsetHeight > 0,
                classes: c.className
            }));
        }""")
        print("Candidatos 'Todos Os Movimentos' ANTES do clique:")
        for c in info_antes:
            print(" ", c)

        print(f"\nURL antes do clique: {page.url}")
        print(f"Frame URL antes:     {fr.url}")

        try:
            fr.evaluate("""() => {
                const candidates = Array.from(document.querySelectorAll('a, button, span, div'))
                  .filter(b => (b.textContent || '').toLowerCase().includes('todos os movimentos'));
                if (candidates.length) candidates[0].click();
            }""")
        except Exception as e:
            print("clique err:", e)

        time.sleep(10)
        print(f"\nURL depois do clique: {page.url}")
        print(f"Frame URL depois:     {fr.url}")

        body = fr.inner_text("body")
        print(f"\nTamanho do body depois: {len(body)} chars")
        print("Últimas 300 chars:")
        print(body[-300:])

        integra = fr.evaluate("""() => {
            return Array.from(document.querySelectorAll('a, button, span, div'))
              .filter(b => {
                const t = (b.textContent || '').toLowerCase().trim();
                return t.includes('ver íntegra') || t.includes('ver integra') ||
                       t.includes('visualizar ato') || t.includes('íntegra');
              })
              .map(b => ({tag: b.tagName, text: (b.textContent||'').trim().slice(0,40)}));
        }""")
        print(f"\nLinks 'Ver Íntegra' / 'Visualizar Ato' após clique: {len(integra)}")
        for c in integra[:10]:
            print(" ", c)

        print(f"\nNavegação events: {len(navs)}")
        for n in navs[-5:]:
            print(" ", n)

        browser.close()


if __name__ == "__main__":
    main()
