# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== CHECAGEM DJERJ AO VIVO — 05/08/2026 (15:05 BRT) ===")

target_file = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\analises_e_automacoes_ia\Consultas_e_Logs_Automacoes\djerj_check_august5.txt"

terms = ["0023013-51.2021.8.19.0078", "00230135120218190078", "JULIO PEREIRA MARCOS", "163342"]

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()

    # 1. Acessar portal de consulta do DJERJ
    try:
        print("Acessando portal de consulta do DJERJ...")
        page.goto("https://www3.tjrj.jus.br/consultadjerj/consulta.aspx", wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

        for term in terms:
            try:
                print(f"Buscando por: {term}")
                inp = page.query_selector("input[id*='txtProcesso'], input[id*='txtTexto'], input[id*='Processo'], input[type='text']")
                if inp:
                    inp.fill("")
                    inp.fill(term)
                    time.sleep(1)
                    btn = page.query_selector("input[type='submit'], button:has-text('Pesquisar'), input[value*='Pesquisar']")
                    if btn:
                        btn.click()
                        time.sleep(4)
                        txt = page.inner_text("body")
                        results.append(f"=== TERMO: {term} ===\n{txt[:1500]}\n")
            except Exception as e:
                results.append(f"Erro ao buscar {term}: {e}")

    except Exception as e:
        results.append(f"Erro geral no portal DJERJ: {e}")

    browser.close()

res_str = "\n".join(results)
with open(target_file, "w", encoding="utf-8") as f:
    f.write(res_str)

print("SUCESSO: Busca concluída. Resultados salvos em " + target_file)
