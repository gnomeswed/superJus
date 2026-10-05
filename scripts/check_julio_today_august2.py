# -*- coding: utf-8 -*-
import time
import os
import sys
import json
import urllib.request
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== CHECAGEM EM TEMPO REAL — HOJE (02/08/2026) PARA JÚLIO PEREIRA MARCOS ===")

# 1. Consulta Datajud
url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}

req_data = json.dumps({"query": {"match": {"numeroProcesso": "00230135120218190078"}}, "size": 10}).encode('utf-8')
req = urllib.request.Request(url, data=req_data, headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        hits = res.get('hits', {}).get('hits', [])
        print(f"Datajud API retornou {len(hits)} registros.")
except Exception as e:
    print(f"Datajud erro: {e}")

# 2. Playwright TJRJ ao vivo
target_file = r"c:\Projetos\superJus\tjrj_today_check_02082026.txt"
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        page = ctx.new_page()
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=60000)
        time.sleep(4)
        
        frame = page.frame_locator("iframe#mainframe")
        frame.locator("input[name='numeroProcesso']").fill("0023013-51.2021.8.19.0078")
        time.sleep(1)
        frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
        time.sleep(6)
        
        try:
            frame.locator("button:has-text('Todos Os Movimentos')").first.click()
            time.sleep(4)
        except Exception:
            pass
            
        real_frame = page.query_selector("iframe#mainframe").content_frame()
        txt = real_frame.inner_text("body")
        
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(txt)
        print("Sucesso! Captura do TJRJ salva em " + target_file)
        browser.close()
except Exception as e:
    print(f"Playwright erro: {e}")
