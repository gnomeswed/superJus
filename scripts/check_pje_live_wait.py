# -*- coding: utf-8 -*-
import time
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

proc_fmt = "0808595-36.2026.8.19.0002"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-blink-features=AutomationControlled'])
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0")
    page = context.new_page()
    page.goto("https://tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam", wait_until="commit", timeout=60000)
    page.wait_for_selector("#fPP\\:searchProcessos", timeout=45000)
    
    page.evaluate(f"""() => {{
        var inp = document.getElementById('fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso');
        if (inp) {{
            inp.value = '{proc_fmt}';
            inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
            inp.dispatchEvent(new Event('change', {{ bubbles: true }}));
            inp.dispatchEvent(new Event('blur', {{ bubbles: true }}));
        }}
    }}""")
    time.sleep(2)
    page.click("#fPP\\:searchProcessos")
    
    # Wait explicitly for the table row to appear
    print("Aguardando retorno da tabela...")
    try:
        page.wait_for_selector("a:has-text('0808595'), a:has-text('VER DETALHES')", timeout=25000)
        print("Tabela carregou com sucesso!")
        txt_res = page.inner_text("#fPP\\:processosTable")
        print("RESUMO:\n", txt_res)
        
        with context.expect_page(timeout=25000) as np:
            page.locator("a:has-text('0808595'), a:has-text('VER DETALHES')").first.click()
        dp = np.value
        dp.wait_for_load_state("domcontentloaded")
        time.sleep(4)
        
        detalhes = dp.inner_text("body")
        lines = [l.strip() for l in detalhes.splitlines() if l.strip()]
        out_f = r"c:\Projetos\superJus\Clientes\Lucas_Dias_Oliveira\03_Documentos_do_Processo\detalhes_pje_lucas_taxista_live_01_10_2026.txt"
        with open(out_f, "w", encoding="utf-8") as f:
            f.write(detalhes)
        print(f"Salvo em {out_f}. Total linhas: {len(lines)}")
        
        print("\nTOP MOVIMENTAÇÕES:")
        idx = -1
        for i, l in enumerate(lines):
            if "Movimentações do Processo" in l:
                idx = i
                break
        if idx != -1:
            for l in lines[idx:idx+35]:
                print("  •", l)
    except Exception as e:
        print("Erro / Timeout:", e)
        page.screenshot(path="scratch_pje_01out.png")
        print("Body:", page.inner_text("body")[:500])
    
    browser.close()
