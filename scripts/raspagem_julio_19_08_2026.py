# -*- coding: utf-8 -*-
"""
RASPAGEM OFICIAL AO VIVO - JÚLIO PEREIRA MARCOS
Data da consulta: 19/08/2026
Fontes: TJRJ 1ª Instância (Búzios), TJRJ 2ª Instância (HC e ROC), DJERJ Novo e STJ (HC 1.116.750/RJ)
"""
import os
import sys
import time
import json
import re

sys.stdout.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

from playwright.sync_api import sync_playwright

OUT_DIR = r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\documentos_processo\_varredura_19_08_2026"
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
    # 1. TJRJ 1ª INSTÂNCIA
    # =========================================================================
    for cnj, label in PROCS_1A:
        print(f"\n==========================================", flush=True)
        print(f"1ª INSTÂNCIA TJRJ: {label} ({cnj})", flush=True)
        print(f"==========================================", flush=True)
        try:
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
            time.sleep(3)
            iframe_el = page.wait_for_selector("iframe#mainframe", timeout=25000)
            frame = iframe_el.content_frame()
            if not frame:
                raise RuntimeError("Iframe mainframe not found")
            
            inp = frame.wait_for_selector("input[name='numeroProcesso']", timeout=15000)
            inp.fill(cnj)
            time.sleep(1)

            btns = frame.query_selector_all("button")
            btn_pesq = None
            for b in btns:
                if any(w in b.inner_text().lower() for w in ["pesquisar", "buscar", "consultar"]):
                    btn_pesq = b
                    break
            if not btn_pesq and btns:
                btn_pesq = btns[0]
            btn_pesq.click()
            time.sleep(6)

            # Verificar se tem botão "Todos Os Movimentos"
            try:
                btn_all = frame.query_selector("button:has-text('Todos Os Movimentos'), a:has-text('Todos Os Movimentos')")
                if btn_all:
                    btn_all.click()
                    time.sleep(4)
            except Exception:
                pass

            body_txt = frame.inner_text("body")
            save_text(f"{label}.txt", body_txt)
            html_txt = frame.evaluate("document.documentElement.outerHTML")
            save_text(f"{label}.html", html_txt)
            
            results[label] = body_txt
            print(f"[OK] Capturado {label}: {len(body_txt)} caracteres", flush=True)

            # Imprime primeiras linhas informativas
            for line in [l.strip() for l in body_txt.split('\n') if l.strip()][:25]:
                print(f"  > {line[:120]}", flush=True)

        except Exception as e:
            print(f"[ERRO] 1ª Instância {cnj}: {e}", flush=True)
            results[label] = f"ERRO: {e}"

    # =========================================================================
    # 2. TJRJ 2ª INSTÂNCIA (HC e ROC)
    # =========================================================================
    print(f"\n==========================================", flush=True)
    print(f"2ª INSTÂNCIA TJRJ: {PROC_2A}", flush=True)
    print(f"==========================================", flush=True)
    for sub_target, sub_label in [("2026.059.10770", "2A_HC_10770"), ("2026.141.00580", "2A_ROC_00580")]:
        try:
            print(f"\nConsultando {sub_label} ({sub_target})...", flush=True)
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
            time.sleep(3)
            iframe_el = page.wait_for_selector("iframe#mainframe", timeout=25000)
            frame = iframe_el.content_frame()
            
            inp = frame.wait_for_selector("input[name='numeroProcesso']", timeout=15000)
            inp.fill(PROC_2A)
            time.sleep(1)

            btns = frame.query_selector_all("button")
            btn_pesq = None
            for b in btns:
                if any(w in b.inner_text().lower() for w in ["pesquisar", "buscar", "consultar"]):
                    btn_pesq = b
                    break
            if not btn_pesq and btns:
                btn_pesq = btns[0]
            btn_pesq.click()
            time.sleep(6)

            # Clicar no link do recurso
            frame.evaluate(f"""(target) => {{
                const links = Array.from(document.querySelectorAll('table a, .table a, a'));
                const l = links.find(a => (a.textContent||'').includes(target));
                if(l) l.click();
            }}""", sub_target)
            time.sleep(6)

            # Clicar em todos os movimentos se houver
            try:
                btn_all = frame.query_selector("button:has-text('Todos Os Movimentos'), a:has-text('Todos Os Movimentos')")
                if btn_all:
                    btn_all.click()
                    time.sleep(4)
            except Exception:
                pass

            proc_txt = frame.inner_text("body")
            save_text(f"{sub_label}.txt", proc_txt)
            save_text(f"{sub_label}.html", frame.evaluate("document.documentElement.outerHTML"))
            results[sub_label] = proc_txt
            print(f"[OK] Capturado {sub_label}: {len(proc_txt)} caracteres", flush=True)

            for line in [l.strip() for l in proc_txt.split('\n') if l.strip()][:20]:
                print(f"  > {line[:120]}", flush=True)

        except Exception as e:
            print(f"[ERRO] 2ª Instância {sub_label}: {e}", flush=True)
            results[sub_label] = f"ERRO: {e}"

    # =========================================================================
    # 3. DJERJ NOVO (01/08/2026 a 19/08/2026)
    # =========================================================================
    print(f"\n==========================================", flush=True)
    print(f"DJERJ NOVO: 01/08/2026 a 19/08/2026", flush=True)
    print(f"==========================================", flush=True)
    for cnj in ["0023013-51.2021.8.19.0078", "0029845-67.2026.8.19.0000", "0001140-87.2024.8.19.0078", "Julio Pereira Marcos"]:
        is_name = (cnj == "Julio Pereira Marcos")
        safe_type = "NOME" if is_name else "PROC"
        safe_param = "Julio%20Pereira%20Marcos" if is_name else cnj
        dje_url = (
            f"https://www3.tjrj.jus.br/consultadje/Result.aspx"
            f"?dtInicio=01%2F08%2F2026"
            f"&dtFim=19%2F08%2F2026"
            f"&txtPesq={safe_param}"
            f"&tipoPesq={safe_type}"
        )
        try:
            print(f"Consultando DJERJ: {cnj}...", flush=True)
            page.goto(dje_url, timeout=35000, wait_until="domcontentloaded")
            time.sleep(5)
            txt = page.evaluate("document.body.innerText")
            safe = cnj.replace('.', '_').replace('-', '_').replace(' ', '_')
            save_text(f"DJERJ_{safe}.txt", txt)
            has_pub = "Nenhum registro encontrado" not in txt and "0 registros" not in txt.lower()
            print(f"  • DJERJ {cnj}: Publicação encontrada? {'SIM' if has_pub else 'NÃO'} ({len(txt)} chars)", flush=True)
            results[f"DJERJ_{safe}"] = {"tem_pub": has_pub, "texto": txt}
        except Exception as e:
            print(f"[ERRO] DJERJ {cnj}: {e}", flush=True)

    # =========================================================================
    # 4. STJ (HC 1.116.750/RJ)
    # =========================================================================
    print(f"\n==========================================", flush=True)
    print(f"STJ: HC 1.116.750 / RJ (Registro 2026/0311210-7)", flush=True)
    print(f"==========================================", flush=True)
    try:
        page.goto(STJ_URL, timeout=45000, wait_until="domcontentloaded")
        time.sleep(6)
        stj_body = page.evaluate("document.body.innerText")
        save_text("STJ_HC1116750_principal.txt", stj_body)

        for tab in ["Fases", "Decisões", "Petições"]:
            try:
                page.evaluate(f"""(name) => {{
                    const el = Array.from(document.querySelectorAll('a, button, li, span')).find(e => (e.textContent||'').trim().toLowerCase() === name.toLowerCase() && e.offsetWidth > 0);
                    if(el) el.click();
                }}""", tab)
                time.sleep(4)
                tab_txt = page.evaluate("document.body.innerText")
                save_text(f"STJ_HC1116750_aba_{tab}.txt", tab_txt)
                results[f"STJ_{tab}"] = tab_txt
                print(f"[OK] STJ Aba {tab} capturada: {len(tab_txt)} chars", flush=True)
                for line in [l.strip() for l in tab_txt.split('\n') if l.strip()][:15]:
                    print(f"  > {line[:120]}", flush=True)
            except Exception as te:
                print(f"  • Erro tab {tab}: {te}", flush=True)

        results["STJ_principal"] = stj_body
    except Exception as e:
        print(f"[ERRO] STJ: {e}", flush=True)
        results["STJ_principal"] = f"ERRO: {e}"

    browser.close()

# Salvar json final
with open(os.path.join(OUT_DIR, "varredura_final_19_08_2026.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n==========================================", flush=True)
print("VARREDURA COMPLETA 19/08/2026 FINALIZADA COM SUCESSO!", flush=True)
print(f"Arquivos salvos em: {OUT_DIR}", flush=True)
print("==========================================", flush=True)
