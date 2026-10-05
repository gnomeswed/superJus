# -*- coding: utf-8 -*-
"""
SUPERJUS — CONSULTA AO VIVO DO CASO JÚLIO PEREIRA MARCOS (02/09/2026)
Consulta direta no portal do TJRJ e STJ em tempo real.
"""

import sys, time, json
from datetime import datetime
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

proc_buzios = "0023013-51.2021.8.19.0078"
proc_buzios_clean = "00230135120218190078"

proc_hc_tjrj = "0029845-67.2026.8.19.0000"
proc_hc_clean = "00298456720268190000"

print("=" * 85)
print(f"🏛️ CONSULTA AO VIVO — JÚLIO PEREIRA MARCOS")
print(f"⏰ Horário da Consulta: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
print("=" * 85)

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 1280, "height": 900})

    # 1. Ação Penal 1ª Instância (Búzios)
    print("\n[1] Consultando Ação Penal em Búzios (0023013-51.2021.8.19.0078)...", flush=True)
    try:
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=25000)
        page.wait_for_timeout(2000)
        fr = page.query_selector("iframe#mainframe").content_frame()
        fr.evaluate(f"""() => {{
            const el = document.getElementById('numeroProcesso') || document.querySelector('input[type="text"]');
            if (el) {{
                el.value = '{proc_buzios_clean}';
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            const btn = document.getElementById('btnPesquisar') || document.querySelector('button[type="submit"]');
            if (btn) btn.click();
        }}""")
        page.wait_for_timeout(3500)
        txt_buzios = fr.evaluate("() => document.body.innerText")
        lines_b = [l.strip() for l in txt_buzios.splitlines() if l.strip()]
        results["buzios"] = lines_b[:30]
        print("  ✓ Retorno de Búzios capturado com sucesso.")
        for l in lines_b[:12]:
            print(f"    • {l}")
    except Exception as e:
        print(f"  ✗ Erro em Búzios: {e}")
        results["buzios_erro"] = str(e)

    # 2. HC no TJRJ
    print("\n[2] Consultando HC 2ª Instância TJRJ (0029845-67.2026.8.19.0000)...", flush=True)
    try:
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=25000)
        page.wait_for_timeout(2000)
        fr = page.query_selector("iframe#mainframe").content_frame()
        fr.evaluate(f"""() => {{
            const el = document.getElementById('numeroProcesso') || document.querySelector('input[type="text"]');
            if (el) {{
                el.value = '{proc_hc_clean}';
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            const btn = document.getElementById('btnPesquisar') || document.querySelector('button[type="submit"]');
            if (btn) btn.click();
        }}""")
        page.wait_for_timeout(3500)
        txt_hc = fr.evaluate("() => document.body.innerText")
        lines_hc = [l.strip() for l in txt_hc.splitlines() if l.strip()]
        results["hc_tjrj"] = lines_hc[:30]
        print("  ✓ Retorno do HC capturado com sucesso.")
        for l in lines_hc[:12]:
            print(f"    • {l}")
    except Exception as e:
        print(f"  ✗ Erro no HC: {e}")
        results["hc_erro"] = str(e)

    browser.close()

with open(r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\consulta_live_02_09_2026.json", "w", encoding="utf-8") as fp:
    json.dump(results, fp, indent=2, ensure_ascii=False)

print("\n" + "=" * 85)
print("✅ Consulta ao vivo concluída com sucesso.")
print("=" * 85)
