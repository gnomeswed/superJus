# -*- coding: utf-8 -*-
import time
import os
import json
import urllib.request
from playwright.sync_api import sync_playwright

proc_num = "0023013-51.2021.8.19.0078"
proc_num_clean = "00230135120218190078"
target_file = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\check_online_13h22.txt"

print(f"=== VERIFICAÇÃO ONLINE EM TEMPO REAL — 29/07/2026 ÀS 13H22 ===")

# 1. Consulta ao Datajud API
url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

datajud_txt = ""
try:
    req_data = json.dumps({"query": {"match": {"numeroProcesso": proc_num_clean}}, "size": 10}).encode('utf-8')
    req = urllib.request.Request(url, data=req_data, headers=headers)
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        hits = res.get('hits', {}).get('hits', [])
        datajud_txt += f"Datajud hits: {len(hits)}\n"
        for hit in hits:
            movs = hit['_source'].get('movimentos', [])
            movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
            for m in movs_sorted[:5]:
                datajud_txt += f" • {m.get('dataHora')} — {m.get('nome')}\n"
except Exception as e:
    datajud_txt += f"Erro Datajud: {e}\n"

# 2. Raspagem ao vivo do Portal TJRJ via Playwright
tjrj_txt = ""
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        page = ctx.new_page()
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
        time.sleep(3)
        
        frame = page.frame_locator("iframe#mainframe")
        frame.locator("input[name='numeroProcesso']").fill(proc_num)
        time.sleep(1)
        frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
        time.sleep(5)
        
        frame.locator("button:has-text('Todos Os Movimentos')").first.click()
        time.sleep(4)
        
        real_frame = page.query_selector("iframe#mainframe").content_frame()
        tjrj_txt = real_frame.inner_text("body")
        browser.close()
except Exception as e:
    tjrj_txt = f"Erro Playwright TJRJ: {e}"

full_res = f"=== CONSULTA EM TEMPO REAL DATAJUD + TJRJ (29/07/2026 13h22) ===\n\n--- DATAJUD ---\n{datajud_txt}\n\n--- TJRJ PORTAL ---\n{tjrj_txt[:3500]}\n"

with open(target_file, "w", encoding="utf-8") as f:
    f.write(full_res)

print("Consulta online concluída!")
