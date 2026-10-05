# -*- coding: utf-8 -*-
"""
SUPERJUS — CONSULTA PJe 1G TJRJ AO VIVO: PASTOR JUNEO
Acessa o PJe do TJRJ para o processo 0810659-95.2026.8.19.0203
"""

import sys, time, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

proc_fmt = "0810659-95.2026.8.19.0203"
proc_clean = "08106599520268190203"

print("=" * 80)
print(f"🏛️ CONSULTA PJe 1G AO VIVO — PROCESSO {proc_fmt}")
print("=" * 80)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
    ctx = browser.new_context(
        viewport={"width": 1366, "height": 850},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()

    # Tentar URLs do PJe
    urls = [
        "https://tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam",
        "https://tjrj.pje.jus.br/pje/ConsultaPublica/listView.seam"
    ]

    for u in urls:
        print(f"\n[Tentativa] Acessando {u}...")
        try:
            resp = page.goto(u, timeout=20000, wait_until="domcontentloaded")
            print(f"Status HTTP: {resp.status if resp else 'N/A'}")
            time.sleep(3)
            
            body = page.inner_text("body")
            print(f"Tamanho do corpo: {len(body)} caracteres")
            if "numProcesso" in page.content():
                print("✓ Campo numProcesso encontrado na página!")
                
                # Preencher os campos
                page.fill("input[id*='inputNumeroProcesso']", proc_fmt)
                time.sleep(1)
                
                # Clicar pesquisar
                btn = page.query_selector("input[id*='searchProcessos'], button[id*='searchProcessos']")
                if btn:
                    print("✓ Clicando no botão pesquisar...")
                    btn.click()
                    time.sleep(6)
                    
                    res_body = page.inner_text("body")
                    print("\n--- RESULTADO DA CONSULTA NO PJe ---")
                    lines = [l.strip() for l in res_body.splitlines() if l.strip()]
                    for l in lines[:40]:
                        print(f"  • {l}")
                    
                    with open(r"c:\Projetos\superJus\Clientes\Pastor_Juneo\pje_live_result.txt", "w", encoding="utf-8") as f:
                        f.write(res_body)
                    break
            else:
                print(f"Trecho inicial: {body[:300]}")
        except Exception as e:
            print(f"Erro ao acessar {u}: {e}")

    browser.close()

print("\n" + "=" * 80)
print("Fim da tentativa PJe.")
print("=" * 80)
