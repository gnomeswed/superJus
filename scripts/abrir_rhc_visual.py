# -*- coding: utf-8 -*-
"""Capturar tela completa do RHC com todos os movimentos."""
import os, sys, time, json, logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
sys.stdout.reconfigure(encoding="utf-8")
os.environ["PYTHONIOENCODING"] = "utf-8"

PROC = "0029845-67.2026.8.19.0000"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 850},
    )
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
    time.sleep(3)
    iframe_el = page.wait_for_selector("iframe#mainframe", timeout=20000)
    frame = iframe_el.content_frame()

    inp = frame.query_selector("input[name='numeroProcesso']")
    inp.fill(PROC)
    btns = frame.query_selector_all("button")
    btn = None
    for b in btns:
        if "pesquisar" in b.inner_text().lower():
            btn = b; break
    if not btn and btns: btn = btns[0]
    btn.click()
    time.sleep(6)

    # Clicar no RHC
    frame.evaluate("""() => {
        const links = document.querySelectorAll('a');
        for (const a of links) {
            if (a.innerText.includes('2026.141.00580')) {
                a.click();
                return 'OK';
            }
        }
        return 'NAO';
    }""")
    time.sleep(6)

    # Capturar TELA COMPLETA
    body = frame.inner_text("body")
    out_file = r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\analises\rhc_tela_11_08_2026.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"[OK] Tela do RHC salva ({len(body)} chars)")

    # Voltar e abrir o HC (2026.059.10770)
    frame.evaluate("""() => {
        const links = document.querySelectorAll('a');
        for (const a of links) {
            if (a.innerText.includes('2026.059.10770')) {
                a.click();
                return 'OK';
            }
        }
        return 'NAO';
    }""")
    time.sleep(6)
    body_hc = frame.inner_text("body")
    out_file_hc = r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\analises\hc_tela_11_08_2026.txt"
    with open(out_file_hc, "w", encoding="utf-8") as f:
        f.write(body_hc)
    print(f"[OK] Tela do HC salva ({len(body_hc)} chars)")
    print("\n=== TELA DO HC ===")
    print(body_hc[:3000])

    browser.close()