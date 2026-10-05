# -*- coding: utf-8 -*-
"""
Varredura AO VIVO - Lucas de Souza Freitas ("Motoboy Lucas")
Data: 21/08/2026 (Noite - 19:42)
Processo Principal: 0011857-95.2024.8.19.0002
Instâncias: TJRJ 1ª Instância (Niterói - 3ª Vara Criminal / Júri), TJRJ 2ª Instância (2ª Câmara Criminal - Apelação), DJERJ Novo, DataJud CNJ e Tribunais Superiores (STJ/STF)
"""
import os
import sys
import time
import json
import re
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

from playwright.sync_api import sync_playwright

OUT_DIR = r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_varredura_21_08_2026"
os.makedirs(OUT_DIR, exist_ok=True)

PROC_CNJ = "0011857-95.2024.8.19.0002"
PROC_CLEAN = "00118579520248190002"
NOME_CLIENTE = "Lucas de Souza Freitas"

results = {}

def save_text(fname, content):
    path = os.path.join(OUT_DIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

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

print(f"==========================================================================")
print(f"=== CONSULTA EM TEMPO REAL — LUCAS DE SOUZA FREITAS (MOTOBOY LUCAS) ===")
print(f"=== Data/Hora: {time.strftime('%Y-%m-%d %H:%M:%S')} ===")
print(f"==========================================================================\n", flush=True)

# -------------------------------------------------------------------------
# 1. TJRJ 1ª e 2ª INSTÂNCIAS (PLAYWRIGHT LIVE)
# -------------------------------------------------------------------------
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

    # --- 1.1 TJRJ 1ª INSTÂNCIA ---
    print(f"[TJRJ 1ª INSTÂNCIA] Consultando {PROC_CNJ}...", flush=True)
    try:
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
        time.sleep(4)
        iframe_el = page.wait_for_selector("iframe#mainframe", timeout=25000)
        frame = iframe_el.content_frame()
        inp = frame.wait_for_selector("input[name='numeroProcesso']", timeout=15000)
        inp.fill(PROC_CNJ)
        time.sleep(1)

        btns = frame.query_selector_all("button")
        btn_pesq = next((b for b in btns if any(w in b.inner_text().lower() for w in ["pesquisar", "buscar", "consultar"])), btns[0] if btns else None)
        if btn_pesq:
            btn_pesq.click()
        time.sleep(7)

        # Se houver lista de instâncias ou entrar direto
        try:
            btn_all = frame.query_selector("button:has-text('Todos Os Movimentos'), a:has-text('Todos Os Movimentos')")
            if btn_all:
                btn_all.click()
                time.sleep(4)
        except Exception:
            pass

        body_1a = frame.inner_text("body")
        save_text("1A_TJRJ_Lucas_0011857.txt", body_1a)
        save_text("1A_TJRJ_Lucas_0011857.html", frame.evaluate("document.documentElement.outerHTML"))
        loc_1a, movs_1a = parse_movements(body_1a)
        results["1a_instancia"] = {
            "localizacao": loc_1a,
            "total_movimentos": body_1a.count("Tipo do Movimento:"),
            "movimentos": movs_1a[:10],
            "texto": body_1a
        }
        print(f"[OK] 1ª Instância capturada! Local: {loc_1a} | Total Movs: {body_1a.count('Tipo do Movimento:')}", flush=True)
        for m in movs_1a[:5]:
            print(f"  * {m}", flush=True)
    except Exception as e:
        print(f"[ERRO] 1ª Instância: {e}", flush=True)
        results["1a_instancia"] = {"erro": str(e)}

    # --- 1.2 TJRJ 2ª INSTÂNCIA (APELAÇÃO) ---
    print(f"\n[TJRJ 2ª INSTÂNCIA] Consultando Apelação Criminal {PROC_CNJ}...", flush=True)
    try:
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
        time.sleep(4)
        iframe_el = page.wait_for_selector("iframe#mainframe", timeout=25000)
        frame = iframe_el.content_frame()
        inp = frame.wait_for_selector("input[name='numeroProcesso']", timeout=15000)
        inp.fill(PROC_CNJ)
        time.sleep(1)

        btns = frame.query_selector_all("button")
        btn_pesq = next((b for b in btns if any(w in b.inner_text().lower() for w in ["pesquisar", "buscar", "consultar"])), btns[0] if btns else None)
        if btn_pesq:
            btn_pesq.click()
        time.sleep(7)

        # Se houver link para 2ª Instância na tabela de resultados
        links = frame.query_selector_all("table a, .table a, tbody tr td a")
        print(f"Links encontrados na busca: {len(links)}", flush=True)
        clicked_2a = False
        for l in links:
            txt = l.inner_text().strip()
            if any(k in txt for k in ["Segunda Instância", "2ª Instância", "Apelação", "0011857", "2ª Câmara"]):
                l.click()
                time.sleep(6)
                clicked_2a = True
                break

        try:
            btn_all2 = frame.query_selector("button:has-text('Todos Os Movimentos'), a:has-text('Todos Os Movimentos')")
            if btn_all2:
                btn_all2.click()
                time.sleep(4)
        except Exception:
            pass

        body_2a = frame.inner_text("body")
        save_text("2A_TJRJ_Lucas_Apelacao.txt", body_2a)
        save_text("2A_TJRJ_Lucas_Apelacao.html", frame.evaluate("document.documentElement.outerHTML"))
        loc_2a, movs_2a = parse_movements(body_2a)
        results["2a_instancia"] = {
            "localizacao": loc_2a,
            "movimentos": movs_2a[:10],
            "texto": body_2a
        }
        print(f"[OK] 2ª Instância capturada! Local: {loc_2a} | Chars: {len(body_2a)}", flush=True)
        for line in [l.strip() for l in body_2a.split('\n') if l.strip()][:20]:
            print(f"  > {line[:120]}", flush=True)
    except Exception as e:
        print(f"[ERRO] 2ª Instância: {e}", flush=True)
        results["2a_instancia"] = {"erro": str(e)}

    # --- 1.3 DJERJ NOVO ---
    print(f"\n[DJERJ NOVO] Consulta 01/08/2026 a 21/08/2026...", flush=True)
    for q_term, q_type, q_label in [(PROC_CNJ, "PROC", "proc"), (NOME_CLIENTE, "NOME", "nome")]:
        safe_param = urllib.parse.quote(q_term)
        dje_url = f"https://www3.tjrj.jus.br/consultadje/Result.aspx?dtInicio=01%2F08%2F2026&dtFim=21%2F08%2F2026&txtPesq={safe_param}&tipoPesq={q_type}"
        try:
            page.goto(dje_url, timeout=35000, wait_until="domcontentloaded")
            time.sleep(5)
            txt = page.evaluate("document.body.innerText")
            save_text(f"DJERJ_Lucas_{q_label}.txt", txt)
            has_pub = "Nenhum registro encontrado" not in txt and "0 registros" not in txt.lower()
            print(f"  • DJERJ ({q_label}): Publicação encontrada? {'SIM' if has_pub else 'NÃO'} ({len(txt)} chars)", flush=True)
            results[f"djerj_{q_label}"] = {"tem_pub": has_pub, "texto": txt}
        except Exception as e:
            print(f"[ERRO] DJERJ {q_label}: {e}", flush=True)

    browser.close()

# -------------------------------------------------------------------------
# 2. DATAJUD CNJ API (TJRJ, STJ, STF)
# -------------------------------------------------------------------------
print(f"\n[DATAJUD CNJ] Consultando APIs oficiais...", flush=True)
try:
    auth_header = __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization']
    dj_headers = {'Authorization': auth_header, 'Content-Type': 'application/json'}
    
    def q_dj(endpoint, payload):
        req = urllib.request.Request(f"https://api-publica.datajud.cnj.jus.br/{endpoint}/_search", data=json.dumps(payload).encode('utf-8'), headers=dj_headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode('utf-8'))

    # TJRJ
    dj_tjrj = q_dj("api_publica_tjrj", {"query": {"match": {"numeroProcesso": PROC_CLEAN}}, "size": 10})
    hits_tjrj = dj_tjrj.get('hits', {}).get('hits', [])
    print(f"  • DataJud TJRJ Hits: {len(hits_tjrj)}", flush=True)
    results["datajud_tjrj"] = hits_tjrj
    save_text("datajud_tjrj_lucas.json", json.dumps(dj_tjrj, indent=2, ensure_ascii=False))

    for h in hits_tjrj:
        src = h['_source']
        print(f"    - Órgão: {src.get('orgaoJulgador', {}).get('nome')} | Classe: {src.get('classe', {}).get('nome')} | Atualização: {src.get('dataHoraUltimaAtualizacao')}", flush=True)
        movs = sorted(src.get('movimentos', []), key=lambda m: m.get('dataHora', ''), reverse=True)
        for m in movs[:3]:
            print(f"      * {m.get('dataHora')[:19].replace('T', ' ')} — {m.get('nome')}", flush=True)

    # STJ
    dj_stj = q_dj("api_publica_stj", {"query": {"match_phrase": {"partes.nome": NOME_CLIENTE}}, "size": 5})
    hits_stj = dj_stj.get('hits', {}).get('hits', [])
    print(f"  • DataJud STJ Hits: {len(hits_stj)}", flush=True)
    results["datajud_stj"] = hits_stj

except Exception as e:
    print(f"  [Aviso DataJud]: {e}", flush=True)
    results["datajud_erro"] = str(e)

# Salvar consolidado final
with open(os.path.join(OUT_DIR, "resultado_lucas_21_08_2026.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n==========================================================================")
print(f"=== VARREDURA COMPLETA DE LUCAS CONCLUÍDA! ===")
print(f"=== Arquivos salvos em: {OUT_DIR} ===")
print(f"==========================================================================", flush=True)
