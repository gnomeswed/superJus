# -*- coding: utf-8 -*-
"""
Busca por Processo de Tráfico de Drogas (2019 / Niterói) - Lucas de Souza Freitas
Fontes: TJRJ Consulta Pública (Por Nome), DataJud CNJ e Dossiê/FAC do Caso
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

print("==========================================================================")
print(f"=== BUSCA ESPECÍFICA: PROCESSO DE TRÁFICO / 2019 EM NITERÓI ===")
print("==========================================================================\n", flush=True)

# 1. DATAJUD API TJRJ - BUSCA POR NOME AMPLA
print("[1] Buscando no DataJud TJRJ...", flush=True)
try:
    auth_header = __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization']
    dj_headers = {'Authorization': auth_header, 'Content-Type': 'application/json'}
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
        print(f"Total de processos encontrados no DataJud para '{NOME}': {len(hits)}", flush=True)
        with open(os.path.join(OUT_DIR, "datajud_busca_nome.json"), "w", encoding="utf-8") as f:
            json.dump(res, f, indent=2, ensure_ascii=False)
            
        for idx, h in enumerate(hits, 1):
            src = h['_source']
            num = src.get('numeroProcesso')
            classe = src.get('classe', {}).get('nome')
            orgao = src.get('orgaoJulgador', {}).get('nome')
            assuntos = [a.get('nome') for a in src.get('assuntos', [])]
            dt = src.get('dataHoraUltimaAtualizacao')
            print(f"  [{idx}] Processo: {num} | Órgão: {orgao} | Classe: {classe} | Assuntos: {assuntos} | Modif: {dt}", flush=True)

except Exception as e:
    print(f"Erro DataJud: {e}", flush=True)

# 2. TJRJ CONSULTA POR NOME VIA PLAYWRIGHT
print("\n[2] Buscando no Portal do TJRJ (Por Nome / Todos os anos)...", flush=True)
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-dev-shm-usage"]
    )
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 900},
        locale="pt-BR"
    )
    ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    page = ctx.new_page()

    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
    time.sleep(4)
    iframe_el = page.wait_for_selector("iframe#mainframe", timeout=25000)
    fr = iframe_el.content_frame()

    # Clicar em "Por Nome"
    fr.evaluate("""() => {
        const alvo = Array.from(document.querySelectorAll('label, span, a, div, button'))
          .find(c => (c.textContent || '').trim().toLowerCase() === 'por nome');
        if (alvo) alvo.click();
    }""")
    time.sleep(2)

    # Preencher nome
    fr.evaluate(f"""() => {{
        const el = document.getElementById('nomeParte');
        if(el) {{
            el.value = '{NOME}';
            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            el.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
    }}""")
    time.sleep(1)

    # Anos 2018 a 2026
    fr.evaluate("""() => {
        const a1 = document.getElementById('anoInicial1');
        const a2 = document.getElementById('anoFinal1');
        if(a1) { a1.value = '2018'; a1.dispatchEvent(new Event('input', { bubbles: true })); a1.dispatchEvent(new Event('change', { bubbles: true })); }
        if(a2) { a2.value = '2026'; a2.dispatchEvent(new Event('input', { bubbles: true })); a2.dispatchEvent(new Event('change', { bubbles: true })); }
    }""")
    time.sleep(1)

    # Clicar em Pesquisar
    fr.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button'))
          .find(b => b.offsetWidth > 0 && b.textContent.toLowerCase().includes('pesquisar'));
        if (btn) btn.click();
    }""")
    time.sleep(10)

    body = fr.inner_text("body")
    with open(os.path.join(OUT_DIR, "tjrj_busca_nome_2018_2026.txt"), "w", encoding="utf-8") as f:
        f.write(body)
    with open(os.path.join(OUT_DIR, "tjrj_busca_nome_2018_2026.html"), "w", encoding="utf-8") as f:
        f.write(fr.evaluate("document.documentElement.outerHTML"))
    page.screenshot(path=os.path.join(OUT_DIR, "tjrj_busca_nome.png"), full_page=True)

    print("\n--- Resultado da busca por nome no TJRJ (2018-2026) ---", flush=True)
    for line in [l.strip() for l in body.split('\n') if l.strip()][:35]:
        print(f"  {line}", flush=True)

    browser.close()

print("\n==========================================================================")
print(f"=== FIM DA BUSCA. Evidências em: {OUT_DIR} ===")
print("==========================================================================", flush=True)
