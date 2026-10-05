# -*- coding: utf-8 -*-
"""Tentar STJ/DJEN para Lucas — geralmente bloqueado mas vale tentar."""

def main() -> None:
    import sys, time
    from playwright.sync_api import sync_playwright
    sys.stdout.reconfigure(encoding="utf-8")

    resultados = {}

    # STJ - busca direta por nome do réu
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_context(viewport={"width": 1366, "height": 900}).new_page()
        try:
            page.goto("https://processo.stj.jus.br/processo/pesquisa/?aplicacao=processos.ea&tipoPesquisa=tipoPesquisaNomeParte&parametroNomeParte=Lucas+de+Souza+Freitas",
                      timeout=30000, wait_until="domcontentloaded")
            time.sleep(8)
            body = page.inner_text("body")
            resultados["stj_nome_lucas"] = body[:3000]
        except Exception as e:
            resultados["stj_nome_lucas"] = f"ERRO: {e}"
        browser.close()

    # DJEN - consulta HC
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_context(viewport={"width": 1366, "height": 900}).new_page()
        try:
            page.goto("https://comunica.pje.jus.br/consulta?siglaTribunal=STJ&meio=D", timeout=45000)
            time.sleep(8)
            body = page.inner_text("body")
            resultados["djen_stj"] = body[:3000]
        except Exception as e:
            resultados["djen_stj"] = f"ERRO: {e}"
        browser.close()

    print("\n=== RESULTADOS STJ/DJEN LUCAS ===")
    for k, v in resultados.items():
        print(f"\n--- {k} ---")
        print(v[:500])


if __name__ == "__main__":
    main()
