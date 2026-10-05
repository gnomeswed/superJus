# -*- coding: utf-8 -*-
"""Investigar opções de paginação do TJRJ: 'exibir X por página'."""
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
        # Clica em "Todos os Movimentos" para expandir
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
              .find(b => (b.textContent || '').toLowerCase().includes('todos os movimentos'));
            if (btn) btn.click();
        }""")
        time.sleep(15)

        # Dump dos selects do DOM (possíveis "exibir N por página")
        selects = fr.evaluate("""() => {
            return Array.from(document.querySelectorAll('select'))
              .filter(el => el.offsetWidth > 0)
              .map(s => ({
                  id: s.id, name: s.name,
                  options: Array.from(s.options).map(o => ({value: o.value, text: o.text}))
              }));
        }""")
        print("SELECTS ENCONTRADOS:")
        for s in selects:
            print(f"  - id={s['id']} name={s['name']}")
            for o in s['options'][:10]:
                print(f"      [{o['value']}] {o['text']}")

        # Procurar texto "exibir" / "por página" / "página"
        candidatos = fr.evaluate("""() => {
            const all = Array.from(document.querySelectorAll('*'))
              .filter(el => el.offsetWidth > 0 && el.children.length < 5);
            return all
              .map(el => ({tag: el.tagName, text: (el.innerText || '').slice(0, 80)}))
              .filter(o => /exibir|por página|por pagina|registros|pagina/i.test(o.text))
              .slice(0, 30);
        }""")
        print("\nELEMENTOS COM 'exibir/pagina/registros':")
        for c in candidatos:
            print(f"  - {c}")

        # Contar elementos de movimento renderizados
        contagem = fr.evaluate("""() => {
            const tipos = ['.titulo-movimentacao', '.ng-tns-c2046008342-1.ng-star-inserted'];
            const todos = Array.from(document.querySelectorAll('button, a'))
              .filter(el => el.offsetWidth > 0)
              .filter(el => {
                const t = (el.textContent || '').toLowerCase().trim();
                return t.includes('ver íntegra') || t.includes('visualizar ato');
              });
            const movs = Array.from(document.querySelectorAll('.titulo-movimentacao'));
            return {
                integrais_buttons: todos.length,
                movimentos_blocos: movs.length,
            };
        }""")
        print(f"\nCONTAGEM:")
        print(f"  Botões 'Ver Íntegra/Ato': {contagem['integrais_buttons']}")
        print(f"  Blocos 'titulo-movimentacao': {contagem['movimentos_blocos']}")

        browser.close()


if __name__ == "__main__":
    main()
