# -*- coding: utf-8 -*-
"""Buscar 2ª instância por NOME do réu + corréu."""

def main() -> None:
    import sys, time
    from playwright.sync_api import sync_playwright
    sys.stdout.reconfigure(encoding="utf-8")

    nomes = ["Lucas de Souza Freitas", "Ronny Batalha Fernandes"]

    for nome in nomes:
        print(f"\n{'='*70}\n>>> Buscando: {nome}\n{'='*70}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_context(viewport={"width": 1366, "height": 900}).new_page()
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000)
            page.wait_for_selector("iframe#mainframe", timeout=30000)
            fr = page.query_selector("iframe#mainframe").content_frame()
            time.sleep(2)

            # Por Nome
            fr.evaluate("""() => {
                const alvo = Array.from(document.querySelectorAll('label, span, a, div, button'))
                  .find(c => (c.textContent || '').trim().toLowerCase() === 'por nome');
                if (alvo) alvo.click();
            }""")
            time.sleep(2)
            fr.evaluate(f"""() => {{
                const inputs = Array.from(document.querySelectorAll('input[type=text], input:not([type])'))
                  .filter(i => i.offsetWidth > 50);
                const target = inputs[inputs.length - 1] || inputs[0];
                if (target) {{
                  target.value = '{nome}';
                  target.dispatchEvent(new Event('input', {{ bubbles: true }}));
                  target.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            }}""")
            fr.evaluate("""() => {
                const btn = Array.from(document.querySelectorAll('button'))
                  .find(b => b.offsetWidth > 0 && b.textContent.toLowerCase().includes('pesquisar'));
                if (btn) btn.click();
            }""")
            time.sleep(12)
            body = fr.inner_text("body")
            print(f"URL: {fr.url}")
            print("Corpo (até 3000 chars):")
            print(body[:3000])
            # Salvar
            slug = nome.replace(" ", "_").lower()
            open(f"C:\\Projetos\\superJus\\Clientes\\Lucas_Freitas\\03_Documentos_do_Processo\\_raspagem_10_08_2026\\2_inst_nome_{slug}.txt", "w", encoding="utf-8").write(body)
            try:
                page.screenshot(path=f"C:\\Projetos\\superJus\\Clientes\\Lucas_Freitas\\03_Documentos_do_Processo\\_raspagem_10_08_2026\\2_inst_nome_{slug}.png", full_page=True)
            except Exception:
                pass
            browser.close()


if __name__ == "__main__":
    main()
