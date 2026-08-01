# -*- coding: utf-8 -*-
import sys
import os
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

from playwright.sync_api import sync_playwright

target_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(target_dir, exist_ok=True)

clean_num = "00298456720268190000"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    logging.info("Navegando ate o TJRJ...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=40000, wait_until="domcontentloaded")
    time.sleep(3)
    
    iframe_el = page.wait_for_selector("iframe#mainframe", timeout=15000)
    if iframe_el:
        frame = iframe_el.content_frame()
        if frame:
            logging.info("Acessou iframe mainframe.")
            # Procurar todos os inputs do frame
            inputs = frame.query_selector_all("input")
            logging.info(f"Encontrados {len(inputs)} inputs no frame.")
            for idx, inp in enumerate(inputs):
                try:
                    name = inp.get_attribute("name") or ""
                    id_attr = inp.get_attribute("id") or ""
                    placeholder = inp.get_attribute("placeholder") or ""
                    logging.info(f"Input {idx}: id='{id_attr}', name='{name}', placeholder='{placeholder}'")
                except Exception:
                    pass
                    
            # Tentar preencher input unico se houver
            single = frame.query_selector("input#numeroProcesso") or frame.query_selector("input[type='text']")
            if single:
                single.fill("0029845-67.2026.8.19.0000")
                logging.info("Preencheu input com 0029845-67.2026.8.19.0000")
                btn = frame.query_selector("button") or frame.query_selector("input[type='submit']")
                if btn:
                    btn.click()
                    logging.info("Clicou no botão.")
                    time.sleep(5)
                    
            text = frame.inner_text("body")
            out_file = os.path.join(target_dir, "tjrj_live_text.txt")
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(text)
            logging.info(f"Texto salvo em {out_file}. Tamanho: {len(text)}")

    browser.close()
