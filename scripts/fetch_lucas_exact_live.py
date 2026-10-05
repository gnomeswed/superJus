# -*- coding: utf-8 -*-
"""
Consulta Exata 2ª Instância - Lucas de Souza Freitas (Lucas Motoboy)
Sem loops de polling (evita detecção de automação)
"""
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

from playwright.sync_api import sync_playwright

OUT_DIR = r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_varredura_01_09_2026"
os.makedirs(OUT_DIR, exist_ok=True)

PROC_CNJ = "0011857-95.2024.8.19.0002"

print(f"=== CONSULTANDO AO VIVO: 2ª INSTÂNCIA DE LUCAS MOTOBOY ({PROC_CNJ}) ===", flush=True)

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

    links = frame.query_selector_all("table a, .table a, tbody tr td a")
    link_2a = None
    for l in links:
        t = l.inner_text().strip()
        if "2026.050" in t or "Segunda" in t or "2ª" in t or "Apelação" in t or "CAMARA" in t:
            link_2a = l
            break
    if not link_2a and len(links) > 1:
        link_2a = links[1]

    if link_2a:
        print(f"Clicando na Apelação (2ª Instância): {link_2a.inner_text().strip()}...", flush=True)
        link_2a.click()
        time.sleep(8)

        # Clicar Todos os Movimentos se existir
        try:
            btn_todos = frame.query_selector("button:has-text('Todos Os Movimentos'), a:has-text('Todos Os Movimentos')")
            if btn_todos:
                btn_todos.click()
                time.sleep(3)
        except Exception:
            pass

        txt_2a = frame.inner_text("body")
        html_2a = frame.evaluate("document.documentElement.outerHTML")
        
        with open(os.path.join(OUT_DIR, "2A_Apelacao_Lucas_01_09_2026.txt"), "w", encoding="utf-8") as f:
            f.write(txt_2a)
        with open(os.path.join(OUT_DIR, "2A_Apelacao_Lucas_01_09_2026.html"), "w", encoding="utf-8") as f:
            f.write(html_2a)
        page.screenshot(path=os.path.join(OUT_DIR, "2A_screenshot_01_09.png"), full_page=True)

        print(f"\n=======================================================")
        print(f"=== RESULTADO CAPTURADO (01/09/2026) ===")
        print(f"=======================================================")
        lines = [l.strip() for l in txt_2a.split('\n') if l.strip()]
        for line in lines:
            print(f"  {line}")

    browser.close()

print("\n=== CONCLUÍDO ===", flush=True)
