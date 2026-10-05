# -*- coding: utf-8 -*-
"""
SUPERJUS — CONSULTA PJe 1G TJRJ AO VIVO: LEANDRO DA SILVA (LEANDRO MECÂNICO)
Processo: 0827233-23.2026.8.19.0001
1ª Vara Criminal da Regional de Santa Cruz / TJRJ
"""

import sys, time, json, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

proc_fmt = "0827233-23.2026.8.19.0001"
proc_clean = "08272332320268190001"

print("=" * 85, flush=True)
print(f"🏛️ CONSULTA PJe 1G TJRJ AO VIVO — PROCESSO {proc_fmt} (LEANDRO MECÂNICO)", flush=True)
print("=" * 85, flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
    ctx = browser.new_context(
        viewport={"width": 1400, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()

    url = "https://tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam"
    print(f"1. Acessando {url}...", flush=True)
    page.goto(url, timeout=30000, wait_until="domcontentloaded")
    time.sleep(2)

    print(f"2. Preenchendo número {proc_fmt}...", flush=True)
    page.fill("input[id*='inputNumeroProcesso']", proc_fmt)
    time.sleep(1)

    btn = page.query_selector("input[id*='searchProcessos'], button[id*='searchProcessos']")
    if btn:
        btn.click()
        time.sleep(5)

    res_body = page.inner_text("body")
    print(f"3. Resposta da busca recebida ({len(res_body)} caracteres).", flush=True)

    link_detalhes = page.locator(f"a:has-text('{proc_fmt}'), a[title*='detalhes'], a:has-text('VER DETALHES')").first
    
    if link_detalhes.is_visible():
        print("✓ Link de detalhes do processo localizado! Abrindo autos digitais...", flush=True)
        with ctx.expect_page(timeout=15000) as new_page_info:
            link_detalhes.click()
            time.sleep(3)

        dp = new_page_info.value
        dp.wait_for_load_state("domcontentloaded")
        time.sleep(4)

        txt_detalhes = dp.inner_text("body")
        out_txt = r"c:\Projetos\superJus\Clientes\Leandro_Mecanico\detalhes_pje_leandro_0827233.txt"
        os.makedirs(os.path.dirname(out_txt), exist_ok=True)
        with open(out_txt, "w", encoding="utf-8") as f:
            f.write(txt_detalhes)

        print(f"\n✅ Detalhes salvos com sucesso em: {out_txt}", flush=True)
        print("\n--- LINHAS DO PROCESSO EXTRAÍDAS DO PJe ---", flush=True)
        lines = [l.strip() for l in txt_detalhes.splitlines() if l.strip()]
        for l in lines[:70]:
            print(f"  • {l}", flush=True)
    else:
        print("⚠️ Link de detalhes não encontrado diretamente. Analisando texto da consulta pública...", flush=True)
        out_txt = r"c:\Projetos\superJus\Clientes\Leandro_Mecanico\detalhes_pje_leandro_0827233.txt"
        with open(out_txt, "w", encoding="utf-8") as f:
            f.write(res_body)
        for l in [x.strip() for x in res_body.splitlines() if x.strip()][:50]:
            print(f"  • {l}", flush=True)

    browser.close()

print("\n=== CONSULTA PJe CONCLUÍDA ===", flush=True)
