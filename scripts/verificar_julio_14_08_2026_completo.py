# -*- coding: utf-8 -*-
"""
Verificação completa e detalhada em tempo real no TJRJ
Data: 14/08/2026
Processos de Júlio Pereira Marcos:
1) 1ª Instância (Búzios): 0023013-51.2021.8.19.0078
2) 2ª Instância (TJRJ - HC / ROC): 0029845-67.2026.8.19.0000
3) DJERJ Novo: Consulta de publicações 01/08/2026 a 14/08/2026
4) Processo Originário: 0022975-39.2021.8.19.0078
"""
import os
import sys
import time
import json
import logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
sys.stdout.reconfigure(encoding="utf-8")
os.environ["PYTHONIOENCODING"] = "utf-8"

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
    )
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 900},
    )
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # ----------------------------------------------------
    # 1. Processo 1ª Instância Búzios (0023013-51.2021.8.19.0078)
    # ----------------------------------------------------
    logging.info("=== Consultando 1ª Instância (0023013-51.2021.8.19.0078) ===")
    try:
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
        time.sleep(4)
        iframe_el = page.wait_for_selector("iframe#mainframe", timeout=20000)
        frame = iframe_el.content_frame()
        if not frame:
            raise RuntimeError("iframe#mainframe não encontrado")
        
        frame.query_selector("input[name='numeroProcesso']").fill("0023013-51.2021.8.19.0078")
        btns = frame.query_selector_all("button")
        btn = [b for b in btns if any(w in b.inner_text().lower() for w in ["pesquisar", "buscar", "consultar"])][0]
        btn.click()
        time.sleep(6)
        
        # Clica em Todos Os Movimentos
        link_movs = frame.query_selector("a:has-text('Todos Os Movimentos'), button:has-text('Todos Os Movimentos')")
        if link_movs:
            link_movs.click()
            time.sleep(4)
            
        txt_1inst = frame.inner_text("body")
        results["1a_instancia_buzios"] = txt_1inst
        logging.info(f"1ª Instância capturada com sucesso: {len(txt_1inst)} chars")
    except Exception as e:
        logging.error(f"Erro ao consultar 1ª Instância: {e}")
        results["1a_instancia_buzios"] = f"ERRO: {e}"

    # ----------------------------------------------------
    # 2. Processo 2ª Instância TJRJ (0029845-67.2026.8.19.0000)
    # ----------------------------------------------------
    logging.info("=== Consultando 2ª Instância (0029845-67.2026.8.19.0000) ===")
    def busca_e_abre_2a(rotulo):
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
        time.sleep(4)
        frame_el = page.wait_for_selector("iframe#mainframe", timeout=20000)
        frame = frame_el.content_frame()
        frame.query_selector("input[name='numeroProcesso']").fill("0029845-67.2026.8.19.0000")
        time.sleep(1)
        btns = frame.query_selector_all("button")
        btn = [b for b in btns if any(w in b.inner_text().lower() for w in ["pesquisar", "buscar", "consultar"])][0]
        btn.click()
        time.sleep(6)

        real_frame = page.query_selector("iframe#mainframe").content_frame()
        links = real_frame.locator("table a")
        n = links.count()
        target = None
        for i in range(n):
            t = links.nth(i).inner_text(timeout=3000)
            if rotulo in t:
                target = i
                break
        if target is None:
            return f"[{rotulo}] link não encontrado na tabela de 2ª instância"

        links.nth(target).click()
        time.sleep(6)
        real_frame = page.query_selector("iframe#mainframe").content_frame()
        try:
            btn_todos = real_frame.locator("button:has-text('Todos Os Movimentos'), a:has-text('Todos Os Movimentos')").first
            btn_todos.click(timeout=6000)
            time.sleep(4)
        except Exception:
            pass
        return real_frame.inner_text("body")

    try:
        logging.info("Consultando HC 2026.059.10770...")
        results["2a_instancia_hc"] = busca_e_abre_2a("2026.059.10770")
    except Exception as e:
        results["2a_instancia_hc"] = f"ERRO HC: {e}"

    try:
        logging.info("Consultando ROC/RHC 2026.141.00580...")
        results["2a_instancia_roc"] = busca_e_abre_2a("2026.141.00580")
    except Exception as e:
        results["2a_instancia_roc"] = f"ERRO ROC: {e}"

    # ----------------------------------------------------
    # 3. DJERJ Novo (consultadje)
    # ----------------------------------------------------
    logging.info("=== Consultando DJERJ Novo (01/08 a 14/08/2026) ===")
    dje_url = (
        "https://www3.tjrj.jus.br/consultadje/Result.aspx"
        "?dtInicio=01%2F08%2F2026"
        "&dtFim=14%2F08%2F2026"
        "&txtPesq=0023013-51.2021.8.19.0078"
        "&tipoPesq=PROC"
    )
    try:
        page.goto(dje_url, wait_until="domcontentloaded", timeout=45000)
        time.sleep(8)
        results["djerj_buzios"] = page.evaluate("document.body.innerText")
    except Exception as e:
        results["djerj_buzios"] = f"ERRO DJERJ: {e}"

    browser.close()

# Salvar relatório consolidado bruto
out_file = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\analises\verificacao_live_14_08_2026.json"
os.makedirs(os.path.dirname(out_file), exist_ok=True)
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

txt_summary_file = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\analises\verificacao_live_14_08_2026.txt"
with open(txt_summary_file, "w", encoding="utf-8") as f:
    for k, v in results.items():
        f.write(f"\n{'='*30} {k.upper()} {'='*30}\n")
        f.write(v)
        f.write("\n\n")

print(f"Verificação concluída com sucesso e gravada em:\n- {out_file}\n- {txt_summary_file}")
