# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== CHECAGEM DJERJ NOITE — 05/08/2026 (18:10 BRT) ===")

target_file = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\analises_e_automacoes_ia\Consultas_e_Logs_Automacoes\djerj_check_august5_evening.txt"

terms = ["0023013-51.2021.8.19.0078", "00230135120218190078", "JULIO PEREIRA MARCOS", "163342", "203902"]

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()

    try:
        print("Acessando portal de consulta DJERJ...")
        page.goto("https://www3.tjrj.jus.br/consultadjerj/consulta.aspx", wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

        # Look for iframe or main elements
        main_page = page
        if page.query_selector("iframe"):
            frame_el = page.query_selector("iframe")
            main_page = frame_el.content_frame() or page

        for term in terms:
            try:
                print(f"Buscando por: {term}")
                inp = main_page.query_selector("input[id*='txtProcesso'], input[id*='txtTexto'], input[id*='Processo'], input[type='text']")
                if inp:
                    inp.fill("")
                    inp.fill(term)
                    time.sleep(1)
                    btn = main_page.query_selector("input[type='submit'], button:has-text('Pesquisar'), input[value*='Pesquisar']")
                    if btn:
                        btn.click()
                        time.sleep(4)
                        txt = main_page.evaluate("document.body.innerText")
                        results.append(f"=== TERMO: {term} ===\n{txt[:2000]}\n")
            except Exception as e:
                results.append(f"Erro ao buscar {term}: {e}")

    except Exception as e:
        results.append(f"Erro geral no portal DJERJ: {e}")

    browser.close()

res_str = "\n".join(results)
with open(target_file, "w", encoding="utf-8") as f:
    f.write(res_str)

print("SUCESSO: Busca concluída. Resultados salvos em " + target_file)
