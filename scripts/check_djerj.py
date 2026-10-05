# -*- coding: utf-8 -*-
import os, sys, time
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

PROCS = [
    "0023013-51.2021.8.19.0078",
    "0029845-67.2026.8.19.0000",
    "0001140-87.2024.8.19.0078",
    "0022975-39.2021.8.19.0078"
]

OUT_DIR = r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\documentos_processo\_varredura_18_08_2026"
os.makedirs(OUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    page = browser.new_page(viewport={"width": 1366, "height": 900})

    print(f"\n==========================================", flush=True)
    print(f"Consultando DJERJ Novo (01/08/2026 a 18/08/2026)", flush=True)
    print(f"==========================================", flush=True)

    for cnj in PROCS:
        dje_url = (
            f"https://www3.tjrj.jus.br/consultadje/Result.aspx"
            f"?dtInicio=01%2F08%2F2026"
            f"&dtFim=18%2F08%2F2026"
            f"&txtPesq={cnj}"
            f"&tipoPesq=PROC"
        )
        try:
            print(f"\n--- DJERJ: {cnj} ---", flush=True)
            page.goto(dje_url, timeout=30000, wait_until="domcontentloaded")
            time.sleep(5)
            txt = page.evaluate("document.body.innerText")
            safe_name = cnj.replace('.', '_').replace('-', '_')
            with open(os.path.join(OUT_DIR, f"DJERJ_{safe_name}.txt"), "w", encoding="utf-8") as f:
                f.write(txt)

            if "Nenhum registro encontrado" in txt or "0 registros" in txt.lower():
                print(f"  • Nenhuma publicação encontrada no período (01/08 a 18/08/2026)", flush=True)
            else:
                print(f"  • PUBLICAÇÃO ENCONTRADA! Chars: {len(txt)}", flush=True)
                for l in [x.strip() for x in txt.split('\n') if x.strip()][:15]:
                    print(f"    > {l[:120]}", flush=True)
        except Exception as e:
            print(f"  • Erro ao consultar DJERJ para {cnj}: {e}", flush=True)

    # Consulta também por nome "Julio Pereira Marcos"
    try:
        print(f"\n--- DJERJ por Nome: Julio Pereira Marcos ---", flush=True)
        dje_url_nome = (
            f"https://www3.tjrj.jus.br/consultadje/Result.aspx"
            f"?dtInicio=01%2F08%2F2026"
            f"&dtFim=18%2F08%2F2026"
            f"&txtPesq=Julio+Pereira+Marcos"
            f"&tipoPesq=NOME"
        )
        page.goto(dje_url_nome, timeout=30000, wait_until="domcontentloaded")
        time.sleep(5)
        txt_nome = page.evaluate("document.body.innerText")
        with open(os.path.join(OUT_DIR, "DJERJ_nome_Julio_Pereira_Marcos.txt"), "w", encoding="utf-8") as f:
            f.write(txt_nome)
        if "Nenhum registro encontrado" in txt_nome:
            print("  • Nenhuma publicação por nome no período.", flush=True)
        else:
            print(f"  • Publicação encontrada por nome! Chars: {len(txt_nome)}", flush=True)
    except Exception as e:
        print(f"  • Erro consulta DJERJ por nome: {e}", flush=True)

    browser.close()
