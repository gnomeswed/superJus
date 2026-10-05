# -*- coding: utf-8 -*-
import time
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
proc_fmt = "0827233-23.2026.8.19.0001"

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

        # Buscar linhas que mencionem 30/09 ou petição
        rows = dp.locator("tr").all()
        print(f"Total de linhas na página de detalhes: {len(rows)}")
        for r in rows:
            txt = r.inner_text().strip()
            if "30/09/2026" in txt or "29/09/2026" in txt or "Mandado" in txt:
                print(f"  ROW: {txt.replace(chr(10), ' | ')}")

    browser.close()
