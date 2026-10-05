# -*- coding: utf-8 -*-
"""Investigar estrutura completa de movimentosProc + tamanho real."""
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

        # Pegar via fetch
        body = f"""() => {{
            return fetch('/consultaprocessual/api/processos/por-numero/movimentos', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{
                    tipoProcesso: '1',
                    codigoProcesso: '2024.002.011419-1',
                    indProcVolumoso: 'N',
                    ultimaOrdemExibida: null,
                }})
            }}).then(r => r.text()).then(t => {{
                const j = JSON.parse(t);
                const movs = j.movimentosProc || [];
                return {{
                    count: movs.length,
                    first_full: movs[0],
                    last_full: movs[movs.length-1],
                    keys_first: Object.keys(movs[0] || {{}}),
                    // Amostra de datas
                    datas_unicas: [...new Set(movs.map(m => (m.dataHora || '').slice(0, 10)))].sort().reverse().slice(0, 15),
                    range_ordem: [movs[0]?.ordem, movs[movs.length-1]?.ordem],
                }};
            }});
        }}"""
        r = fr.evaluate(body)
        print(f"Total movimentos: {r['count']}")
        print(f"Range ordem: {r['range_ordem']}")
        print(f"Keys do primeiro: {r['keys_first']}")
        print(f"Primeiro completo:")
        print(json.dumps(r['first_full'], indent=2, ensure_ascii=False, default=str)[:2000])
        print(f"\nÚltimo completo:")
        print(json.dumps(r['last_full'], indent=2, ensure_ascii=False, default=str)[:1000])
        print(f"\nÚltimas 15 datas:")
        for d in r['datas_unicas']:
            print(f"  {d}")
        browser.close()


if __name__ == "__main__":
    main()
