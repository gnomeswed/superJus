# -*- coding: utf-8 -*-
"""Debug: confirmar que o dropdown 500 está visível após carregar o processo (sem expandir Todos Mov)."""
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

        # SEM clicar em "Todos os Movimentos" - view resumida
        print("=== VIEW RESUMIDA (sem expandir) ===")
        info = fr.evaluate("""() => {
            const selects = Array.from(document.querySelectorAll('select'))
              .filter(s => s.offsetWidth > 0)
              .map(s => ({
                  id: s.id, name: s.name,
                  value: s.value,
                  options: Array.from(s.options).map(o => ({value: o.value, text: o.text.trim()})),
                  classes: s.className.slice(0, 80),
              }));
            return selects;
        }""")
        print(f"Selects visíveis: {len(info)}")
        for s in info:
            print(f"  - id={s['id']} name={s['name']} value={s['value']!r}")
            print(f"    classes: {s['classes']}")
            for o in s['options']:
                print(f"    [{o['value']}] {o['text']}")

        # Contar botões integrais
        cont = fr.evaluate("""() => {
            return Array.from(document.querySelectorAll('a, button'))
              .filter(el => {
                const t = (el.textContent || '').toLowerCase().trim();
                return el.offsetWidth > 0 && (
                  t.includes('ver íntegra') || t.includes('visualizar ato')
                );
              }).length;
        }""")
        print(f"\nBotões integrais na view resumida: {cont}")

        page.screenshot(path=r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_raspagem_10_08_2026\view_resumida_paginador.png", full_page=True)
        browser.close()


if __name__ == "__main__":
    main()
