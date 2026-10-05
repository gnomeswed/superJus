# -*- coding: utf-8 -*-
import os
import sys
import time
import logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
sys.stdout.reconfigure(encoding="utf-8")

processes = [
    ("0023013-51.2021.8.19.0078", "Ação Penal 1ª Instância Búzios"),
    ("0029845-67.2026.8.19.0000", "HC 2ª Instância TJRJ (7ª Câmara)")
]

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
    )
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 850}
    )
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    for proc_num, title in processes:
        logging.info(f"Checking live TJRJ portal for {title} ({proc_num})...")
        try:
            url_portal = "https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica"
            page.goto(url_portal, timeout=30000, wait_until="domcontentloaded")
            time.sleep(3)
            
            iframe_el = page.wait_for_selector("iframe#mainframe", timeout=15000)
            if iframe_el:
                frame = iframe_el.content_frame()
                if frame:
                    inp = frame.query_selector("input[name='numeroProcesso']")
                    if inp:
                        inp.fill(proc_num)
                        btns = frame.query_selector_all("button")
                        btn = None
                        for b in btns:
                            txt = b.inner_text().strip()
                            if any(w in txt.lower() for w in ["pesquisar", "buscar", "consultar"]):
                                btn = b
                                break
                        if not btn and btns:
                            btn = btns[0]
                        if btn:
                            btn.click()
                            time.sleep(5)
                            body_txt = frame.inner_text("body")
                            results[proc_num] = body_txt
        except Exception as e:
            logging.error(f"Erro ao verificar {title}: {e}")
            results[proc_num] = f"Erro: {e}"
            
    browser.close()

out_file = r"c:\Projetos\superJus\julio_verificacao_07_08_2026.txt"
with open(out_file, "w", encoding="utf-8") as f:
    for proc, txt in results.items():
        f.write(f"=== PROCESSO {proc} ===\n{txt}\n\n" + "="*70 + "\n\n")

print(f"Verificação do dia 07/08/2026 concluída! Salvando em {out_file}")
