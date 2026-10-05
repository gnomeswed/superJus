# -*- coding: utf-8 -*-
import sys
import os
import time
import logging
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

target_dir = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(target_dir, exist_ok=True)

processes = [
    ("0029845-67.2026.8.19.0000", "HC 7ª Câmara Criminal TJRJ"),
    ("0023013-51.2021.8.19.0078", "2ª Vara de Búzios (Desmembrado)"),
    ("0022975-39.2021.8.19.0078", "Processo Principal Búzios"),
    ("0001492-25.2016.8.19.0046", "Processo Antigo Rio Bonito")
]

results = []

if sync_playwright:
    logging.info("Iniciando Playwright venv para consultar TJRJ live...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        
        for proc_num, label in processes:
            logging.info(f"Buscando {label} ({proc_num})...")
            try:
                page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=30000, wait_until="domcontentloaded")
                time.sleep(2)
                
                iframe_el = page.query_selector("iframe#mainframe")
                if iframe_el:
                    frame = iframe_el.content_frame()
                    if frame:
                        # Preencher busca
                        input_el = frame.query_selector("input#numeroProcesso") or frame.query_selector("input[formcontrolname='numeroProcesso']") or frame.query_selector("input[placeholder*='processo' i]")
                        if input_el:
                            input_el.fill(proc_num)
                            search_btn = frame.query_selector("button:has-text('Pesquisar')") or frame.query_selector("input[value='Pesquisar']") or frame.query_selector("button.btn-primary")
                            if search_btn:
                                search_btn.click()
                                time.sleep(4)
                                
                                content_text = frame.inner_text("body") if frame.query_selector("body") else ""
                                results.append(f"### {label} (`{proc_num}`)\n```\n{content_text[:1500]}\n```\n")
                            else:
                                results.append(f"### {label} (`{proc_num}`)\n- Botão de busca não localizado.\n")
                        else:
                            results.append(f"### {label} (`{proc_num}`)\n- Campo de texto de busca não localizado.\n")
                else:
                    results.append(f"### {label} (`{proc_num}`)\n- Mainframe não encontrado.\n")
            except Exception as e:
                results.append(f"### {label} (`{proc_num}`)\n- Erro Playwright: {e}\n")
        
        browser.close()
else:
    results.append("Playwright não disponível.")

output_md = os.path.join(target_dir, "andamento_hoje_24_07_2026.md")
with open(output_md, "w", encoding="utf-8") as f:
    f.write("# CONSULTA TJRJ EM TEMPO REAL — HOJE (24/07/2026)\n\n" + "\n".join(results))

print(f"Finalizado. Relatório salvo em {output_md}")
