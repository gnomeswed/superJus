# -*- coding: utf-8 -*-
import time
import os
import json
import requests
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

CLIENT_DIR = r"c:\Projetos\superJus\Clientes\Daniel_Ferreira_Lima"
DOCS_DIR = os.path.join(CLIENT_DIR, "03_Documentos_do_Processo")
MOVS_DIR = os.path.join(CLIENT_DIR, "02_Movimentacoes")

# 1. Salvar dados do RESE da 2ª Instância (DataJud)
DATAJUD_KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {"Authorization": DATAJUD_KEY, "Content-Type": "application/json"}
BASE_TJRJ = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"

print("1. Buscando 2ª Instância (RESE) no DataJud...")
try:
    r = requests.post(BASE_TJRJ, headers=HEADERS, json={
        "query": {"match": {"numeroProcesso": "00043013320188190073"}},
        "size": 10
    }, timeout=30)
    if r.status_code == 200:
        hits = r.json().get("hits", {}).get("hits", [])
        for idx, h in enumerate(hits):
            src = h["_source"]
            orgao = src.get("orgaoJulgador", {}).get("nome", "")
            classe = src.get("classe", {}).get("nome", "")
            if "RECURSO" in classe.upper() or "DESA" in orgao.upper():
                print(f"  Encontrado RESE: {orgao} | {classe}")
                with open(os.path.join(MOVS_DIR, "datajud_2a_instancia_rese.json"), "w", encoding="utf-8") as f:
                    json.dump(src, f, indent=2, ensure_ascii=False)
                
                movs = sorted(src.get("movimentos", []), key=lambda m: m.get("dataHora", ""), reverse=True)
                with open(os.path.join(MOVS_DIR, "movimentacoes_2a_instancia_rese.md"), "w", encoding="utf-8") as f:
                    f.write(f"# 2ª Instância TJRJ — Recurso em Sentido Estrito — 0004301-33.2018.8.19.0073\n\n")
                    f.write(f"- **Relator / Gabinete:** {orgao}\n")
                    f.write(f"- **Classe:** {classe}\n")
                    f.write(f"- **Resultado:** Acórdão de Não-Provimento (confirmou pronúncia)\n\n")
                    f.write("| Data | Código | Movimento |\n| :--- | :--- | :--- |\n")
                    for m in movs:
                        f.write(f"| {m.get('dataHora','')[:19]} | {m.get('codigo','')} | {m.get('nome','')} |\n")
                print("  RESE salvo com sucesso!")
except Exception as e:
    print(f"Erro ao salvar RESE: {e}")

# 2. Raspagem no Portal Público do TJRJ via Playwright
print("\n2. Conectando ao Portal do TJRJ via Playwright...")
proc_num = "0004301-33.2018.8.19.0073"

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1280, "height": 900})
        page = ctx.new_page()
        
        print("  Acessando Consulta Processual do TJRJ...")
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
        time.sleep(3)
        
        # Preencher processo no iframe
        frame = page.frame_locator("iframe#mainframe")
        frame.locator("input[name='numeroProcesso']").fill(proc_num)
        time.sleep(1)
        frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
        time.sleep(6)
        
        real_frame = page.query_selector("iframe#mainframe").content_frame()
        tjrj_txt = real_frame.inner_text("body")
        tjrj_html = real_frame.content()
        
        out_txt = os.path.join(DOCS_DIR, "espelho_integral_tjrj_portal_0004301.txt")
        out_html = os.path.join(DOCS_DIR, "espelho_integral_tjrj_portal_0004301.html")
        
        with open(out_txt, "w", encoding="utf-8") as f:
            f.write(tjrj_txt)
        with open(out_html, "w", encoding="utf-8") as f:
            f.write(tjrj_html)
            
        print(f"  [OK] Espelho e despachos do TJRJ salvos em: {out_txt}")
        print(f"  Visualização prévia do conteúdo capturado:\n{tjrj_txt[:800]}")
        
        # 3. Busca por outros processos no TJRJ em nome de Daniel Ferreira Lima
        print("\n3. Verificando outros processos por nome no TJRJ...")
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/conspublica", timeout=30000)
        time.sleep(3)
        page.click("text=Por Nome")
        time.sleep(2)
        
        inp = page.query_selector("input[placeholder*='nome da parte'], input[name*='nome da parte']")
        if inp:
            inp.fill("DANIEL FERREIRA LIMA")
            time.sleep(1)
            chk = page.query_selector("input[name='procEmAndamento']")
            if chk and chk.is_checked():
                chk.uncheck()
            btn = page.query_selector("button:has-text('Pesquisar')")
            if btn:
                btn.click()
                time.sleep(8)
                out_name_txt = os.path.join(DOCS_DIR, "pesquisa_por_nome_daniel_ferreira_lima_tjrj.txt")
                with open(out_name_txt, "w", encoding="utf-8") as f:
                    f.write(page.inner_text("body"))
                print(f"  [OK] Varredura nominal salva em: {out_name_txt}")
                
        browser.close()
except Exception as e:
    print(f"Erro na raspagem Playwright: {e}")

print("\n=== DOWNLOAD E EXTRAÇÃO DE DOCUMENTOS FINALIZADOS ===")
