# -*- coding: utf-8 -*-
import json
import urllib.request
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== CONSULTA DO PROCESSO 0175803-86.2023.8.19.0001 ===")

target_dir = r"c:\Projetos\superJus\temp_logs_e_resultados"
os.makedirs(target_dir, exist_ok=True)

# 1. Consulta Datajud
headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNxLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

proc_clean = "01758038620238190001"
url_tjrj = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'

req_data = json.dumps({"query": {"match": {"numeroProcesso": proc_clean}}, "size": 10}).encode('utf-8')
req = urllib.request.Request(url_tjrj, data=req_data, headers=headers)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        hits = res.get('hits', {}).get('hits', [])
        print(f"\n📌 Datajud returned {len(hits)} records:")
        for hit in hits:
            src = hit['_source']
            classe = src.get('classe', {}).get('nome', 'N/I')
            orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
            movs = src.get('movimentos', [])
            movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
            print(f"   • Órgão: {orgao} | Classe: {classe} | Total Movs: {len(movs)}")
            for m in movs_sorted[:15]:
                dt = m.get('dataHora', '')[:19].replace('T', ' ')
                nome = m.get('nome', '')
                print(f"     - {dt} | {nome}")
except Exception as e:
    print(f"Erro Datajud: {e}")

# 2. Playwright scraping do link direto
target_url = "https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica?numProcessoCNJ=0175803-86.2023.8.19.0001"
print(f"\n2. Abrindo URL fornecida pelo usuário:\n   {target_url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 1280, "height": 800})

    try:
        page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(5)

        # Screenshot inicial
        ss = os.path.join(target_dir, "processo_0175803_screenshot.png")
        page.screenshot(path=ss)
        print(f"✅ Screenshot salvo: {ss}")

        # Tentar interagir com o iframe se existir
        txt = ""
        try:
            frame = page.frame_locator("iframe#mainframe")
            try:
                frame.locator("button:has-text('Todos Os Movimentos')").first.click()
                time.sleep(2)
            except Exception:
                pass
            real_frame = page.query_selector("iframe#mainframe").content_frame()
            txt = real_frame.inner_text("body")
        except Exception:
            txt = page.inner_text("body")

        out_txt = os.path.join(target_dir, "processo_0175803_extrato.txt")
        with open(out_txt, "w", encoding="utf-8") as f:
            f.write(txt)

        print(f"✅ Extrato salvo em: {out_txt}\n")

        lines = [l.strip() for l in txt.split('\n') if l.strip()]
        print("--- CONTEÚDO EXTRAÍDO DA PÁGINA DO PROCESSO ---")
        for i, l in enumerate(lines[:35], start=1):
            print(f"  {i:02d}. {l[:120]}")

    except Exception as e:
        print(f"Erro no Playwright: {e}")

    browser.close()

print("\n=== CONSULTA CONCLUÍDA ===")
