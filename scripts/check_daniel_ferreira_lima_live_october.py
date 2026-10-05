# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import urllib.request
import logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
sys.stdout.reconfigure(encoding="utf-8")

proc_fmt = "0004301-33.2018.8.19.0073"
proc_clean = "00043013320188190073"
hc_fmt = "0105796-38.2024.8.19.0000"

results = {
    "datajud_1a_2a": None,
    "tjrj_portal_1a": None,
    "tjrj_portal_2a": None
}

headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

print("=== 1. CONSULTA DATAJUD CNJ (TJRJ) ===")
url_datajud = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
payload = {"query": {"match": {"numeroProcesso": proc_clean}}, "size": 10}

try:
    req_data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url_datajud, data=req_data, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        hits = res.get('hits', {}).get('hits', [])
        results["datajud_1a_2a"] = [h['_source'] for h in hits]
        print(f"DataJud: {len(hits)} registro(s) encontrado(s).")
except Exception as e:
    print(f"Erro DataJud: {e}")

print("\n=== 2. CONSULTA PORTAL TJRJ AO VIVO (PLAYWRIGHT) ===")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1366, "height": 850}, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    url_portal = "https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica"
    try:
        page.goto(url_portal, timeout=30000, wait_until="domcontentloaded")
        time.sleep(3)
        
        iframe_el = page.wait_for_selector("iframe#mainframe", timeout=15000)
        if iframe_el:
            frame = iframe_el.content_frame()
            if frame:
                inp = frame.query_selector("input[name='numeroProcesso']")
                if inp:
                    inp.fill(proc_fmt)
                    btns = frame.query_selector_all("button")
                    btn = [b for b in btns if any(w in b.inner_text().lower() for w in ["pesquisar", "buscar", "consultar"])][0]
                    btn.click()
                    time.sleep(6)
                    results["tjrj_portal_1a"] = frame.inner_text("body")
    except Exception as e:
        print(f"Erro Portal TJRJ: {e}")
        
    browser.close()

out_path = r"c:\Projetos\superJus\Clientes\Daniel_Ferreira_Lima\02_Movimentacoes\resultado_ao_vivo_01_10_2026.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\nConsulta ao vivo concluída e salva em {out_path}!")
