# -*- coding: utf-8 -*-
"""Debug: investigar URL exata + view que o usuário viu."""
import sys, time
from playwright.sync_api import sync_playwright


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    PROC = "0011857-95.2024.8.19.0002"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_context(viewport={"width": 1366, "height": 900}).new_page()
        # Tentar ir direto pra #porNumero como o usuário
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica#porNumero", timeout=45000)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        fr = page.query_selector("iframe#mainframe").content_frame()
        time.sleep(3)

        print(f"URL após goto: {page.url}")
        print(f"Frame URL:     {fr.url}")

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
        print(f"\nURL após pesquisar: {page.url}")
        print(f"Frame URL:          {fr.url}")

        # Dump de todos elementos - procurar paginador
        print("\n=== TODOS OS ELEMENTOS VISÍVEIS COM TEXTO ===")
        info = fr.evaluate("""() => {
            const all = Array.from(document.querySelectorAll('*'))
              .filter(el => el.offsetWidth > 0 && el.offsetHeight > 0 && el.children.length < 3);
            return all.map(el => ({
                tag: el.tagName,
                text: (el.innerText || '').trim().slice(0, 80),
                type: el.type || '',
                classes: (el.className || '').toString().slice(0, 40),
            })).filter(x => x.text);
        }""")
        print(f"Total: {len(info)}")
        for i in info:
            print(f"  {i['tag']:6} {i['type']:8} | {i['text']}")

        page.screenshot(path=r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_raspagem_10_08_2026\debug_view_atual.png", full_page=True)
        browser.close()


if __name__ == "__main__":
    main()
