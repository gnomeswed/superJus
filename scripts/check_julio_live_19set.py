# -*- coding: utf-8 -*-
"""
Consulta online ao vivo e em tempo real — Júlio Pereira Marcos (19/09/2026)
Fontes consultadas:
1. Portal do TJRJ (1ª e 2ª Instâncias via Playwright direto do portal público)
2. DJERJ (Consulta de Publicações de 01/09/2026 a 19/09/2026)
3. Datajud API (CNJ) - TJRJ (1ª e 2ª Instâncias) e STJ
4. Portal do STJ (Fases e Decisões do HC 1.116.750 / RJ)
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

OUT_DIR = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(OUT_DIR, exist_ok=True)

PROCS_TJRJ = [
    ("0023013-51.2021.8.19.0078", "00230135120218190078", "Ação Penal Desmembrada - 2ª Vara de Búzios"),
    ("0001140-87.2024.8.19.0078", "00011408720248190078", "Recurso em Sentido Estrito / Apenso - Búzios"),
    ("0022975-39.2021.8.19.0078", "00229753920218190078", "Processo Originário / Co-réus - Búzios")
]
PROC_2A = "0029845-67.2026.8.19.0000"

results = {
    "data_consulta": "19/09/2026",
    "hora_consulta": time.strftime("%H:%M:%S"),
    "datajud_tjrj": {},
    "datajud_stj": {},
    "portal_tjrj": {},
    "portal_stj": {},
    "djerj": {}
}

print("="*70)
print("🔍 1. CONSULTA DATAJUD CNJ — TJRJ E STJ (19/09/2026)")
print("="*70)

for proc_fmt, proc_clean, desc in PROCS_TJRJ + [(PROC_2A, "00298456720268190000", "2ª Instância TJRJ")]:
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

print("\n" + "="*70)
print("🌐 2. RASPAGEM DIRETA TJRJ (PLAYWRIGHT AO VIVO)")
print("="*70)

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

    def query_tjrj_portal(proc_target, save_fname):
        print(f"\n--- Consultando {proc_target} no Portal TJRJ ---")
        try:
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=45000)
            time.sleep(4)
            page.wait_for_selector("iframe#mainframe", timeout=30000)
            frame_el = page.query_selector("iframe#mainframe")
            frame = frame_el.content_frame()
            time.sleep(2)

            frame.evaluate(f"""() => {{
                const inp = Array.from(document.querySelectorAll('input')).find(i => i.name==='numeroProcesso' || i.id==='numeroProcesso');
                if(inp) {{
                    inp.value = '{proc_target}';
                    inp.dispatchEvent(new Event('input', {{bubbles:true}}));
                    inp.dispatchEvent(new Event('change', {{bubbles:true}}));
                }}
            }}""")
            time.sleep(1)
            frame.evaluate("""() => {
                const btn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth>0 && (b.textContent||'').toLowerCase().includes('pesquisar'));
                if(btn) btn.click();
            }""")
            time.sleep(8)

            # Tenta expandir Todos os Movimentos se disponível
            try:
                frame.evaluate("""() => {
                    const todosBtn = Array.from(document.querySelectorAll('a, button, span')).find(el => (el.textContent||'').trim().toLowerCase() === 'todos os movimentos' || (el.textContent||'').trim().toLowerCase() === 'todos');
                    if(todosBtn) todosBtn.click();
                }""")
                time.sleep(3)
            except Exception:
                pass

            body_txt = frame.inner_text("body")
            print(f"Caracteres capturados: {len(body_txt)}")
            
            fpath = os.path.join(OUT_DIR, save_fname)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(body_txt)
            print(f"Salvo em {fpath}")

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

            return {
                "status": "sucesso",
                "data_hora_consulta": time.strftime("%d/%m/%Y %H:%M:%S"),
                "localizacao": loc_str,
                "ultimo_movimento": mov_str,
                "fpath": fpath,
                "raw": body_txt
            }
        except Exception as e:
            print(f"Erro Portal TJRJ ({proc_target}): {e}")
            return {"status": "erro", "erro": str(e)}

    # 1. Principal Julio
    results["portal_tjrj"]["0023013-51.2021.8.19.0078"] = query_tjrj_portal(
        "0023013-51.2021.8.19.0078", "julio_tjrj_1A_Principal_Julio_19set.txt"
    )

    # 2. Apenso RSE
    results["portal_tjrj"]["0001140-87.2024.8.19.0078"] = query_tjrj_portal(
        "0001140-87.2024.8.19.0078", "julio_tjrj_1A_Apenso_RSE_19set.txt"
    )

    # 3. Originário Corréus
    results["portal_tjrj"]["0022975-39.2021.8.19.0078"] = query_tjrj_portal(
        "0022975-39.2021.8.19.0078", "julio_tjrj_1A_Original_Desmembrado_19set.txt"
    )

    # 4. 2ª Instância (HC e ROC)
    print(f"\n--- Consultando {PROC_2A} no Portal TJRJ (2ª Instância) ---")
    try:
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=45000)
        time.sleep(4)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        frame = page.query_selector("iframe#mainframe").content_frame()
        time.sleep(2)

        frame.evaluate(f"""() => {{
            const inp = Array.from(document.querySelectorAll('input')).find(i => i.name==='numeroProcesso' || i.id==='numeroProcesso');
            if(inp) {{
                inp.value = '{PROC_2A}';
                inp.dispatchEvent(new Event('input', {{bubbles:true}}));
                inp.dispatchEvent(new Event('change', {{bubbles:true}}));
            }}
        }}""")
        time.sleep(1)
        frame.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth>0 && (b.textContent||'').toLowerCase().includes('pesquisar'));
            if(btn) btn.click();
        }""")
        time.sleep(8)

        table_body = frame.inner_text("body")
        hc_fpath = os.path.join(OUT_DIR, "julio_tjrj_2A_HC_19set.txt")
        with open(hc_fpath, "w", encoding="utf-8") as f:
            f.write(table_body)

        # Clica no HC 2026.059.10770
        frame.evaluate("""() => {
            const links = Array.from(document.querySelectorAll('table a, .table a, a'));
            const l = links.find(a => (a.textContent||'').includes('2026.059.10770') || (a.textContent||'').includes('10770'));
            if(l) l.click();
        }""")
        time.sleep(6)
        hc_detail = frame.inner_text("body")
        with open(hc_fpath, "w", encoding="utf-8") as f:
            f.write(hc_detail)

        results["portal_tjrj"][PROC_2A] = {
            "status": "sucesso",
            "data_hora_consulta": time.strftime("%d/%m/%Y %H:%M:%S"),
            "fpath": hc_fpath,
            "raw": hc_detail[:2000]
        }
        print("2ª Instância capturada com sucesso!")
    except Exception as e:
        print(f"Erro 2ª Instância: {e}")
        results["portal_tjrj"][PROC_2A] = {"status": "erro", "erro": str(e)}

    # 5. STJ Consulta Direta
    print("\n--- Portal STJ (HC 1.116.750 / RJ) ---")
    URL_STJ_RE = "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo=202603112107"
    try:
        page.goto(URL_STJ_RE, wait_until="domcontentloaded", timeout=45000)
        time.sleep(5)
        
        # Se listou resultados, clica no link do processo
        page.evaluate("""() => {
            const links = Array.from(document.querySelectorAll('a'));
            const l = links.find(a => (a.textContent||'').includes('1116750') || (a.textContent||'').includes('2026/0311210-7') || (a.href||'').includes('num_registro=202603112107'));
            if(l) l.click();
        }""")
        time.sleep(6)
        
        stj_txt = page.evaluate("document.body.innerText")
        stj_fpath = os.path.join(OUT_DIR, "julio_stj_live_direct_19set.txt")
        with open(stj_fpath, "w", encoding="utf-8") as f:
            f.write(stj_txt)
        print(f"STJ Capturado ({len(stj_txt)} chars). Salvo em {stj_fpath}")

        relevant_stj = []
        for line in stj_txt.splitlines():
            if any(k in line.upper() for k in ["CONCLUSOS", "GABINETE", "FASE:", "ÚLTIMA FASE", "PARECER", "MINISTRO", "RELATOR"]):
                print(f"  • STJ Linha Relevante: {line.strip()}")
                relevant_stj.append(line.strip())

        results["portal_stj"] = {
            "status": "sucesso",
            "fpath": stj_fpath,
            "relevant_lines": relevant_stj[:10],
            "raw": stj_txt[:2500]
        }
    except Exception as e:
        print(f"Erro STJ Scraping: {e}")
        results["portal_stj"] = {"status": "erro", "erro": str(e)}

    # 6. DJERJ Consulta de Publicações recentes (01/09 a 19/09/2026)
    print("\n--- DJERJ Consulta de Publicações (01/09/2026 a 19/09/2026) ---")
    for proc_fmt, _, _ in PROCS_TJRJ + [(PROC_2A, "", "2ª Instância")]:
        url_djerj = f"https://www3.tjrj.jus.br/consultadje/Result.aspx?dtInicio=01%2F09%2F2026&dtFim=19%2F09%2F2026&txtPesq={proc_fmt}&tipoPesq=PROC"
        try:
            page.goto(url_djerj, wait_until="domcontentloaded", timeout=45000)
            time.sleep(4)
            djerj_body = page.evaluate("document.body.innerText")
            if "Não foram encontradas" in djerj_body or "Nenhum registro encontrado" in djerj_body:
                print(f"  • {proc_fmt}: Sem novas publicações no DJERJ.")
                results["djerj"][proc_fmt] = "Sem publicações no período (01 a 19/09/2026)"
            else:
                print(f"  🚨 {proc_fmt}: PUBLICAÇÃO LOCALIZADA!\n{djerj_body[:1000]}")
                results["djerj"][proc_fmt] = djerj_body[:2000]
        except Exception as e:
            print(f"Erro DJERJ {proc_fmt}: {e}")
            results["djerj"][proc_fmt] = f"Erro: {e}"

    # DJERJ por nome
    try:
        url_nome = "https://www3.tjrj.jus.br/consultadje/Result.aspx?dtInicio=01%2F09%2F2026&dtFim=19%2F09%2F2026&txtPesq=Julio%20Pereira%20Marcos&tipoPesq=NOME"
        page.goto(url_nome, wait_until="domcontentloaded", timeout=45000)
        time.sleep(4)
        djerj_nome = page.evaluate("document.body.innerText")
        if "Não foram encontradas" in djerj_nome or "Nenhum registro encontrado" in djerj_nome:
            print("  • Julio Pereira Marcos: Sem publicações no DJERJ.")
            results["djerj"]["Julio Pereira Marcos"] = "Sem publicações no período (01 a 19/09/2026)"
        else:
            print(f"  🚨 Julio Pereira Marcos: PUBLICAÇÃO LOCALIZADA!\n{djerj_nome[:1000]}")
            results["djerj"]["Julio Pereira Marcos"] = djerj_nome[:2000]
    except Exception as e:
        print(f"Erro DJERJ Nome: {e}")
        results["djerj"]["Julio Pereira Marcos"] = f"Erro: {e}"

    browser.close()

# Salvar json de resultados no superJus e no swedsystem
json_out = os.path.join(r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal", "consulta_ao_vivo_19_09_2026.json")
with open(json_out, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

swed_json_out = r"C:\Projetos\swedsystem\docs\consulta_ao_vivo_19_09_2026.json"
with open(swed_json_out, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n" + "="*70)
print(f"✅ CHECAGEM 19/09/2026 CONCLUÍDA! DADOS SALVOS EM:\n  {json_out}\n  {swed_json_out}")
print("="*70)
