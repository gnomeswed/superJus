# -*- coding: utf-8 -*-
"""Tentar descobrir o número do processo de apelação pelo protocolo 202600653257."""

def main() -> None:
    import sys, time
    from playwright.sync_api import sync_playwright
    sys.stdout.reconfigure(encoding="utf-8")

    PROT = "202600653257"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_context(viewport={"width": 1366, "height": 900}).new_page()

        # Buscar por "Protocolo"
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        fr = page.query_selector("iframe#mainframe").content_frame()
        time.sleep(2)

        # Tenta clicar em "Por Protocolo"
        fr.evaluate("""() => {
            const alvo = Array.from(document.querySelectorAll('label, span, a, div, button'))
              .find(c => (c.textContent || '').trim().toLowerCase() === 'por protocolo');
            if (alvo) alvo.click();
        }""")
        time.sleep(2)
        fr.evaluate(f"""() => {{
            const inputs = Array.from(document.querySelectorAll('input[type=text], input:not([type])'))
              .filter(i => i.offsetWidth > 50);
            const target = inputs[inputs.length - 1] || inputs[0];
            if (target) {{
              target.value = '{PROT}';
              target.dispatchEvent(new Event('input', {{ bubbles: true }}));
              target.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        }}""")
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
              .find(b => b.offsetWidth > 0 && b.textContent.toLowerCase().includes('pesquisar'));
            if (btn) btn.click();
        }""")
        time.sleep(10)

        body = fr.inner_text("body")
        print("=== URL após pesquisa por protocolo ===")
        print(fr.url)
        print("\n=== BODY ===")
        print(body[:3000])

        page.screenshot(path=r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_raspagem_10_08_2026\2_instancia_por_protocolo.png", full_page=True)
        open(r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_raspagem_10_08_2026\2_instancia_por_protocolo.txt", "w", encoding="utf-8").write(body)
        browser.close()


if __name__ == "__main__":
    main()
