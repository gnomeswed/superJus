# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== CONSULTA STJ — HC 1.116.750/RJ (2026/0311210-7) / ROC de origem ===")

target_dir = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(target_dir, exist_ok=True)
lines_out = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1280, "height": 900})
    page = ctx.new_page()

    try:
        page.goto("https://processo.stj.jus.br/processo/pesquisa/?aplicacao=processos.ea&tipoPesquisa=tipoPesquisaGenerica&termo=1116750", wait_until="domcontentloaded", timeout=60000)
        time.sleep(6)
        txt = page.inner_text("body")
        lines_out.append("=== BUSCA STJ POR 1116750 (pagina inicial) ===")
        lines_out.append(txt[:4000])
    except Exception as e:
        lines_out.append(f"Erro busca STJ: {e}")

    # Tentar pela numeração de origem
    try:
        page.goto("https://processo.stj.jus.br/processo/pesquisa/?aplicacao=processos.ea&tipoPesquisa=tipoPesquisaGenerica&termo=00298456720268190000", wait_until="domcontentloaded", timeout=60000)
        time.sleep(6)
        txt2 = page.inner_text("body")
        lines_out.append("\n=== BUSCA STJ POR NUMERO DE ORIGEM ===")
        lines_out.append(txt2[:4000])
    except Exception as e:
        lines_out.append(f"Erro busca origem: {e}")

    browser.close()

res_txt = "\n".join(lines_out)
target_file = os.path.join(target_dir, "stj_hc_roc_check_03_08_2026.txt")
with open(target_file, "w", encoding="utf-8") as f:
    f.write(res_txt)
print("SUCESSO: salvo em " + target_file)
