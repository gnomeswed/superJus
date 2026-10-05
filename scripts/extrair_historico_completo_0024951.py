# -*- coding: utf-8 -*-
"""
Extração de TODAS as páginas de movimentação do processo 0024951-89.2019.8.19.0001
"""
import os
import sys
import time
import json

sys.stdout.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

from playwright.sync_api import sync_playwright

OUT_DIR = r"C:\Projetos\superJus\Clientes\Lucas_Freitas\05_Processos_Anteriores\Processos_2019"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1366, "height": 900}, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = ctx.new_page()

    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
    time.sleep(4)
    iframe_el = page.wait_for_selector("iframe#mainframe", timeout=25000)
    fr = iframe_el.content_frame()

    inp = fr.wait_for_selector("input[name='numeroProcesso']", timeout=15000)
    inp.fill("0024951-89.2019.8.19.0001")
    time.sleep(1)

    btns = fr.query_selector_all("button")
    btn_pesq = next((b for b in btns if any(w in b.inner_text().lower() for w in ["pesquisar", "buscar", "consultar"])), btns[0] if btns else None)
    if btn_pesq:
        btn_pesq.click()
    time.sleep(7)

    # Entrar no processo se houver tabela
    links = fr.query_selector_all("table a, .table a, tbody tr td a")
    if len(links) > 0:
        links[0].click()
        time.sleep(6)

    try:
        btn_all = fr.query_selector("button:has-text('Todos Os Movimentos'), a:has-text('Todos Os Movimentos')")
        if btn_all:
            btn_all.click()
            time.sleep(5)
    except Exception:
        pass

    # Coletar todas as páginas de movimentação
    all_pages_text = []
    page_num = 1
    while True:
        body_p = fr.inner_text("body")
        all_pages_text.append(f"\n{'='*50}\n=== PÁGINA {page_num} ===\n{'='*50}\n" + body_p)
        print(f"Página {page_num} capturada. Chars: {len(body_p)}", flush=True)

        # Tentar ir para a próxima página
        next_btn = fr.query_selector("a:has-text('>'), button:has-text('>'), .pagination .next a, a[aria-label='Next']")
        # Ou botões numéricos
        pagination_links = fr.query_selector_all(".pagination a, ul.pagination li a, a.page-link")
        has_next = False
        for pl in pagination_links:
            t = pl.inner_text().strip()
            if t == str(page_num + 1):
                pl.click()
                time.sleep(4)
                page_num += 1
                has_next = True
                break
        if not has_next:
            break
        if page_num > 15:
            break

    full_history = "\n".join(all_pages_text)
    with open(os.path.join(OUT_DIR, "historico_completo_todas_paginas_0024951.txt"), "w", encoding="utf-8") as f:
        f.write(full_history)

    print(f"\nTotal de páginas extraídas: {len(all_pages_text)}")
    browser.close()
