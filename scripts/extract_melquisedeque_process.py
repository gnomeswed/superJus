# -*- coding: utf-8 -*-
import json
import urllib.request
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

num_processo = "0807644-58.2025.8.19.0202"
clean_num = "08076445820258190202"
api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

target_dir = r"c:\Projetos\superJus\Clientes\Melquisedeque\processos\0807644-58.2025.8.19.0202"
os.makedirs(target_dir, exist_ok=True)

print(f"=== EXTRAÇÃO TOTAL: PROCESSO {num_processo} — MELQUISEDEQUE RODRIGUES DOS SANTOS ===")

# 1. CONSULTA DATAJUD TJRJ COM O NÚMERO EXATO
print("1. Consultando DataJud TJRJ pelo número exato...")
url_datajud = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
headers_dj = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}
query_dj = {
    "query": {
        "match": {
            "numeroProcesso": clean_num
        }
    },
    "size": 10
}

datajud_data = None
try:
    req = urllib.request.Request(url_datajud, data=json.dumps(query_dj).encode("utf-8"), headers=headers_dj)
    with urllib.request.urlopen(req, timeout=15) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        hits = res.get("hits", {}).get("hits", [])
        print(f"   • Hits no DataJud: {len(hits)}")
        if hits:
            datajud_data = hits[0]["_source"]
            with open(os.path.join(target_dir, "datajud_raw.json"), "w", encoding="utf-8") as f:
                json.dump(datajud_data, f, ensure_ascii=False, indent=2)
except Exception as e:
    print(f"   ❌ Erro DataJud: {e}")

# 2. EXTRAÇÃO DETALHADA VIA PLAYWRIGHT NO PJe
print("\n2. Extraindo detalhes integrais e movimentações no PJe TJRJ...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = context.new_page()

    url_pje = "https://tjrj.pje.jus.br/pje/ConsultaPublica/listView.seam"
    try:
        page.goto(url_pje, wait_until="domcontentloaded", timeout=25000)
        time.sleep(2)

        # Preencher número do processo
        page.fill("input[id*='numSequencial']", "0807644")
        page.fill("input[id*='numDigitoVerificador']", "58")
        page.fill("input[id*='ano']", "2025")
        page.fill("input[id*='ramoJustica']", "8")
        page.fill("input[id*='respectivoTribunal']", "19")
        page.fill("input[id*='orgaoJurisdicional']", "0202")
        time.sleep(1)

        btn = page.query_selector("input[id*='search'], button[id*='search'], input[value*='Pesquisar'], button:has-text('Pesquisar')")
        if btn:
            btn.click()
            time.sleep(5)

            # Clicar no link de detalhes do processo
            detail_link = page.query_selector("a:has-text('VER DETALHES DO PROCESSO'), a:has-text('0807644'), a[title*='detalhe'], a[onclick*='detalhe']")
            if detail_link:
                print("   • Abrindo página de detalhes...")
                with context.expect_page() as new_page_info:
                    detail_link.click()
                detail_page = new_page_info.value
                detail_page.wait_for_load_state("domcontentloaded")
                time.sleep(5)

                det_text = detail_page.inner_text("body")
                det_html = detail_page.content()
                ss_det = os.path.join(target_dir, "pje_detalhes_processo.png")
                detail_page.screenshot(path=ss_det, full_page=True)

                with open(os.path.join(target_dir, "detalhes_pje_completo.txt"), "w", encoding="utf-8") as f:
                    f.write(det_text)
                with open(os.path.join(target_dir, "detalhes_pje_completo.html"), "w", encoding="utf-8") as f:
                    f.write(det_html)

                print(f"   ✅ Detalhes do processo extraídos com sucesso! ({len(det_text)} caracteres)")
            else:
                # Se não abriu popup, salvar texto da página atual
                cur_text = page.inner_text("body")
                with open(os.path.join(target_dir, "detalhes_pje_listview.txt"), "w", encoding="utf-8") as f:
                    f.write(cur_text)
                print("   • Salvo texto da lista de resultados.")
    except Exception as e:
        print(f"   ❌ Erro ao extrair PJe: {e}")

    browser.close()

print("\n=== EXTRAÇÃO CONCLUÍDA ===")
