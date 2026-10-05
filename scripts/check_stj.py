# -*- coding: utf-8 -*-
import os, sys, time, json
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

STJ_REG_URL = "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo=202603112107&totalRegistrosPorPagina=40&aplicacao=processos.ea"
OUT_DIR = r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\documentos_processo\_varredura_18_08_2026"
os.makedirs(OUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    page = browser.new_page(viewport={"width": 1366, "height": 900}, locale="pt-BR")

    print(f"\n==========================================", flush=True)
    print(f"Consultando STJ - HC 1.116.750 / RJ (Registro 2026/0311210-7)", flush=True)
    print(f"==========================================", flush=True)

    page.goto(STJ_REG_URL, timeout=35000, wait_until="domcontentloaded")
    time.sleep(5)

    body_txt = page.evaluate("document.body.innerText")
    with open(os.path.join(OUT_DIR, "STJ_HC1116750_principal.txt"), "w", encoding="utf-8") as f:
        f.write(body_txt)

    # Extrai abas de Fases e Decisões
    for tab in ["Fases", "Decisões", "Petições"]:
        try:
            print(f"\n--- STJ Aba: {tab} ---", flush=True)
            page.evaluate(f"""(name) => {{
                const el = Array.from(document.querySelectorAll('a, button, li, span')).find(e => (e.textContent||'').trim().toLowerCase() === name.toLowerCase() && e.offsetWidth > 0);
                if(el) el.click();
            }}""", tab)
            time.sleep(4)
            tab_txt = page.evaluate("document.body.innerText")
            with open(os.path.join(OUT_DIR, f"STJ_HC1116750_aba_{tab}.txt"), "w", encoding="utf-8") as f:
                f.write(tab_txt)

            lines = [l.strip() for l in tab_txt.split('\n') if l.strip()]
            for l in lines[:20]:
                print(f"  > {l[:120]}", flush=True)
        except Exception as e:
            print(f"  • Erro ao abrir aba {tab}: {e}", flush=True)

    browser.close()
