# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== SCRAPING PJe CONSULTA PÚBLICA SEM LOGIN — LEANDRO MECÂNICO ===")

target_dir = r"c:\Projetos\superJus\Clientes\Leandro_Mecanico\scraping_2026-08-16"
os.makedirs(target_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    page = context.new_page()

    # URL oficial de consulta pública do PJe TJRJ
    url_pje_pub = "https://tjrj.pje.jus.br/pje/ConsultaPublica/listView.seam"
    print(f"1. Acessando {url_pje_pub}...")

    try:
        page.goto(url_pje_pub, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

        # Tirar screenshot inicial
        ss1 = os.path.join(target_dir, "pje_consulta_publica_home.png")
        page.screenshot(path=ss1)
        print(f"   • Screenshot inicial salvo: {ss1}")

        # Tentar preencher o número do processo
        # No PJe, o número é dividido em num_sequencial, digito_verificador, ano, ramo_justica, tribunal, orgao_jurisdicional
        # 0827233-23.2026.8.19.0001 -> 0827233 - 23 . 2026 . 8 . 19 . 0001
        try:
            page.fill("input[id*='numSequencial']", "0827233")
            page.fill("input[id*='numDigitoVerificador']", "23")
            page.fill("input[id*='ano']", "2026")
            page.fill("input[id*='ramoJustica']", "8")
            page.fill("input[id*='respectivoTribunal']", "19")
            page.fill("input[id*='orgaoJurisdicional']", "0001")
            print("   • Número do processo 0827233-23.2026.8.19.0001 preenchido!")
        except Exception as e:
            print(f"   • Campo individual não encontrado, tentando campo único: {e}")
            try:
                page.fill("input[type='text']", "0827233-23.2026.8.19.0001")
            except Exception:
                pass

        time.sleep(1)
        # Clicar em Pesquisar
        try:
            page.click("input[id*='search'], button[id*='search'], input[value='Pesquisar'], button:has-text('Pesquisar')")
            print("   • Botão Pesquisar clicado!")
        except Exception as e:
            print(f"   • Erro ao clicar pesquisar: {e}")

        time.sleep(5)

        # Capturar resultado
        txt = page.inner_text("body")
        ss2 = os.path.join(target_dir, "pje_consulta_publica_resultado.png")
        page.screenshot(path=ss2)
        print(f"   • Screenshot do resultado salvo: {ss2}")

        out_txt = os.path.join(target_dir, "resultado_pje_consulta_publica_leandro.txt")
        with open(out_txt, "w", encoding="utf-8") as f:
            f.write(txt)

        print(f"✅ Resultado em texto salvo: {out_txt}")

        print("\n--- CONTEÚDO EXTRAÍDO DA CONSULTA PÚBLICA PJe ---")
        lines = [l.strip() for l in txt.split('\n') if l.strip()]
        for l in lines[:30]:
            print(f"  • {l[:120]}")

    except Exception as e:
        print(f"Erro na consulta pública do PJe: {e}")

    browser.close()

print("\n=== CONSULTA PÚBLICA PJe CONCLUÍDA ===")
