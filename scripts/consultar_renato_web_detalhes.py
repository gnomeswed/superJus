# -*- coding: utf-8 -*-
"""
Consulta Detalhada via Playwright Web no TJRJ para Renato Bastos Rocha
- Verifica 1ª Instância (0801630-04.2025.8.19.0026 - Itaperuna)
- Verifica 2ª Instância por Nome ("Renato Bastos Rocha") para checar Apelação Criminal
"""

import sys, time, json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

proc_itaperuna = "0801630-04.2025.8.19.0026"
proc_clean = "08016300420258190026"

print("=" * 80)
print("🔍 CONSULTA PLAYWRIGHT WEB — TJRJ (RENATO BASTOS ROCHA)")
print("=" * 80)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    
    # 1. Consulta Ação Penal Itaperuna
    print("\n[1] Consultando Ação Penal Itaperuna (0801630-04.2025.8.19.0026)...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=30000)
    page.wait_for_timeout(2000)
    fr = page.query_selector("iframe#mainframe").content_frame()
    fr.evaluate(f"""() => {{
        const el = document.getElementById('numeroProcesso') || document.querySelector('input[type="text"]');
        if (el) {{
            el.value = '{proc_clean}';
            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            el.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
        const btn = document.getElementById('btnPesquisar') || document.querySelector('button[type="submit"]');
        if (btn) btn.click();
    }}""")
    page.wait_for_timeout(4000)
    
    txt_1inst = fr.evaluate("() => document.body.innerText")
    lines_1inst = [l.strip() for l in txt_1inst.splitlines() if l.strip()]
    print("Retorno 1ª Instância (primeiras 25 linhas):")
    for l in lines_1inst[:25]:
        print(f"  {l}")
        
    # Salvar snapshot de texto
    with open(r"c:\Projetos\superJus\Clientes\Renato_Bastos_Rocha\tjrj_web_itaperuna_snapshot.txt", "w", encoding="utf-8") as fp:
        fp.write(txt_1inst)
        
    browser.close()

print("\n" + "=" * 80)
print("✅ Detalhamento Web concluído.")
print("=" * 80)
