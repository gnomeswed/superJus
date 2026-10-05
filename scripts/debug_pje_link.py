# -*- coding: utf-8 -*-
"""Clicar no botão 'Acessar PJe' no TJRJ e capturar próxima página."""
import sys, time, json
from pathlib import Path
from playwright.sync_api import sync_playwright


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    PROC = "0821248-17.2025.8.19.0031"
    RAW_DIR = Path(r"C:\Projetos\superJus\Clientes\Renan\03_Documentos_do_Processo\_raspagem_10_08_2026")
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()

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

        # Verificar se apareceu o botão "Acessar PJe"
        botao_pje = fr.evaluate("""() => {
            const alvos = Array.from(document.querySelectorAll('button, a'))
              .filter(el => el.offsetWidth > 0)
              .filter(el => (el.textContent || '').toLowerCase().includes('acessar pje'));
            return alvos.map(a => ({
                tag: a.tagName,
                text: (a.textContent || '').trim(),
                href: a.getAttribute('href'),
                onclick: a.getAttribute('onclick'),
            }));
        }""")
        print(f"Botão 'Acessar PJe': {botao_pje}")

        # Capturar screenshot
        page.screenshot(path=str(RAW_DIR / "tjrj_pje_link.png"), full_page=True)

        # Tentar clicar
        if botao_pje:
            print("Clicando...")
            fr.evaluate("""() => {
                const alvo = Array.from(document.querySelectorAll('button, a'))
                  .find(el => el.offsetWidth > 0 && (el.textContent || '').toLowerCase().includes('acessar pje'));
                if (alvo) alvo.click();
            }""")
            time.sleep(10)
            # Tentar pegar nova URL
            print(f"URL após clique: {page.url}")
            # Pode ter aberto nova aba ou navegação
            pages = ctx.pages
            print(f"Total de abas: {len(pages)}")
            for i, pg in enumerate(pages):
                print(f"  Aba {i}: {pg.url}")

            # Tentar última aba
            last_page = pages[-1]
            last_page.bring_to_front()
            time.sleep(5)
            try:
                body = last_page.inner_text("body")
                print(f"\nBody da última aba (1000 chars):")
                print(body[:1000])
                last_page.screenshot(path=str(RAW_DIR / "pje_pos_clique.png"), full_page=True)
            except Exception as e:
                print(f"err: {e}")

        browser.close()


if __name__ == "__main__":
    main()
