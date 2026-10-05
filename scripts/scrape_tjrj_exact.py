# -*- coding: utf-8 -*-
import sys
import os
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

from playwright.sync_api import sync_playwright

target_dir = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(target_dir, exist_ok=True)

processes = [
    ("0029845-67.2026.8.19.0000", "Habeas Corpus 7ª Câmara"),
    ("0023013-51.2021.8.19.0078", "Ação Penal 2ª Vara Búzios")
]

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    for proc_num, label in processes:
        logging.info(f"Acessando TJRJ para {label} ({proc_num})...")
        try:
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=30000, wait_until="domcontentloaded")
            time.sleep(3)
            
            iframe_el = page.wait_for_selector("iframe#mainframe", timeout=15000)
            if iframe_el:
                frame = iframe_el.content_frame()
                if frame:
                    inp = frame.query_selector("input[name='numeroProcesso']")
                    if inp:
                        inp.fill(proc_num)
                        logging.info("Preencheu número do processo.")
                        
                        # Buscar botão Pesquisar dentro de form ou por texto
                        btns = frame.query_selector_all("button")
                        target_btn = None
                        for b in btns:
                            txt = b.inner_text().strip()
                            if "pesquisar" in txt.lower() or "buscar" in txt.lower() or "consultar" in txt.lower():
                                target_btn = b
                                break
                        if not target_btn and btns:
                            target_btn = btns[0]
                            
                        if target_btn:
                            target_btn.click()
                            logging.info("Clicou no botão de pesquisa. Aguardando...")
                            time.sleep(6)
                            
                            page_text = frame.inner_text("body")
                            results.append(f"## {label} (`{proc_num}`)\n```text\n{page_text[:3000]}\n```\n")
                        else:
                            results.append(f"## {label} (`{proc_num}`)\nBotão não localizado.\n")
                    else:
                        results.append(f"## {label} (`{proc_num}`)\nInput name=numeroProcesso não localizado.\n")
        except Exception as e:
            results.append(f"## {label} (`{proc_num}`)\nErro: {e}\n")
            
    browser.close()

out_file = os.path.join(target_dir, "andamento_hoje_real.md")
with open(out_file, "w", encoding="utf-8") as f:
    f.write("# ANDAMENTOS CAPTURADOS NO TJRJ — HOJE (24/07/2026)\n\n" + "\n".join(results))

print(f"Sucesso! Relatório salvo em {out_file}")
