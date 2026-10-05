# -*- coding: utf-8 -*-
"""Pegar codigoProcesso e testar variantes de size."""
import sys, time, json
from playwright.sync_api import sync_playwright


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    PROC = "0011857-95.2024.8.19.0002"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()

        captured = {}
        def on_req(req):
            if "/api/processos" in req.url:
                captured["url"] = req.url
                captured["body"] = req.post_data
        page.on("request", on_req)

        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000)
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
        time.sleep(8)
        print(f"URL: {captured.get('url')}")
        print(f"BODY: {captured.get('body')}")

        # Extrair codigoProcesso da URL
        url = captured.get('url', '')
        codigo = "?"
        if "codigoProcesso=" in url:
            codigo = url.split("codigoProcesso=")[1].split("&")[0]
        print(f"\ncodigoProcesso: {codigo}")

        # Testar POST com fetch + size 500
        body_template = f"""() => {{
            return fetch('/consultaprocessual/api/processos/por-numero/movimentos', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{
                    tipoProcesso: '1',
                    codigoProcesso: '{codigo}',
                    indProcVolumoso: 'N',
                    ultimaOrdemExibida: null,
                    size: 500,
                }})
            }}).then(r => r.text()).then(t => {{
                try {{
                    const j = JSON.parse(t);
                    return {{
                        count: (j.movimentos || []).length,
                        keys: Object.keys(j).slice(0, 15),
                        first_ordem: j.movimentos ? j.movimentos[0]?.ordem : null,
                        last_ordem: j.movimentos ? j.movimentos[j.movimentos.length-1]?.ordem : null,
                    }};
                }} catch (e) {{ return {{error: e.toString(), raw: t.slice(0, 500)}}; }}
            }}).catch(e => ({{error: e.toString()}}));
        }}"""
        print("\n--- POST com size=500 ---")
        r = fr.evaluate(body_template)
        print(json.dumps(r, indent=2, ensure_ascii=False, default=str))
        browser.close()


if __name__ == "__main__":
    main()
