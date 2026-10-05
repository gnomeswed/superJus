# -*- coding: utf-8 -*-
"""
Varredura AO VIVO - Processos de Júlio Pereira Marcos
Data: 22/08/2026 (17:01)
Fontes: TJRJ 1ª Instância (Búzios), TJRJ 2ª Instância (HC / ROC), DJERJ Novo, STJ (HC 1.116.750/RJ)
"""
import os
import sys
import time
import json
import re

sys.stdout.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

from playwright.sync_api import sync_playwright

OUT_DIR = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\_varredura_22_08_2026"
os.makedirs(OUT_DIR, exist_ok=True)

PROCS_1A = [
    ("0023013-51.2021.8.19.0078", "1A_Principal_Julio"),
    ("0001140-87.2024.8.19.0078", "1A_Apenso_RSE"),
    ("0022975-39.2021.8.19.0078", "1A_Original_Desmembrado")
]

PROC_2A = "0029845-67.2026.8.19.0000"
STJ_URL = "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo=202603112107&totalRegistrosPorPagina=40&aplicacao=processos.ea"

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
print(f"=== VARREDURA AO VIVO — JÚLIO PEREIRA MARCOS (22/08/2026 17:01) ===")
print(f"==========================================================================\n", flush=True)

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

    # =========================================================================
    # 1. TJRJ 1ª INSTÂNCIA (BÚZIOS)
    # =========================================================================
    for cnj, label in PROCS_1A:
        print(f"\n[TJRJ 1ª INSTÂNCIA] {label} ({cnj})...", flush=True)
        try:
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
            time.sleep(4)
            iframe_el = page.wait_for_selector("iframe#mainframe", timeout=25000)
            frame = iframe_el.content_frame()
            inp = frame.wait_for_selector("input[name='numeroProcesso']", timeout=15000)
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
            save_text(f"{label}.txt", body_txt)
            save_text(f"{label}.html", frame.evaluate("document.documentElement.outerHTML"))
            
            loc, movs = parse_movements(body_txt)
            results[label] = {
                "localizacao": loc,
                "total_movimentos": body_txt.count("Tipo do Movimento:"),
                "movimentos": movs[:5],
                "texto": body_txt
            }
            print(f"[OK] {label}: Local: {loc} | Movs: {body_txt.count('Tipo do Movimento:')}", flush=True)
            for m in movs[:3]:
                print(f"  * {m}", flush=True)
        except Exception as e:
            print(f"[ERRO] {label}: {e}", flush=True)
            results[label] = {"erro": str(e)}

    # =========================================================================
    # 2. TJRJ 2ª INSTÂNCIA (HC e ROC)
    # =========================================================================
    print(f"\n[TJRJ 2ª INSTÂNCIA] {PROC_2A}...", flush=True)
    for sub_target, sub_label in [("2026.059.10770", "2A_HC_10770"), ("2026.141.00580", "2A_ROC_00580")]:
        try:
            print(f"Consultando {sub_label} ({sub_target})...", flush=True)
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
            time.sleep(4)
            iframe_el = page.wait_for_selector("iframe#mainframe", timeout=25000)
            frame = iframe_el.content_frame()
            inp = frame.wait_for_selector("input[name='numeroProcesso']", timeout=15000)
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
            save_text(f"{sub_label}.txt", proc_txt)
            results[sub_label] = proc_txt
            loc_2, movs_2 = parse_movements(proc_txt)
            print(f"[OK] {sub_label}: Local: {loc_2} | Chars: {len(proc_txt)}", flush=True)
            for line in [l.strip() for l in proc_txt.split('\n') if l.strip()][:15]:
                print(f"  > {line[:120]}", flush=True)
        except Exception as e:
            print(f"[ERRO] 2ª Instância {sub_label}: {e}", flush=True)
            results[sub_label] = f"ERRO: {e}"

    # =========================================================================
    # 3. DJERJ NOVO
    # =========================================================================
    print(f"\n[DJERJ NOVO] Consulta 15/08/2026 a 22/08/2026...", flush=True)
    for cnj in ["0023013-51.2021.8.19.0078", "0029845-67.2026.8.19.0000", "0001140-87.2024.8.19.0078", "Julio Pereira Marcos"]:
        is_name = (cnj == "Julio Pereira Marcos")
        safe_type = "NOME" if is_name else "PROC"
        safe_param = "Julio%20Pereira%20Marcos" if is_name else cnj
        dje_url = (
            f"https://www3.tjrj.jus.br/consultadje/Result.aspx"
            f"?dtInicio=15%2F08%2F2026"
            f"&dtFim=22%2F08%2F2026"
            f"&txtPesq={safe_param}"
            f"&tipoPesq={safe_type}"
        )
        try:
            page.goto(dje_url, timeout=35000, wait_until="domcontentloaded")
            time.sleep(5)
            txt = page.evaluate("document.body.innerText")
            safe = cnj.replace('.', '_').replace('-', '_').replace(' ', '_')
            save_text(f"DJERJ_{safe}.txt", txt)
            has_pub = "Não foram encontradas" not in txt and "Nenhum registro encontrado" not in txt and "0 registros" not in txt.lower()
            print(f"  • DJERJ {cnj}: Publicação? {'SIM' if has_pub else 'NÃO'} ({len(txt)} chars)", flush=True)
            results[f"DJERJ_{safe}"] = {"tem_pub": has_pub, "texto": txt}
        except Exception as e:
            print(f"[ERRO] DJERJ {cnj}: {e}", flush=True)

    # =========================================================================
    # 4. STJ (HC 1.116.750/RJ - Min. Og Fernandes)
    # =========================================================================
    print(f"\n[STJ] HC 1.116.750 / RJ (Registro 2026/0311210-7)...", flush=True)
    try:
        page.goto(STJ_URL, timeout=45000, wait_until="domcontentloaded")
        time.sleep(6)
        stj_body = page.evaluate("document.body.innerText")
        save_text("STJ_HC1116750_principal.txt", stj_body)
        results["STJ_principal"] = stj_body
        print(f"[OK] STJ capturado: {len(stj_body)} chars", flush=True)
        for l in stj_body.split('\n'):
            if any(k in l for k in ["ÚLTIMA FASE", "Conclusos", "Decisão", "Julgamento", "LOCALIZAÇÃO"]):
                print(f"  [STJ Info] {l.strip()}", flush=True)
    except Exception as e:
        print(f"[ERRO] STJ: {e}", flush=True)
        results["STJ_principal"] = f"ERRO: {e}"

    browser.close()

with open(os.path.join(OUT_DIR, "varredura_22_08_2026.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\n==========================================================================")
print(f"=== VARREDURA 22/08/2026 CONCLUÍDA COM SUCESSO! ===")
print("==========================================================================", flush=True)
