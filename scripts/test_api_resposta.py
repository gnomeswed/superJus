# -*- coding: utf-8 -*-
"""Capturar API /movimentos via request interception (sem Response.body)."""
import sys, time, json
from playwright.sync_api import sync_playwright


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    PROC = "0011857-95.2024.8.19.0002"

    # Interceptar request e responder manualmente (não funciona pra API, mas serve pra logar)
    captured = {}

    def handle_request(route, request):
        if "/api/processos/por-numero/movimentos" in request.url:
            captured.setdefault("calls", []).append({
                "method": request.method,
                "url": request.url,
                "post_data": request.post_data,
            })
            # Continuar a request normal
            route.continue_()
        else:
            route.continue_()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()
        page.route("**/api/processos/**", handle_request)

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
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
              .find(b => (b.textContent || '').toLowerCase().includes('todos os movimentos'));
            if (btn) btn.click();
        }""")
        time.sleep(15)

        # Agora ler o HTML do frame pra ver se há botão "Carregar mais" / "Próximos"
        print("\n=== Buscando controles de paginação 'Carregar mais' / 'Próximos' / 'Página 2' ===")
        mais = fr.evaluate("""() => {
            const candidates = Array.from(document.querySelectorAll('button, a, span, div'))
              .filter(el => el.offsetWidth > 0)
              .filter(el => {
                const t = (el.textContent || '').toLowerCase();
                return /carregar mais|pr[oó]xim[oa]s?|p[aá]gina \\d|more|next|mais movimentos/i.test(t);
              });
            return candidates.slice(0, 20).map(c => ({
                tag: c.tagName,
                text: (c.textContent || '').trim().slice(0, 80),
                classes: c.className.slice(0, 60),
            }));
        }""")
        print(f"Controles 'carregar mais' encontrados: {len(mais)}")
        for m in mais:
            print(f"  - {m}")

        # Contar movimentos renderizados e botões integrais
        cont = fr.evaluate("""() => {
            const movs = Array.from(document.querySelectorAll('.titulo-movimentacao')).length;
            const integrais = Array.from(document.querySelectorAll('a, button'))
              .filter(el => {
                const t = (el.textContent || '').toLowerCase().trim();
                return el.offsetWidth > 0 && (
                  t.includes('ver íntegra') || t.includes('visualizar ato')
                );
              }).length;
            return {movs, integrais};
        }""")
        print(f"\n  Movimentos renderizados: {cont['movs']}")
        print(f"  Botões integrais: {cont['integrais']}")

        browser.close()

    print(f"\n=== REQUESTS INTERCEPTADAS: {len(captured.get('calls',[]))} ===")
    for c in captured.get("calls", []):
        print(f"  {c['method']} {c['url']}")
        print(f"    body: {c['post_data']!r}")


if __name__ == "__main__":
    main()
