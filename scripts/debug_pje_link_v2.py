# -*- coding: utf-8 -*-
"""Investigar HTML do frame TJRJ - onde está o botão Acessar PJe."""
import sys, time
from playwright.sync_api import sync_playwright


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    PROC = "0821248-17.2025.8.19.0031"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_context(viewport={"width": 1366, "height": 900}).new_page()
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
        html = fr.evaluate("() => document.documentElement.outerHTML")
        open(r"C:\Projetos\superJus\Clientes\Renan\03_Documentos_do_Processo\_raspagem_10_08_2026\frame_pje_link.html", "w", encoding="utf-8").write(html)
        page.screenshot(path=r"C:\Projetos\superJus\Clientes\Renan\03_Documentos_do_Processo\_raspagem_10_08_2026\frame_pje_link.png", full_page=True)
        matches = fr.evaluate("""() => {
            const all = Array.from(document.querySelectorAll('*'))
              .filter(el => el.offsetWidth > 0 && el.offsetHeight > 0);
            return all
              .map(el => ({tag: el.tagName, text: (el.textContent||'').trim().slice(0,80)}))
              .filter(x => /acessar|pje/i.test(x.text));
        }""")
        print(f"Elementos com 'acessar' ou 'pje': {len(matches)}")
        for m in matches[:20]:
            print(f"  {m}")
        # Procurar onclick que contenha pje
        onclick_pje = fr.evaluate("""() => {
            return Array.from(document.querySelectorAll('button, a'))
              .filter(el => el.offsetWidth > 0)
              .map(el => ({tag: el.tagName, text: (el.textContent||'').trim().slice(0,40), onclick: (el.getAttribute('onclick') || '').slice(0, 200)}))
              .filter(x => x.onclick && /pje/i.test(x.onclick));
        }""")
        print(f"\nOnclick com PJe:")
        for x in onclick_pje:
            print(f"  {x}")
        browser.close()


if __name__ == "__main__":
    main()
