# -*- coding: utf-8 -*-
"""Debug 3: clicar 'Todos os Movimentos' e esperar network idle."""

def main() -> None:
    import sys, time
    from playwright.sync_api import sync_playwright

    sys.stdout.reconfigure(encoding="utf-8")

    PROC = "0011857-95.2024.8.19.0002"
    RAW = r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_raspagem_10_08_2026"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()

        requests = []
        page.on("request", lambda r: requests.append((r.method, r.url[:120], time.time())))
        page.on("response", lambda r: None)

        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        fr = page.query_selector("iframe#mainframe").content_frame()
        time.sleep(2)
        requests.clear()

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

        # Agora clica "Todos os Movimentos" e aguarda muito
        print(">>> Clicando 'Todos os Movimentos' e aguardando...")
        nreq_antes = len(requests)
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
              .find(b => (b.textContent || '').toLowerCase().includes('todos os movimentos'));
            if (btn) btn.click();
        }""")
        time.sleep(15)
        print(f"Requests após clique: {len(requests) - nreq_antes}")
        for r in requests[nreq_antes:]:
            print(" ", r[0], r[1])
        print(f"URL após: {fr.url}")

        # Verifica se há elementos de movimento renderizados
        info = fr.evaluate("""() => {
            const linhas = Array.from(document.querySelectorAll('tr, .movimento, .linha-movimento, [class*=moviment]'));
            return {
                tr_count: linhas.length,
                classes_encontradas: [...new Set(linhas.map(l => l.className).filter(Boolean))].slice(0, 20),
                sample_text: linhas.slice(0, 5).map(l => (l.innerText || '').slice(0, 100)),
            };
        }""")
        print(f"\nLinhas de movimento encontradas: {info['tr_count']}")
        print(f"Classes: {info['classes_encontradas']}")
        print(f"Samples: {info['sample_text']}")

        body = fr.inner_text("body")
        print(f"\nBody length final: {len(body)}")
        print("Últimas 500 chars:")
        print(body[-500:])

        # Salvar HTML final
        html = fr.evaluate("() => document.documentElement.outerHTML")
        open(f"{RAW}\\frame_pos_todos_movimentos.html", "w", encoding="utf-8").write(html)
        open(f"{RAW}\\frame_pos_todos_movimentos.txt", "w", encoding="utf-8").write(body)

        browser.close()


if __name__ == "__main__":
    main()
