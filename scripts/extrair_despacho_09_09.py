# -*- coding: utf-8 -*-
import time
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

proc_fmt = "0827233-23.2026.8.19.0001"
print(f"=== EXTRAINDO DESPACHO DE 09/09/2026 — PJe 1G TJRJ ===", flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-blink-features=AutomationControlled'])
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    page.on("dialog", lambda d: d.accept())

    page.goto("https://tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam", wait_until="commit", timeout=60000)
    page.wait_for_selector("#fPP\\:searchProcessos", timeout=45000)

    page.evaluate(f"""() => {{
        var inp = document.getElementById('fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso');
        if (inp) {{
            inp.value = '{proc_fmt}';
            inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
            inp.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
    }}""")
    time.sleep(1)
    page.click("#fPP\\:searchProcessos")
    time.sleep(8)

    proc_link = page.locator(f"a:has-text('{proc_fmt}')").first
    if proc_link.is_visible():
        with context.expect_page(timeout=20000) as new_page_info:
            proc_link.click()
        dp = new_page_info.value
        dp.wait_for_load_state("domcontentloaded", timeout=20000)
        time.sleep(5)

        # Encontrar os links de VISUALIZAR DOCUMENTOS
        doc_links = dp.locator("a:has-text('VISUALIZAR DOCUMENTOS')").all()
        print(f"Total de links de documentos encontrados: {len(doc_links)}", flush=True)

        # Clicar no primeiro link (despacho de 09/09/2026)
        if len(doc_links) > 0:
            print("Abrindo o despacho mais recente (09/09/2026)...", flush=True)
            try:
                with context.expect_page(timeout=10000) as doc_page_info:
                    doc_links[0].click()
                doc_p = doc_page_info.value
                doc_p.wait_for_load_state("domcontentloaded", timeout=15000)
                time.sleep(4)
                txt_despacho = doc_p.inner_text("body")
                out_path = r"c:\Projetos\superJus\Clientes\Leandro_Mecanico\novo_despacho_pje_09_09_2026.txt"
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(txt_despacho)
                print(f"✅ Texto do despacho salvo em: {out_path}", flush=True)
                print("\n--- TEOR DO DESPACHO DE 09/09/2026 ---", flush=True)
                print(txt_despacho, flush=True)
            except Exception as e:
                print(f"Erro ao abrir em nova aba: {e}", flush=True)
                # Verificar se abriu em modal
                modals = dp.inner_text("body")
                print("Texto da tela principal:", modals[:1000])

    browser.close()

print("=== CONCLUÍDO ===", flush=True)
