# -*- coding: utf-8 -*-
"""
SUPERJUS — CONSULTA DIRETA AO VIVO NO STJ DO HC 1.116.750 / RJ (JÚLIO PEREIRA MARCOS)
Acessa o portal oficial do Superior Tribunal de Justiça pelo número de registro 2026/0311210-7.
"""

import sys, time
from datetime import datetime
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

registro_stj = "202603112107"
url_stj = f"https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo={registro_stj}"

print("=" * 85)
print(f"🏛️ CONSULTA AO VIVO STJ — HC 1.116.750 / RJ (JÚLIO PEREIRA MARCOS)")
print(f"⏰ Horário da Consulta: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
print("=" * 85)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()
    try:
        page.goto(url_stj, timeout=30000, wait_until="domcontentloaded")
        time.sleep(5)
        
        # Obter texto do processo
        txt = page.inner_text("body")
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        
        print(f"Status da consulta no STJ: {len(lines)} linhas capturadas.")
        print("\n--- RESUMO DAS LINHAS EXTRAÍDAS DO STJ ---")
        for l in lines[:35]:
            print(f"  • {l}")
            
        with open(r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\stj_live_snapshot_02_09_2026.txt", "w", encoding="utf-8") as fp:
            fp.write(txt)
    except Exception as e:
        print(f"Erro ao consultar STJ: {e}")
    finally:
        browser.close()

print("\n" + "=" * 85)
print("✅ Varredura no STJ concluída.")
print("=" * 85)
