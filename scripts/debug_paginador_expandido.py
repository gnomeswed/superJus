# -*- coding: utf-8 -*-
"""Após carregar processo + expandir 'Todos os Movimentos', verificar paginador 500."""
import sys, time
from playwright.sync_api import sync_playwright


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    PROC = "0011857-95.2024.8.19.0002"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_context(viewport={"width": 1366, "height": 900}).new_page()
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
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
              .find(b => (b.textContent || '').toLowerCase().includes('todos os movimentos'));
            if (btn) btn.click();
        }""")
        time.sleep(15)

        # Agora procurar paginador
        info = fr.evaluate("""() => {
            const all = Array.from(document.querySelectorAll('*'))
              .filter(el => el.offsetWidth > 0 && el.offsetHeight > 0 && el.children.length < 3);
            const paginador = all.map(el => ({
                tag: el.tagName,
                text: (el.innerText || '').trim().slice(0, 40),
                classes: (el.className || '').toString().slice(0, 50),
            })).filter(x => x.text && /500|pagina|^\\s*[<>«»]+\\s*$|\\d+\\s*$/.test(x.text));
            return paginador;
        }""")
        print(f"Elementos relacionados a paginação: {len(info)}")
        for x in info[:30]:
            print(f"  {x}")

        # Selecionar dropdowns visíveis
        selects = fr.evaluate("""() => {
            return Array.from(document.querySelectorAll('select'))
              .filter(s => s.offsetWidth > 0)
              .map(s => ({
                  id: s.id,
                  value: s.value,
                  options: Array.from(s.options).slice(0, 10).map(o => o.text.trim()),
              }));
        }""")
        print(f"\nSelects visíveis: {len(selects)}")
        for s in selects:
            print(f"  {s}")

        page.screenshot(path=r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_raspagem_10_08_2026\view_expandida_pagina.png", full_page=True)
        browser.close()


if __name__ == "__main__":
    main()
