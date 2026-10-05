# -*- coding: utf-8 -*-
"""Pegar codigoProcesso interno + testar size=500."""
import sys, time, json
from playwright.sync_api import sync_playwright


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    PROC = "0011857-95.2024.8.19.0002"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()

        captured = []
        def on_req(req):
            if "/api/processos/por-numero" in req.url:
                captured.append({"url": req.url, "method": req.method, "body": req.post_data})
        page.on("request", on_req)

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
        # Expandir
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
              .find(b => (b.textContent || '').toLowerCase().includes('todos os movimentos'));
            if (btn) btn.click();
        }""")
        time.sleep(15)

        print(f"Captured: {len(captured)} requests")
        for c in captured:
            print(f"  {c['method']} {c['url'][:120]}")
            print(f"    body: {c['body']!r}")

        # Pegar codigoProcesso interno (do POST de movimentos)
        codigo = None
        for c in captured:
            if "movimentos" in c["url"] and c["body"]:
                j = json.loads(c["body"])
                codigo = j.get("codigoProcesso")
                break
        print(f"\ncodigoProcesso interno: {codigo}")

        # Agora testar size variants
        for variant in [
            {},
            {"size": 500},
            {"pageSize": 500},
            {"itemsPerPage": 500},
            {"registrosPorPagina": 500},
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
                        if (Array.isArray(j)) return {{type: 'array[' + j.length + ']', first: JSON.stringify(j[0]).slice(0,300)}};
                        // Procurar movimentos recursivamente
                        function findMovs(obj, depth) {{
                            if (depth > 3) return null;
                            if (!obj || typeof obj !== 'object') return null;
                            for (var k of Object.keys(obj)) {{
                                if (Array.isArray(obj[k]) && obj[k].length > 0 && typeof obj[k][0] === 'object' && (obj[k][0].nome || obj[k][0].ordem)) {{
                                    return {{key: k, count: obj[k].length, first: obj[k][0]}};
                                }}
                                var found = findMovs(obj[k], depth + 1);
                                if (found) return found;
                            }}
                            return null;
                        }}
                        var movsFound = findMovs(j, 0);
                        var info = {{type: 'object', top_keys: Object.keys(j), size: t.length}};
                        if (movsFound) {{
                            info.movs_key = movsFound.key;
                            info.movs_count = movsFound.count;
                            info.movs_first_ordem = movsFound.first.ordem;
                            info.movs_first_desc = (movsFound.first.nome || '').slice(0, 60);
                            info.movs_first_date = movsFound.first.dataHora;
                        }}
                        return info;
                    }} catch (e) {{ return {{error: e.toString().slice(0, 80), raw_start: t.slice(0, 200), raw_size: t.length}}; }}
                }}).catch(e => ({{error: e.toString().slice(0, 80)}}));
            }}"""
            r = fr.evaluate(body)
            if r.get("type", "").startswith("array"):
                print(f"  {variant!r}: ERRO: {r.get('first', '?')[:100]}")
            else:
                print(f"  {variant!r}: size={r.get('size','?')}  movs_key={r.get('movs_key','-')}  movs_count={r.get('movs_count','-')}")
                if r.get('movs_first_ordem'):
                    print(f"    first_ordem={r['movs_first_ordem']}  date={r['movs_first_date']}  desc={r['movs_first_desc']!r}")
        browser.close()


if __name__ == "__main__":
    main()
