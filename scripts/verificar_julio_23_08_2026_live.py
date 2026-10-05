# -*- coding: utf-8 -*-
"""
Varredura AO VIVO - Processos de Júlio Pereira Marcos
Data: 23/08/2026
Fontes:
  1. Datajud CNJ (TJRJ e STJ)
  2. TJRJ 1ª Instância (Búzios - Principal, Apenso RSE e Originário)
  3. TJRJ 2ª Instância (7ª Câmara Criminal - HC 2026.059.10770 e ROC 2026.141.00580)
  4. DJERJ Novo (Diário da Justiça RJ)
  5. STJ (HC 1.116.750 / RJ - 6ª Turma / Min. Og Fernandes)
"""
import os
import sys
import time
import json
import urllib.request
import re

sys.stdout.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

DATAJUD_API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {
    'Authorization': f'APIKey {DATAJUD_API_KEY}',
    'Content-Type': 'application/json'
}

OUT_DIR = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\_varredura_23_08_2026"
os.makedirs(OUT_DIR, exist_ok=True)

PROCS_1A = [
    ("0023013-51.2021.8.19.0078", "00230135120218190078", "1A_Principal_Julio", "Ação Penal Desmembrada - 2ª Vara Búzios"),
    ("0001140-87.2024.8.19.0078", "00011408720248190078", "1A_Apenso_RSE", "Recurso em Sentido Estrito / Apenso Búzios"),
    ("0022975-39.2021.8.19.0078", "00229753920218190078", "1A_Original_Desmembrado", "Processo Originário / Co-réus Búzios")
]

PROC_2A = "0029845-67.2026.8.19.0000"
PROC_2A_CLEAN = "00298456720268190000"
STJ_URL = "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo=202603112107&totalRegistrosPorPagina=40&aplicacao=processos.ea"

results = {
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "datajud": {},
    "tjrj_1a": {},
    "tjrj_2a": {},
    "djerj": {},
    "stj": {}
}

def save_file(filename, content):
    p = os.path.join(OUT_DIR, filename)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    return p

print("="*80)
print("=== CONSULTA AO VIVO ONLINE — JÚLIO PEREIRA MARCOS (23/08/2026) ===")
print("="*80, flush=True)

# 1. CONSULTA DATAJUD CNJ API
print("\n>>> [1/5] CONSULTANDO DATAJUD CNJ API (TJRJ e STJ)...", flush=True)
for cnj_fmt, cnj_clean, label, desc in PROCS_1A + [(PROC_2A, PROC_2A_CLEAN, "2A_HC_ROC", "HC e ROC 2ª Instância TJRJ")]:
    try:
        url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
        payload = json.dumps({"query": {"match": {"numeroProcesso": cnj_clean}}, "size": 10}).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as resp:
            dj_data = json.loads(resp.read().decode('utf-8'))
            hits = dj_data.get('hits', {}).get('hits', [])
            print(f"  • DataJud TJRJ [{label} - {cnj_fmt}]: {len(hits)} registro(s)")
            entries = []
            for hit in hits:
                src = hit['_source']
                orgao = src.get('orgaoJulgador', {}).get('nome', 'N/A')
                classe = src.get('classe', {}).get('nome', 'N/A')
                dt_up = src.get('dataHoraUltimaAtualizacao', 'N/A')
                movs = src.get('movimentos', [])
                movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
                top_movs = []
                for m in movs_sorted[:6]:
                    top_movs.append({
                        "dataHora": m.get('dataHora', '')[:19].replace('T', ' '),
                        "nome": m.get('nome', ''),
                        "complemento": ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in m.get('complementosTabelados', [])]) if m.get('complementosTabelados') else ""
                    })
                entries.append({
                    "orgao": orgao,
                    "classe": classe,
                    "ultimaAtualizacao": dt_up,
                    "totalMovimentos": len(movs),
                    "ultimosMovimentos": top_movs
                })
            results["datajud"][label] = entries
    except Exception as e:
        print(f"  [ERRO] DataJud {label}: {e}")
        results["datajud"][label] = {"erro": str(e)}

# STJ via Datajud
try:
    url_stj = 'https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search'
    payload_stj = json.dumps({"query": {"match_phrase": {"pessoas.nome": "Julio Pereira Marcos"}}, "size": 5}).encode('utf-8')
    req_stj = urllib.request.Request(url_stj, data=payload_stj, headers=HEADERS)
    with urllib.request.urlopen(req_stj, timeout=20) as resp:
        data_stj = json.loads(resp.read().decode('utf-8'))
        hits_stj = data_stj.get('hits', {}).get('hits', [])
        print(f"  • DataJud STJ (Júlio Pereira Marcos): {len(hits_stj)} registro(s)")
        stj_entries = []
        for h in hits_stj:
            src = h['_source']
            movs = src.get('movimentos', [])
            movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
            stj_entries.append({
                "numeroProcesso": src.get('numeroProcesso'),
                "classe": src.get('classe', {}).get('nome'),
                "ultimaAtualizacao": src.get('dataHoraUltimaAtualizacao'),
                "ultimosMovimentos": [{"dataHora": m.get('dataHora', '')[:19].replace('T', ' '), "nome": m.get('nome', '')} for m in movs_sorted[:6]]
            })
        results["datajud"]["STJ"] = stj_entries
except Exception as e:
    print(f"  [ERRO] DataJud STJ: {e}")
    results["datajud"]["STJ"] = {"erro": str(e)}

# 2. PLAYWRIGHT
from playwright.sync_api import sync_playwright

def parse_movements(text):
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    loc = "Não identificada"
    movs = []
    for i, l in enumerate(lines):
        if "Localização na Serventia" in l and i+1 < len(lines):
            loc = lines[i+1]
        if "Tipo do Movimento:" in l:
            bloco = lines[i:min(len(lines), i+8)]
            movs.append(" | ".join(bloco))
    return loc, movs

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

    # 2.1 TJRJ 1ª INSTÂNCIA (BÚZIOS)
    print("\n>>> [2/5] RASPANDO TJRJ 1ª INSTÂNCIA (BÚZIOS)...", flush=True)
    for cnj, _, label, desc in PROCS_1A:
        print(f"  • Consultando {label} ({cnj} - {desc})...", flush=True)
        try:
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=50000, wait_until="domcontentloaded")
            time.sleep(4)
            iframe_el = page.wait_for_selector("iframe#mainframe", timeout=30000)
            frame = iframe_el.content_frame()
            inp = frame.wait_for_selector("input[name='numeroProcesso']", timeout=20000)
            inp.fill(cnj)
            time.sleep(1)

            btns = frame.query_selector_all("button")
            btn_pesq = next((b for b in btns if any(w in b.inner_text().lower() for w in ["pesquisar", "buscar", "consultar"])), btns[0] if btns else None)
            if btn_pesq:
                btn_pesq.click()
            time.sleep(7)

            try:
                btn_all = frame.query_selector("button:has-text('Todos Os Movimentos'), a:has-text('Todos Os Movimentos')")
                if btn_all:
                    btn_all.click()
                    time.sleep(4)
            except Exception:
                pass

            body_txt = frame.inner_text("body")
            html_txt = frame.evaluate("document.documentElement.outerHTML")
            save_file(f"{label}.txt", body_txt)
            save_file(f"{label}.html", html_txt)
            
            loc, movs = parse_movements(body_txt)
            total_m = body_txt.count("Tipo do Movimento:")
            results["tjrj_1a"][label] = {
                "cnj": cnj,
                "descricao": desc,
                "localizacao": loc,
                "total_movimentos": total_m,
                "ultimos_movimentos": movs[:5],
                "corpo_completo": body_txt
            }
            print(f"    [OK] Local: {loc} | Total Movs: {total_m}")
            for m in movs[:3]:
                print(f"      -> {m}")
        except Exception as e:
            print(f"    [ERRO] {label}: {e}", flush=True)
            results["tjrj_1a"][label] = {"erro": str(e)}

    # 2.2 TJRJ 2ª INSTÂNCIA (HC E ROC)
    print("\n>>> [3/5] RASPANDO TJRJ 2ª INSTÂNCIA (7ª CÂMARA CRIMINAL / 2VP)...", flush=True)
    for sub_target, sub_label, sub_desc in [
        ("2026.059.10770", "2A_HC_10770", "Habeas Corpus - 7ª Câmara Criminal"),
        ("2026.141.00580", "2A_ROC_00580", "Recurso Ordinário Constitucional - 2ª Vice-Presidência")
    ]:
        print(f"  • Consultando {sub_label} ({sub_target} - {sub_desc})...", flush=True)
        try:
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=50000, wait_until="domcontentloaded")
            time.sleep(4)
            iframe_el = page.wait_for_selector("iframe#mainframe", timeout=30000)
            frame = iframe_el.content_frame()
            inp = frame.wait_for_selector("input[name='numeroProcesso']", timeout=20000)
            inp.fill(PROC_2A)
            time.sleep(1)

            btns = frame.query_selector_all("button")
            btn_pesq = next((b for b in btns if any(w in b.inner_text().lower() for w in ["pesquisar", "buscar", "consultar"])), btns[0] if btns else None)
            if btn_pesq:
                btn_pesq.click()
            time.sleep(7)

            frame.evaluate(f"""(target) => {{
                const links = Array.from(document.querySelectorAll('table a, .table a, a'));
                const l = links.find(a => (a.textContent||'').includes(target));
                if(l) l.click();
            }}""", sub_target)
            time.sleep(6)

            try:
                btn_all = frame.query_selector("button:has-text('Todos Os Movimentos'), a:has-text('Todos Os Movimentos')")
                if btn_all:
                    btn_all.click()
                    time.sleep(4)
            except Exception:
                pass

            proc_txt = frame.inner_text("body")
            html_txt = frame.evaluate("document.documentElement.outerHTML")
            save_file(f"{sub_label}.txt", proc_txt)
            save_file(f"{sub_label}.html", html_txt)
            
            loc_2, movs_2 = parse_movements(proc_txt)
            results["tjrj_2a"][sub_label] = {
                "processo_origem": PROC_2A,
                "registro": sub_target,
                "descricao": sub_desc,
                "localizacao": loc_2,
                "total_movimentos": proc_txt.count("Tipo do Movimento:"),
                "ultimos_movimentos": movs_2[:5],
                "corpo_completo": proc_txt
            }
            print(f"    [OK] Local: {loc_2} | Movs: {proc_txt.count('Tipo do Movimento:')}")
            for m in movs_2[:3]:
                print(f"      -> {m}")
        except Exception as e:
            print(f"    [ERRO] {sub_label}: {e}", flush=True)
            results["tjrj_2a"][sub_label] = {"erro": str(e)}

    # 2.3 DJERJ NOVO
    print("\n>>> [4/5] RASPANDO DIÁRIO DA JUSTIÇA ELETRÔNICO DO RJ (DJERJ)...", flush=True)
    for q in ["0023013-51.2021.8.19.0078", "0029845-67.2026.8.19.0000", "0001140-87.2024.8.19.0078", "Julio Pereira Marcos"]:
        is_name = (q == "Julio Pereira Marcos")
        safe_type = "NOME" if is_name else "PROC"
        safe_param = "Julio%20Pereira%20Marcos" if is_name else q
        dje_url = f"https://www3.tjrj.jus.br/consultadje/Result.aspx?dtInicio=01%2F08%2F2026&dtFim=23%2F08%2F2026&txtPesq={safe_param}&tipoPesq={safe_type}"
        try:
            page.goto(dje_url, timeout=35000, wait_until="domcontentloaded")
            time.sleep(5)
            txt = page.evaluate("document.body.innerText")
            safe = q.replace('.', '_').replace('-', '_').replace(' ', '_')
            save_file(f"DJERJ_{safe}.txt", txt)
            has_pub = "Não foram encontradas" not in txt and "Nenhum registro encontrado" not in txt and "0 registros" not in txt.lower()
            print(f"  • DJERJ [{q}]: {'🚨 PUBLICAÇÃO ENCONTRADA!' if has_pub else '✅ Nenhuma publicação encontrada no período'}")
            results["djerj"][q] = {
                "tem_publicacao": has_pub,
                "conteudo": txt if has_pub else "Nenhuma publicação no período de 01/08/2026 a 23/08/2026."
            }
        except Exception as e:
            print(f"    [ERRO] DJERJ {q}: {e}")
            results["djerj"][q] = {"erro": str(e)}

    # 2.4 STJ (HC 1.116.750 / RJ - MIN. OG FERNANDES)
    print("\n>>> [5/5] RASPANDO STJ (HC 1.116.750 / RJ - REGISTRO 2026/0311210-7)...", flush=True)
    try:
        page.goto(STJ_URL, timeout=50000, wait_until="domcontentloaded")
        time.sleep(6)
        
        page.evaluate("""() => {
            const links = document.querySelectorAll('a, span, td');
            for(const el of links) {
                if((el.textContent||'').includes('1116750') && el.offsetParent !== null) {
                    el.click(); return true;
                }
            }
            return false;
        }""")
        time.sleep(6)
        
        stj_txt = page.evaluate("document.body.innerText")
        stj_html = page.content()
        save_file("STJ_HC1116750_principal.txt", stj_txt)
        save_file("STJ_HC1116750_principal.html", stj_html)
        
        seqs = list(set(re.findall(r'sequencial=(\d+)', stj_html)))
        
        stj_lines = [l.strip() for l in stj_txt.split('\n') if l.strip()]
        relevant_stj = []
        for l in stj_lines:
            if any(k in l.upper() for k in ["ÚLTIMA FASE", "CONCLUSOS", "DECISÃO", "JULGAMENTO", "LOCALIZAÇÃO", "RELATOR", "MINISTRO", "PETIÇÃO", "PARECER"]):
                relevant_stj.append(l)
                
        results["stj"] = {
            "status": "sucesso",
            "sequenciais": seqs,
            "linhas_relevantes": relevant_stj,
            "corpo_completo": stj_txt
        }
        print(f"  [OK] STJ capturado com sucesso! ({len(stj_txt)} caracteres)")
        for l in relevant_stj[:6]:
            print(f"    * {l}")
    except Exception as e:
        print(f"  [ERRO] STJ: {e}")
        results["stj"] = {"erro": str(e)}

    browser.close()

# Salvar json consolidado
json_path = os.path.join(OUT_DIR, "varredura_23_08_2026.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n" + "="*80)
print(f"=== VARREDURA 23/08/2026 FINALIZADA COM SUCESSO! ===")
print(f"Dados salvos em: {OUT_DIR}")
print("="*80, flush=True)
