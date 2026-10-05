# -*- coding: utf-8 -*-
"""Buscar 2ª instância por NOME com Origem/Comarca/Ano preenchidos."""
import sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

NOME = "Lucas de Souza Freitas"


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_context(viewport={"width": 1366, "height": 900}).new_page()
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        fr = page.query_selector("iframe#mainframe").content_frame()
        time.sleep(2)

        fr.evaluate("""() => {
            const alvo = Array.from(document.querySelectorAll('label, span, a, div, button'))
              .find(c => (c.textContent || '').trim().toLowerCase() === 'por nome');
            if (alvo) alvo.click();
        }""")
        time.sleep(2)

        info = fr.evaluate("""() => {
            const fields = Array.from(document.querySelectorAll('input, select, textarea'))
              .filter(el => el.offsetWidth > 30);
            return fields.map(f => ({
                tag: f.tagName,
                type: f.type,
                name: f.name,
                id: f.id,
                placeholder: f.placeholder,
                label_text: (f.labels && f.labels[0]) ? (f.labels[0].innerText || '').slice(0,40) : '',
                options_count: f.tagName === 'SELECT' ? f.options.length : 0,
            }));
        }""")
        print("Campos do formulário 'Por Nome':")
        for f in info:
            print(f"  - {f}")

        # Abrir dropdown de Origem
        fr.evaluate("""() => {
            const o = document.getElementById('filtroOrigem1');
            if (o) { o.click(); o.focus(); }
        }""")
        time.sleep(1)
        # Tentar selecionar "Tribunal de Justiça (2ª Instância)"
        fr.evaluate("""() => {
            const o = document.getElementById('filtroOrigem1');
            if (o) {
              o.value = 'Tribunal de Justiça';
              o.dispatchEvent(new Event('input', { bubbles: true }));
              o.dispatchEvent(new Event('change', { bubbles: true }));
              o.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', bubbles: true}));
            }
        }""")
        time.sleep(4)

        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
              .find(b => b.offsetWidth > 0 && b.textContent.toLowerCase().includes('pesquisar'));
            if (btn) btn.click();
        }""")
        time.sleep(12)
        body = fr.inner_text("body")
        print(f"\nURL após pesquisa: {fr.url}")
        print("BODY (até 4000 chars):")
        print(body[:4000])
        open(r"C:\\Projetos\\superJus\\Clientes\\Lucas_Freitas\\03_Documentos_do_Processo\\_raspagem_10_08_2026\\2_inst_busca_nome_v2.txt", "w", encoding="utf-8").write(body)
        try:
            page.screenshot(path=r"C:\\Projetos\\superJus\\Clientes\\Lucas_Freitas\\03_Documentos_do_Processo\\_raspagem_10_08_2026\\2_inst_busca_nome_v2.png", full_page=True)
        except Exception:
            pass
        browser.close()


if __name__ == "__main__":
    main()
