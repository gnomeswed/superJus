# -*- coding: utf-8 -*-
"""
Extração Completa dos 2 Processos de 2019 de Lucas de Souza Freitas:
1. 0024951-89.2019.8.19.0001 (1ª Vara Criminal de Niterói)
2. 0034340-95.2019.8.19.0002 (1ª Vara Criminal de Niterói)
"""
import os
import sys
import time
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

from playwright.sync_api import sync_playwright

API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {'Authorization': f"APIKey {API_KEY}", 'Content-Type': 'application/json'}

OUT_DIR = r"C:\Projetos\superJus\Clientes\Lucas_Freitas\05_Processos_Anteriores\Processos_2019"
os.makedirs(OUT_DIR, exist_ok=True)

PROCS = [
    ("0024951-89.2019.8.19.0001", "00249518920198190001", "Proc_0024951_2019"),
    ("0034340-95.2019.8.19.0002", "00343409520198190002", "Proc_0034340_2019")
]

results = {}

# 1. Consulta DataJud para ambos
print("=== 1. CONSULTA DATAJUD CNJ ===", flush=True)
for cnj_fmt, cnj_clean, label in PROCS:
    print(f"Buscando no DataJud: {cnj_fmt}...", flush=True)
    try:
        url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
        payload = {"query": {"match": {"numeroProcesso": cnj_clean}}, "size": 10}
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            hits = data.get('hits', {}).get('hits', [])
            print(f"  Hits DataJud para {cnj_fmt}: {len(hits)}", flush=True)
            with open(os.path.join(OUT_DIR, f"datajud_{label}.json"), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            results[f"datajud_{label}"] = data
    except Exception as e:
        print(f"  Erro DataJud {cnj_fmt}: {e}", flush=True)

# 2. Consulta TJRJ Playwright (Integral / Todos os Movimentos)
print("\n=== 2. CONSULTA AO VIVO TJRJ PLAYWRIGHT ===", flush=True)
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1366, "height": 900}, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = ctx.new_page()

    for cnj_fmt, cnj_clean, label in PROCS:
        print(f"\n{'-'*60}\nExtraindo TJRJ: {cnj_fmt} ({label})\n{'-'*60}", flush=True)
        try:
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
            time.sleep(4)
            iframe_el = page.wait_for_selector("iframe#mainframe", timeout=25000)
            fr = iframe_el.content_frame()

            inp = fr.wait_for_selector("input[name='numeroProcesso']", timeout=15000)
            inp.fill(cnj_fmt)
            time.sleep(1)

            btns = fr.query_selector_all("button")
            btn_pesq = next((b for b in btns if any(w in b.inner_text().lower() for w in ["pesquisar", "buscar", "consultar"])), btns[0] if btns else None)
            if btn_pesq:
                btn_pesq.click()
            time.sleep(7)

            # Se houver tabela de instâncias/links
            links = fr.query_selector_all("table a, .table a, tbody tr td a")
            if len(links) > 0:
                print(f"Links encontrados na tabela: {len(links)}", flush=True)
                for l in links:
                    if cnj_fmt in l.inner_text() or label in l.inner_text():
                        l.click()
                        time.sleep(6)
                        break

            # Clicar em Todos os Movimentos
            try:
                btn_all = fr.query_selector("button:has-text('Todos Os Movimentos'), a:has-text('Todos Os Movimentos')")
                if btn_all:
                    btn_all.click()
                    time.sleep(5)
            except Exception:
                pass

            body = fr.inner_text("body")
            html = fr.evaluate("document.documentElement.outerHTML")

            with open(os.path.join(OUT_DIR, f"{label}_espelho.txt"), "w", encoding="utf-8") as f:
                f.write(body)
            with open(os.path.join(OUT_DIR, f"{label}_espelho.html"), "w", encoding="utf-8") as f:
                f.write(html)
            page.screenshot(path=os.path.join(OUT_DIR, f"{label}_screenshot.png"), full_page=True)

            results[label] = body
            print(f"[OK] {label} extraído! Total chars: {len(body)}", flush=True)
            print("--- Primeiras Linhas ---")
            for line in [l.strip() for l in body.split('\n') if l.strip()][:30]:
                print(f"  {line}")

        except Exception as e:
            print(f"Erro Playwright {cnj_fmt}: {e}", flush=True)
            results[label] = f"ERRO: {e}"

    browser.close()

with open(os.path.join(OUT_DIR, "resultado_consolidado_ambos.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\n==========================================================================")
print(f"=== EXTRAÇÃO CONCLUÍDA! Arquivos salvos em: {OUT_DIR} ===")
print("==========================================================================", flush=True)
