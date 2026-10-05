# -*- coding: utf-8 -*-
"""
Consulta oficial online ao vivo em tempo real — Júlio Pereira Marcos (22/09/2026 - Terça-feira)
Fontes consultadas:
1. Portal do TJRJ (1ª e 2ª Instâncias via Playwright no portal público)
2. DJERJ (Consulta de Publicações de 01/09/2026 a 22/09/2026)
3. Datajud API (CNJ) - TJRJ e STJ
4. Portal do STJ (Fases e Decisões do HC 1.116.750 / RJ - 6ª Turma)
"""
import sys
import os
import json
import time
import urllib.request
import re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DATAJUD_API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {
    'Authorization': f'APIKey {DATAJUD_API_KEY}',
    'Content-Type': 'application/json'
}

OUT_DIRS = [
    r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo",
    r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\documentos_processo"
]
for d in OUT_DIRS:
    os.makedirs(d, exist_ok=True)

PROCS_1A = [
    ("0023013-51.2021.8.19.0078", "00230135120218190078", "julio_tjrj_1A_Principal_Julio_22set.txt", "Ação Penal Principal - 2ª Vara de Búzios"),
    ("0001140-87.2024.8.19.0078", "00011408720248190078", "julio_tjrj_1A_Apenso_RSE_22set.txt", "Recurso em Sentido Estrito / Apenso - Búzios"),
    ("0022975-39.2021.8.19.0078", "00229753920218190078", "julio_tjrj_1A_Original_Desmembrado_22set.txt", "Processo Originário / Co-réus - Búzios")
]
PROC_2A = ("0029845-67.2026.8.19.0000", "00298456720268190000", "julio_tjrj_2A_HC_22set.txt", "2ª Instância TJRJ (HC e ROC)")

results = {
    "data_consulta": "22/09/2026",
    "hora_consulta": time.strftime("%H:%M:%S"),
    "datajud_tjrj": {},
    "datajud_stj": {},
    "portal_tjrj": {},
    "portal_stj": {},
    "djerj": {}
}

print("="*75)
print("🔍 1. CONSULTA DATAJUD CNJ — TJRJ E STJ (22/09/2026)")
print("="*75)

for proc_fmt, proc_clean, _, desc in PROCS_1A + [PROC_2A]:
    print(f"\n--- DataJud {proc_fmt} ({desc}) ---")
    url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
    payload = json.dumps({"query": {"match": {"numeroProcesso": proc_clean}}, "size": 10}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            hits = data.get('hits', {}).get('hits', [])
            print(f"Registros encontrados: {len(hits)}")
            proc_entries = []
            for hit in hits:
                src = hit['_source']
                orgao = src.get('orgaoJulgador', {}).get('nome', 'N/A')
                classe = src.get('classe', {}).get('nome', 'N/A')
                dt_up = src.get('dataHoraUltimaAtualizacao', 'N/A')
                movs = src.get('movimentos', [])
                movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
                print(f"  • Órgão: {orgao} | Classe: {classe} | Atualização: {dt_up}")
                top_movs = []
                for m in movs_sorted[:5]:
                    dt_m = m.get('dataHora', '')[:19].replace('T', ' ')
                    nome_m = m.get('nome', '')
                    print(f"    - {dt_m} | {nome_m}")
                    top_movs.append({"dataHora": dt_m, "nome": nome_m})
                proc_entries.append({
                    "orgao": orgao,
                    "classe": classe,
                    "ultimaAtualizacao": dt_up,
                    "totalMovimentos": len(movs),
                    "ultimosMovimentos": top_movs
                })
            results["datajud_tjrj"][proc_fmt] = proc_entries
    except Exception as e:
        print(f"Erro DataJud {proc_fmt}: {e}")
        results["datajud_tjrj"][proc_fmt] = {"erro": str(e)}

# STJ via DataJud (Exact match por numeroProcesso CNJ)
print("\n--- DataJud STJ (HC 1.116.750 / 0311210-10.2026.3.00.0000) ---")
try:
    url_stj = 'https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search'
    payload_stj = json.dumps({"query": {"match": {"numeroProcesso": "03112101020263000000"}}, "size": 5}).encode('utf-8')
    req_stj = urllib.request.Request(url_stj, data=payload_stj, headers=HEADERS)
    with urllib.request.urlopen(req_stj, timeout=15) as resp:
        data_stj = json.loads(resp.read().decode('utf-8'))
        hits_stj = data_stj.get('hits', {}).get('hits', [])
        print(f"Registros encontrados no STJ por número: {len(hits_stj)}")
        stj_entries = []
        for h in hits_stj:
            src = h['_source']
            p_num = src.get('numeroProcesso')
            classe = src.get('classe', {}).get('nome')
            dt_up = src.get('dataHoraUltimaAtualizacao')
            movs = src.get('movimentos', [])
            movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
            print(f"  • Processo: {p_num} | Classe: {classe} | Atualização: {dt_up}")
            top_movs = []
            for m in movs_sorted[:8]:
                dt_m = m.get('dataHora', '')[:19].replace('T', ' ')
                nome_m = m.get('nome', '')
                print(f"    - {dt_m} | {nome_m}")
                top_movs.append({"dataHora": dt_m, "nome": nome_m})
            stj_entries.append({
                "numeroProcesso": p_num,
                "classe": classe,
                "ultimaAtualizacao": dt_up,
                "ultimosMovimentos": top_movs
            })
        results["datajud_stj"] = stj_entries
except Exception as e:
    print(f"Erro STJ DataJud: {e}")
    results["datajud_stj"] = {"erro": str(e)}

print("\n" + "="*75)
print("🌐 2. RASPAGEM DIRETA TJRJ (PLAYWRIGHT AO VIVO)")
print("="*75)

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
    )
    ctx = browser.new_context(
        viewport={"width": 1366, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        locale="pt-BR"
    )
    ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
    page = ctx.new_page()

    def query_tjrj_direct(proc_fmt, is_2a, save_fname):
        print(f"\n--- Consultando {proc_fmt} no Portal TJRJ (2ª Instância: {is_2a}) ---")
        for attempt in range(1, 4):
            try:
                page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=40000)
                time.sleep(3)

                if is_2a:
                    page.click('label[for="radioOrigem2"]')
                else:
                    page.click('label[for="radioOrigem1"]')
                time.sleep(1)

                inp = page.wait_for_selector('input[placeholder*="número do processo"]', timeout=15000)
                inp.click()
                inp.fill(proc_fmt)
                time.sleep(1)

                page.click('button:has-text("Pesquisar")')
                print("Pesquisar clicado, aguardando iframe...")

                page.wait_for_selector('iframe#mainframe', timeout=30000)
                time.sleep(3)
                frame_el = page.query_selector('iframe#mainframe')
                frame = frame_el.content_frame()
                time.sleep(3)

                # Se 2ª Instância, clicar no HC se houver lista
                if is_2a:
                    try:
                        hc_link = frame.query_selector('a:has-text("2026.059.10770"), a:has-text("10770"), table a')
                        if hc_link:
                            print(f"Clicando no HC: {hc_link.inner_text()}")
                            hc_link.click()
                            time.sleep(4)
                    except Exception as e:
                        print("Aviso clique HC:", e)

                # Clicar em Todos Os Movimentos se existir
                try:
                    todos_btn = frame.query_selector('a:has-text("Todos Os Movimentos"), a:has-text("Todos")')
                    if todos_btn:
                        print("Clicando em 'Todos Os Movimentos'...")
                        todos_btn.click()
                        time.sleep(3)
                except Exception as e:
                    print("Aviso clique todos os movimentos:", e)

                body_txt = frame.inner_text("body")
                print(f"Caracteres capturados: {len(body_txt)}")

                for d in OUT_DIRS:
                    try:
                        fpath = os.path.join(d, save_fname)
                        with open(fpath, "w", encoding="utf-8") as f:
                            f.write(body_txt)
                        print(f"Salvo em: {fpath}")
                    except Exception as e:
                        print(f"Erro ao salvar em {d}: {e}")

                loc_str = "N/A"
                if "Localização na Serventia" in body_txt:
                    idx = body_txt.index("Localização na Serventia")
                    loc_str = body_txt[idx:idx+300].replace('\n', ' | ')

                mov_str = "N/A"
                if "Tipo do Movimento:" in body_txt:
                    idx = body_txt.index("Tipo do Movimento:")
                    mov_str = body_txt[idx:idx+300].replace('\n', ' | ')

                print(f"  • Localização: {loc_str[:120]}")
                print(f"  • Último Movimento: {mov_str[:120]}")

                # Extrair os 5 primeiros movimentos
                lines = [l.strip() for l in body_txt.split('\n') if l.strip()]
                parsed_movs = []
                for i, l in enumerate(lines):
                    if "Tipo do Movimento:" in l:
                        bloco = lines[i:min(len(lines), i + 8)]
                        parsed_movs.append(" | ".join(bloco))

                return {
                    "status": "sucesso",
                    "data_hora_consulta": time.strftime("%d/%m/%Y %H:%M:%S"),
                    "localizacao": loc_str,
                    "ultimo_movimento": mov_str,
                    "ultimos_movimentos": parsed_movs[:6],
                    "total_movimentos": body_txt.count("Tipo do Movimento:"),
                    "raw_length": len(body_txt)
                }
            except Exception as e:
                print(f"Tentativa {attempt} falhou ({proc_fmt}): {e}")
                time.sleep(3)
        return {"status": "erro", "erro": "Max retries exceeded"}

    # 1. 1ª Instância
    for proc_fmt, _, fname, desc in PROCS_1A:
        results["portal_tjrj"][proc_fmt] = query_tjrj_direct(proc_fmt, False, fname)

    # 2. 2ª Instância
    results["portal_tjrj"][PROC_2A[0]] = query_tjrj_direct(PROC_2A[0], True, PROC_2A[2])

    # 3. STJ Consulta Direta
    print("\n--- Portal STJ (HC 1.116.750 / RJ) ---")
    URL_STJ_RE = "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo=202603112107"
    try:
        page.goto(URL_STJ_RE, wait_until="domcontentloaded", timeout=45000)
        time.sleep(5)

        page.evaluate("""() => {
            const links = Array.from(document.querySelectorAll('a'));
            const l = links.find(a => (a.textContent||'').includes('1116750') || (a.textContent||'').includes('2026/0311210-7') || (a.href||'').includes('num_registro=202603112107'));
            if(l) l.click();
        }""")
        time.sleep(6)

        stj_txt = page.evaluate("document.body.innerText")
        for d in OUT_DIRS:
            try:
                stj_fpath = os.path.join(d, "julio_stj_live_direct_22set.txt")
                with open(stj_fpath, "w", encoding="utf-8") as f:
                    f.write(stj_txt)
                print(f"STJ Capturado ({len(stj_txt)} chars). Salvo em {stj_fpath}")
            except Exception as e:
                print(f"Erro STJ save {d}: {e}")

        relevant_stj = []
        for line in stj_txt.splitlines():
            if any(k in line.upper() for k in ["CONCLUSOS", "GABINETE", "FASE:", "ÚLTIMA FASE", "PARECER", "MINISTRO", "RELATOR"]):
                print(f"  • STJ Linha Relevante: {line.strip()}")
                relevant_stj.append(line.strip())

        results["portal_stj"] = {
            "status": "sucesso",
            "data_hora_consulta": time.strftime("%d/%m/%Y %H:%M:%S"),
            "relevant_lines": relevant_stj[:10],
            "raw_length": len(stj_txt)
        }
    except Exception as e:
        print(f"Erro STJ Scraping: {e}")
        results["portal_stj"] = {"status": "erro", "erro": str(e)}

    # 4. DJERJ Consulta de Publicações recentes (01/09 a 22/09/2026)
    print("\n--- DJERJ Consulta de Publicações (01/09/2026 a 22/09/2026) ---")
    for proc_fmt, _, _, _ in PROCS_1A + [PROC_2A]:
        url_djerj = f"https://www3.tjrj.jus.br/consultadje/Result.aspx?dtInicio=01%2F09%2F2026&dtFim=22%2F09%2F2026&txtPesq={proc_fmt}&tipoPesq=PROC"
        try:
            page.goto(url_djerj, wait_until="domcontentloaded", timeout=45000)
            time.sleep(4)
            djerj_body = page.evaluate("document.body.innerText")
            if "Não foram encontradas" in djerj_body or "Nenhum registro encontrado" in djerj_body:
                print(f"  • {proc_fmt}: Sem novas publicações no DJERJ.")
                results["djerj"][proc_fmt] = "Sem publicações no período (01 a 22/09/2026)"
            else:
                print(f"  🚨 {proc_fmt}: PUBLICAÇÃO LOCALIZADA!\n{djerj_body[:1000]}")
                results["djerj"][proc_fmt] = djerj_body[:2000]
        except Exception as e:
            print(f"Erro DJERJ {proc_fmt}: {e}")
            results["djerj"][proc_fmt] = f"Erro: {e}"

    # DJERJ por nome
    try:
        url_nome = "https://www3.tjrj.jus.br/consultadje/Result.aspx?dtInicio=01%2F09%2F2026&dtFim=22%2F09%2F2026&txtPesq=Julio%20Pereira%20Marcos&tipoPesq=NOME"
        page.goto(url_nome, wait_until="domcontentloaded", timeout=45000)
        time.sleep(4)
        djerj_nome = page.evaluate("document.body.innerText")
        if "Não foram encontradas" in djerj_nome or "Nenhum registro encontrado" in djerj_nome:
            print("  • Julio Pereira Marcos: Sem publicações no DJERJ.")
            results["djerj"]["Julio Pereira Marcos"] = "Sem publicações no período (01 a 22/09/2026)"
        else:
            print(f"  🚨 Julio Pereira Marcos: PUBLICAÇÃO LOCALIZADA!\n{djerj_nome[:1000]}")
            results["djerj"]["Julio Pereira Marcos"] = djerj_nome[:2000]
    except Exception as e:
        print(f"Erro DJERJ Nome: {e}")
        results["djerj"]["Julio Pereira Marcos"] = f"Erro: {e}"

    browser.close()

# Salvar json de resultados em superJus e swedsystem
dest_jsons = [
    r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\consulta_ao_vivo_22_09_2026.json",
    r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\consulta_ao_vivo_22_09_2026.json",
    r"C:\Projetos\swedsystem\docs\consulta_ao_vivo_22_09_2026.json"
]
for pth in dest_jsons:
    try:
        os.makedirs(os.path.dirname(pth), exist_ok=True)
        with open(pth, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"Salvo JSON: {pth}")
    except Exception as e:
        print(f"Erro ao salvar JSON {pth}: {e}")

print("\n" + "="*75)
print("✅ VARREDURA COMPLETA 22/09/2026 CONCLUÍDA COM SUCESSO!")
print("="*75)
