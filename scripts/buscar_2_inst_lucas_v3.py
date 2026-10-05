# -*- coding: utf-8 -*-
"""2ª instância - estratégia: ng-select precisa de digitação + Enter."""

def main() -> None:
    import sys, time, json
    from playwright.sync_api import sync_playwright
    sys.stdout.reconfigure(encoding="utf-8")

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

        # Preencher Ano (vão juntos)
        fr.evaluate("""() => {
            document.getElementById('anoInicial1').value = '2024';
            document.getElementById('anoFinal1').value = '2026';
            ['anoInicial1','anoFinal1'].forEach(id => {
              const el = document.getElementById(id);
              el.dispatchEvent(new Event('input', { bubbles: true }));
              el.dispatchEvent(new Event('change', { bubbles: true }));
            });
        }""")
        time.sleep(1)

        # Nome da parte
        fr.evaluate("""() => {
            const el = document.getElementById('nomeParte');
            el.value = 'Lucas de Souza Freitas';
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }""")
        time.sleep(1)

        # Comarca - ng-select: clicar, digitar, selecionar opção
        comarca_sel = "#filtroComarca1"
        fr.evaluate(f"""(sel) => {{
            const el = document.querySelector(sel);
            if (el) {{
              el.click();
              el.focus();
            }}
        }}""", comarca_sel)
        time.sleep(2)
        # Ver o que apareceu (opções)
        open_opts = fr.evaluate("""() => {
            const opts = Array.from(document.querySelectorAll('[role=option], .ng-option, .dropdown-item, ng-dropdown-panel .ng-option'));
            return opts.slice(0, 30).map(o => (o.innerText || o.textContent || '').trim().slice(0, 60));
        }""")
        print(f"Opções visíveis após clicar Comarca: {open_opts}")

        # Tentar digitar no campo
        fr.evaluate("""() => {
            const el = document.getElementById('filtroComarca1');
            if (el) {
              el.value = '';
              el.focus();
            }
        }""")
        fr.type("#filtroComarca1", "Niterói", delay=200)
        time.sleep(2)
        open_opts2 = fr.evaluate("""() => {
            const opts = Array.from(document.querySelectorAll('[role=option], .ng-option, .dropdown-item'));
            return opts.slice(0, 30).map(o => (o.innerText || o.textContent || '').trim().slice(0, 60));
        }""")
        print(f"Opções após digitar: {open_opts2}")

        # Selecionar primeira que case com Niterói
        if any("niterói" in o.lower() for o in open_opts2):
            # clicar
            fr.evaluate("""() => {
                const opts = Array.from(document.querySelectorAll('[role=option], .ng-option'));
                const match = opts.find(o => /niterói/i.test(o.innerText || o.textContent || ''));
                if (match) match.click();
            }""")
            time.sleep(1)
        elif open_opts2:
            # Clicar primeira
            fr.evaluate("""() => {
                const opts = Array.from(document.querySelectorAll('[role=option], .ng-option'));
                if (opts[0]) opts[0].click();
            }""")
            time.sleep(1)

        # Origem: idem ng-select
        fr.evaluate("""() => {
            const el = document.getElementById('filtroOrigem1');
            if (el) { el.click(); el.focus(); el.value = ''; }
        }""")
        time.sleep(1)
        fr.type("#filtroOrigem1", "Tribunal", delay=200)
        time.sleep(2)
        open_origem = fr.evaluate("""() => {
            const opts = Array.from(document.querySelectorAll('[role=option], .ng-option'));
            return opts.slice(0, 10).map(o => (o.innerText || o.textContent || '').trim().slice(0, 60));
        }""")
        print(f"Opções Origem: {open_origem}")
        fr.evaluate("""() => {
            const opts = Array.from(document.querySelectorAll('[role=option], .ng-option'));
            const match = opts.find(o => /tribunal|2.*inst/i.test(o.innerText || o.textContent || ''));
            if (match) match.click();
            else if (opts[0]) opts[0].click();
        }""")
        time.sleep(1)

        # Pesquisar
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
              .find(b => b.offsetWidth > 0 && b.textContent.toLowerCase().includes('pesquisar'));
            if (btn) btn.click();
        }""")
        time.sleep(12)
        body = fr.inner_text("body")
        print(f"\nURL: {fr.url}")
        print(f"BODY (até 4000 chars):")
        print(body[:4000])
        open(r"C:\\Projetos\\superJus\\Clientes\\Lucas_Freitas\\03_Documentos_do_Processo\\_raspagem_10_08_2026\\2_inst_v3.txt", "w", encoding="utf-8").write(body)
        page.screenshot(path=r"C:\\Projetos\\superJus\\Clientes\\Lucas_Freitas\\03_Documentos_do_Processo\\_raspagem_10_08_2026\\2_inst_v3.png", full_page=True)
        browser.close()


if __name__ == "__main__":
    main()
