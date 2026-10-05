# -*- coding: utf-8 -*-
"""Tentar forçar size=500 via API direta (com sessão do Playwright)."""
import sys, time, json
from playwright.sync_api import sync_playwright


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    PROC = "0011857-95.2024.8.19.0002"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        time.sleep(3)

        # Pegar o codigoProcesso (via fazer um clique primeiro pra saber)
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
        time.sleep(8)
        print(f"Frame URL após pesquisar: {fr.url}")
        # Extrair codigoProcesso
        m = fr.url.split("codigoProcesso=")
        codigo = m[1].split("&")[0] if len(m) > 1 else "?"
        print(f"codigoProcesso: {codigo}")

        # Tentar POST com size=500 via Playwright fetch (cookies automaticamente)
        body_com_size = f"""() => {{
            return fetch('/consultaprocessual/api/processos/por-numero/movimentos', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{
                    tipoProcesso: '1',
                    codigoProcesso: '{codigo}',
                    indProcVolumoso: 'N',
                    ultimaOrdemExibida: null,
                    size: 500,
                    page: 0,
                }})
            }}).then(r => r.json()).then(j => {{
                return {{
                    total_movimentos: (j.movimentos || []).length,
                    first: j.movimentos ? j.movimentos[0] : null,
                    last: j.movimentos ? j.movimentos[j.movimentos.length-1] : null,
                    pagination_keys: Object.keys(j).filter(k => /page|size|total|has|next/i.test(k)),
                    has_mov_field: 'movimentos' in j,
                }};
            }}).catch(e => ({{error: e.toString()}}));
        }}"""
        result = fr.evaluate(body_com_size)
        print(f"\nResultado size=500: {json.dumps(result, indent=2, ensure_ascii=False, default=str)[:2000]}")

        # Tentar com pageSize / itemsPerPage
        for variant in [
            {"pageSize": 500},
            {"itemsPerPage": 500},
            {"registrosPorPagina": 500},
            {"quantidade": 500},
            {"qtd": 500},
        ]:
            variant_body = f"""() => {{
                return fetch('/consultaprocessual/api/processos/por-numero/movimentos', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify(Object.assign({{
                        tipoProcesso: '1',
                        codigoProcesso: '{codigo}',
                        indProcVolumoso: 'N',
                        ultimaOrdemExibida: null,
                    }}, {json.dumps(variant)}))
                }}).then(r => r.json()).then(j => ({{
                    count: (j.movimentos || []).length,
                    keys: Object.keys(j).slice(0, 15),
                }})).catch(e => ({{error: e.toString()}}));
            }}"""
            r = fr.evaluate(variant_body)
            print(f"  variant={variant}: {r}")
        browser.close()


if __name__ == "__main__":
    main()
