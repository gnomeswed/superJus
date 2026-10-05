# -*- coding: utf-8 -*-
"""Investigar API /api/processos/por-numero/movimentos - ver se tem paginação."""
import sys, time, json
from playwright.sync_api import sync_playwright


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    PROC = "0011857-95.2024.8.19.0002"

    responses = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_context(viewport={"width": 1366, "height": 900}).new_page()

        def on_response(resp):
            try:
                if "/api/processos" in resp.url or "/api/publica" in resp.url:
                    ct = resp.headers.get("content-type", "")
                    if "json" in ct.lower():
                        body = resp.body()
                        responses.append({
                            "url": resp.url,
                            "status": resp.status,
                            "size": len(body),
                            "headers": dict(resp.headers),
                            "body": body[:5000].decode("utf-8", errors="replace") if body else "",
                        })
            except Exception:
                pass

        page.on("response", on_response)

        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        fr = page.query_selector("iframe#mainframe").content_frame()
        time.sleep(2)

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
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
              .find(b => (b.textContent || '').toLowerCase().includes('todos os movimentos'));
            if (btn) btn.click();
        }""")
        time.sleep(15)
        browser.close()

    print(f"\n{len(responses)} respostas API capturadas:")
    for r in responses:
        print(f"\n--- {r['status']} {r['url'][:120]}  ({r['size']} B) ---")
        print(f"Headers relevantes:")
        for k, v in r["headers"].items():
            if any(x in k.lower() for x in ["content-type", "content-length", "x-total", "link", "next", "page"]):
                print(f"  {k}: {v[:120]}")
        if r["body"]:
            try:
                j = json.loads(r["body"])
                if isinstance(j, dict):
                    # Top-level keys
                    print(f"Top keys: {list(j.keys())}")
                    # Se tem movimentos, contar
                    if "movimentos" in j:
                        print(f"  -> {len(j['movimentos'])} movimentos")
                    if "data" in j and isinstance(j["data"], list):
                        print(f"  -> data: {len(j['data'])} itens")
                    # Procura indicadores de paginação
                    for pag_key in ["page", "total", "totalPages", "size", "hasNext", "nextPage", "links", "paginacao"]:
                        if pag_key in j:
                            print(f"  -> {pag_key}: {j[pag_key]}")
            except Exception as e:
                print(f"  (não é JSON): {e}")


if __name__ == "__main__":
    main()
