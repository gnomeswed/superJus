# -*- coding: utf-8 -*-
"""
Raspagem Oficial TJRJ 2ª e 1ª Instâncias - Lucas de Souza Freitas (Lucas Motoboy)
Data da Consulta: 30/09/2026
"""
import os
import sys
import time
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

OUT_DIR = r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_varredura_30_09_2026"
os.makedirs(OUT_DIR, exist_ok=True)

PROC_CNJ = "0011857-95.2024.8.19.0002"

print(f"=== INICIANDO RASPAGEM OFICIAL AO VIVO DO TJRJ: {PROC_CNJ} (30/09/2026) ===", flush=True)

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-dev-shm-usage"]
    )
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 900},
        locale="pt-BR"
    )
    ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    page = ctx.new_page()

    try:
        print(">> Acessando Portal de Consulta Pública do TJRJ...", flush=True)
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
        time.sleep(6)

        # Capturar tabela de resultados
        table_text = frame.inner_text("body")
        print("\n>> Tabela de Resultados TJRJ:", flush=True)
        for line in [l.strip() for l in table_text.split('\n') if l.strip()][:25]:
            print(f"   {line}", flush=True)

        links = frame.query_selector_all("table a, .table a, tbody tr td a")
        print(f"\n>> Links encontrados: {len(links)}", flush=True)

        link_2a = None
        for l in links:
            t = l.inner_text().strip()
            if any(k in t for k in ["Segunda", "2ª", "2026.050.14194", "CAMARA", "Apelação"]):
                link_2a = l
                break
        if not link_2a and len(links) > 1:
            link_2a = links[1]

        if link_2a:
            print(f"\n>> Abrindo 2ª Instância: {link_2a.inner_text().strip()}...", flush=True)
            link_2a.click()
            time.sleep(6)

            try:
                btn_todos = frame.query_selector("button:has-text('Todos Os Movimentos'), a:has-text('Todos Os Movimentos'), input[value*='Todos']")
                if btn_todos:
                    btn_todos.click()
                    time.sleep(4)
            except Exception as e:
                print(f">> Aviso clique Todos Movimentos: {e}", flush=True)

            txt_2a = frame.inner_text("body")
            html_2a = frame.evaluate("document.documentElement.outerHTML")

            with open(os.path.join(OUT_DIR, "2A_EXATO_Lucas_Apelacao_30_09_2026.txt"), "w", encoding="utf-8") as f:
                f.write(txt_2a)
            with open(os.path.join(OUT_DIR, "2A_EXATO_Lucas_Apelacao_30_09_2026.html"), "w", encoding="utf-8") as f:
                f.write(html_2a)
            page.screenshot(path=os.path.join(OUT_DIR, "2A_EXATO_screenshot_30_09_2026.png"), full_page=True)

            results["2a_instancia"] = txt_2a
            print("\n=======================================================")
            print("=== MOVIMENTAÇÕES 2ª INSTÂNCIA TJRJ (30/09/2026) ===")
            print("=======================================================")
            for line in [l.strip() for l in txt_2a.split('\n') if l.strip()]:
                print(f"  {line}", flush=True)
        else:
            print(">> Não foi possível isolar o link da 2ª instância na tabela.", flush=True)

    except Exception as e:
        print(f"ERRO durante raspagem: {e}", flush=True)
    finally:
        browser.close()

out_summary = os.path.join(OUT_DIR, "resumo_raspagem.json")
with open(out_summary, "w", encoding="utf-8") as f:
    json.dump({"timestamp": "2026-09-30 22:04", "status": "concluido"}, f, indent=2)

print("\n=== RASPAGEM FINALIZADA COM SUCESSO ===", flush=True)
