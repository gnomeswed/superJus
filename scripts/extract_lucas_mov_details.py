# -*- coding: utf-8 -*-
import time
import sys
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

proc_fmt = '0808595-36.2026.8.19.0002'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-blink-features=AutomationControlled'])
    context = browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0')
    page = context.new_page()
    page.goto('https://tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam', wait_until='commit', timeout=60000)
    page.wait_for_selector('#fPP\\:searchProcessos', timeout=45000)
    page.evaluate(f"""() => {{
        var inp = document.getElementById('fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso');
        if (inp) inp.value = '{proc_fmt}';
    }}""")
    page.click('#fPP\\:searchProcessos')
    time.sleep(8)
    
    with context.expect_page(timeout=25000) as np:
        page.locator(f"a:has-text('{proc_fmt}')").first.click()
    dp = np.value
    dp.wait_for_load_state('domcontentloaded')
    time.sleep(4)
    
    # Extract the movement table rows with details
    movs = dp.evaluate('''() => {
        const rows = Array.from(document.querySelectorAll('tr, .rich-table-row, [id*="movimentacao"]'));
        return rows.map(r => ({
            text: r.innerText.replace(/\\s+/g, ' ').trim(),
            html: r.innerHTML
        })).filter(r => r.text.includes('28/09/2026') || r.text.includes('15/09/2026') || r.text.includes('14/09/2026'));
    }''')
    for m in movs:
        print('ROW:', m['text'])
        print('HTML:', m['html'])
        print('-'*50)
    browser.close()
