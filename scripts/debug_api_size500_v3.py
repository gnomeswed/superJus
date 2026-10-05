# -*- coding: utf-8 -*-
"""Testar size=500 com codigoProcesso correto (com máscara)."""
import sys, time, json
from playwright.sync_api import sync_playwright


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    PROC = "0011857-95.2024.8.19.0002"

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

        # codigoProcesso correto
        codigo = PROC
        # Testar todas variantes
        for variant in [
            {},
            {"size": 500},
            {"pageSize": 500},
            {"itemsPerPage": 500},
            {"registrosPorPagina": 500},
            {"qtd": 500},
            {"page": 0, "size": 500},
            {"pagina": 0, "tamanhoPagina": 500},
        ]:
            body = f"""() => {{
                return fetch('/consultaprocessual/api/processos/por-numero/movimentos', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify(Object.assign({{
                        tipoProcesso: '1',
                        codigoProcesso: '{codigo}',
                        indProcVolumoso: 'N',
                        ultimaOrdemExibida: null,
                    }}, {json.dumps(variant)}))
                }}).then(r => r.text()).then(t => {{
                    try {{
                        const j = JSON.parse(t);
                        var info = {{type: Array.isArray(j) ? ('array[' + j.length + ']') : 'object'}};
                        if (Array.isArray(j) && j.length > 0) info.first_item = JSON.stringify(j[0]).slice(0, 300);
                        if (j.movimentos) info.count = j.movimentos.length;
                        if (typeof j === 'object' && !Array.isArray(j)) info.top_keys = Object.keys(j).slice(0, 15);
                        return info;
                    }} catch (e) {{ return {{error: e.toString().slice(0, 80), raw_start: t.slice(0, 300)}}; }}
                }}).catch(e => ({{error: e.toString().slice(0, 80)}}));
            }}"""
            r = fr.evaluate(body)
            print(f"  {variant!r}: type={r.get('type','err')}  count={r.get('count','-')}  top={r.get('top_keys',[])[:5]}  err={r.get('error','-')}")
            if r.get('first_item'):
                print(f"    first: {r['first_item']}")
        browser.close()


if __name__ == "__main__":
    main()
