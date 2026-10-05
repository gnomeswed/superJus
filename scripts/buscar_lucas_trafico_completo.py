# -*- coding: utf-8 -*-
"""
Varredura Profunda: Processo de Tráfico de Drogas (2018-2022 / Niterói / TJRJ) - Lucas de Souza Freitas
"""
import os
import sys
import time
import json
import urllib.request
import urllib.parse

sys.stdout.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

from playwright.sync_api import sync_playwright

OUT_DIR = r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_busca_trafico_2019"
os.makedirs(OUT_DIR, exist_ok=True)

NOME = "Lucas de Souza Freitas"
DATAJUD_KEY = "APIKey cENkOWRVTUJJT2JMN3V3WWtkM046VTNsTnhvTllTM21kR05kY3pSS3pWZw=="

print("==========================================================================")
print("=== 1. BUSCA DATAJUD CNJ TJRJ (POR NOME EXATO E VARIANTES) ===")
print("==========================================================================", flush=True)

try:
    dj_headers = {'Authorization': DATAJUD_KEY, 'Content-Type': 'application/json'}
    url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
    
    payload = {
        "query": {
            "bool": {
                "must": [
                    {"match_phrase": {"partes.nome": NOME}}
                ]
            }
        },
        "size": 50
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=dj_headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        hits = res.get('hits', {}).get('hits', [])
        print(f"Total de registros encontrados no DataJud TJRJ para '{NOME}': {len(hits)}", flush=True)
        with open(os.path.join(OUT_DIR, "datajud_todos_processos_lucas.json"), "w", encoding="utf-8") as f:
            json.dump(res, f, indent=2, ensure_ascii=False)
            
        for idx, h in enumerate(hits, 1):
            src = h['_source']
            num = src.get('numeroProcesso')
            classe = src.get('classe', {}).get('nome')
            orgao = src.get('orgaoJulgador', {}).get('nome')
            assuntos = [a.get('nome') for a in src.get('assuntos', [])]
            dt = src.get('dataHoraUltimaAtualizacao')
            print(f"  [{idx}] Nº: {num} | Órgão: {orgao} | Classe: {classe} | Assuntos: {assuntos} | Modif: {dt}", flush=True)

except Exception as e:
    print(f"Erro DataJud: {e}", flush=True)

print("\n==========================================================================")
print("=== 2. TJRJ CONSULTA POR NOME (1ª INSTÂNCIA / NITERÓI / 2018-2022) ===")
print("==========================================================================", flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1280, "height": 800}, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = ctx.new_page()

    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
    time.sleep(4)
    frame = page.frame_locator("iframe#mainframe")

    frame.locator("#nav-porNome").click()
    time.sleep(2)

    frame.locator("#porNome #filtroOrigem1").fill("1ª Instância")
    time.sleep(1)
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    time.sleep(1)

    frame.locator("#porNome #filtroComarca1").fill("Niterói")
    time.sleep(1)
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    time.sleep(1)

    frame.locator("#porNome #filtroCompetencia1").fill("Criminal")
    time.sleep(1)
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    time.sleep(1)

    frame.locator("#porNome #nomeParte").fill("Lucas de Souza Freitas")
    time.sleep(1)

    frame.locator("#porNome #anoInicial1").fill("2018")
    frame.locator("#porNome #anoFinal1").fill("2022")
    time.sleep(1)

    try:
        chk = frame.locator("#porNome #procEmAndamento2").first
        if chk.is_checked():
            chk.uncheck()
            print("Desmarcado 'Somente em andamento'")
    except Exception as e:
        print("Aviso checkbox:", e)

    time.sleep(1)
    frame.locator("#porNome button").first.click()
    print("Aguardando resposta do portal TJRJ...")
    time.sleep(12)

    real_frame = page.query_selector("iframe#mainframe").content_frame()
    body_txt = real_frame.inner_text("body")
    with open(os.path.join(OUT_DIR, "tjrj_resultado_niteroi_2018_2022.txt"), "w", encoding="utf-8") as f:
        f.write(body_txt)
    page.screenshot(path=os.path.join(OUT_DIR, "tjrj_niteroi_2018_2022.png"), full_page=True)

    print("\n--- Resultado no TJRJ (Niterói 2018-2022): ---")
    for line in [l.strip() for l in body_txt.split('\n') if l.strip()][:35]:
        print(f"  {line}")

    # Também testar busca ampla sem filtro de comarca (todo o Estado do RJ, anos 2018 a 2022)
    print("\n==========================================================================")
    print("=== 3. TJRJ CONSULTA POR NOME (TODO O ESTADO DO RJ / 2018-2022) ===")
    print("==========================================================================", flush=True)
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
    time.sleep(4)
    frame = page.frame_locator("iframe#mainframe")

    frame.locator("#nav-porNome").click()
    time.sleep(2)

    frame.locator("#porNome #filtroOrigem1").fill("1ª Instância")
    time.sleep(1)
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    time.sleep(1)

    frame.locator("#porNome #nomeParte").fill("Lucas de Souza Freitas")
    time.sleep(1)

    frame.locator("#porNome #anoInicial1").fill("2018")
    frame.locator("#porNome #anoFinal1").fill("2022")
    time.sleep(1)

    try:
        chk = frame.locator("#porNome #procEmAndamento2").first
        if chk.is_checked():
            chk.uncheck()
    except:
        pass

    time.sleep(1)
    frame.locator("#porNome button").first.click()
    time.sleep(12)

    real_frame2 = page.query_selector("iframe#mainframe").content_frame()
    body_txt2 = real_frame2.inner_text("body")
    with open(os.path.join(OUT_DIR, "tjrj_resultado_todo_rj_2018_2022.txt"), "w", encoding="utf-8") as f:
        f.write(body_txt2)

    print("\n--- Resultado no TJRJ (Todo RJ 2018-2022): ---")
    for line in [l.strip() for l in body_txt2.split('\n') if l.strip()][:35]:
        print(f"  {line}")

    browser.close()

print("\n==========================================================================")
print("=== BUSCA CONCLUÍDA ===")
print("==========================================================================", flush=True)
