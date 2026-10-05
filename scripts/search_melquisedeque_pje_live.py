# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

nome = "Melquisedeque Rodrigues dos Santos"
cpf = "064.296.507-23"
cpf_clean = "06429650723"

print(f"=== INICIANDO SCRAPING PLAYWRIGHT TJRJ & PJe: {nome} ===")

target_dir = r"c:\Projetos\superJus\Clientes\Melquisedeque"
os.makedirs(target_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    # ----------------------------------------------------
    # 1. CONSULTA PÚBLICA PJe TJRJ
    # ----------------------------------------------------
    url_pje = "https://tjrj.pje.jus.br/pje/ConsultaPublica/listView.seam"
    print(f"\n1. Acessando PJe TJRJ: {url_pje}...")
    try:
        page.goto(url_pje, wait_until="domcontentloaded", timeout=25000)
        time.sleep(3)

        # Preencher Nome da Parte
        nome_inputs = page.query_selector_all("input[id*='nomeParte'], input[id*='NomeParte'], input[placeholder*='Nome']")
        if nome_inputs:
            nome_inputs[0].fill(nome)
            print(f"   • Nome preenchido no PJe: {nome}")
        else:
            # Tentar preencher CPF
            cpf_inputs = page.query_selector_all("input[id*='CPF'], input[id*='cpf'], input[id*='documento']")
            if cpf_inputs:
                cpf_inputs[0].fill(cpf_clean)
                print(f"   • CPF preenchido no PJe: {cpf_clean}")

        time.sleep(1)
        # Clicar em pesquisar
        btn = page.query_selector("input[id*='search'], button[id*='search'], input[value*='Pesquisar'], button:has-text('Pesquisar')")
        if btn:
            btn.click()
            print("   • Botão Pesquisar PJe acionado.")
            time.sleep(6)
            
            pje_txt = page.inner_text("body")
            ss_pje = os.path.join(target_dir, "resultado_pje_melquisedeque.png")
            page.screenshot(path=ss_pje)
            
            with open(os.path.join(target_dir, "resultado_pje_melquisedeque.txt"), "w", encoding="utf-8") as f:
                f.write(pje_txt)
                
            print(f"   • Captura PJe realizada! Screenshot: {ss_pje}")
            for l in [line.strip() for line in pje_txt.splitlines() if line.strip()][:25]:
                print(f"     [PJe] {l[:120]}")
    except Exception as e:
        print(f"   ❌ Erro no PJe: {e}")

    # ----------------------------------------------------
    # 2. CONSULTA PORTAL TJRJ (1ª INSTÂNCIA - CAPITAL)
    # ----------------------------------------------------
    url_portal = "http://www4.tjrj.jus.br/consultaProcessoWebV2/consultaPorNome.do"
    print(f"\n2. Acessando Portal TJRJ por Nome: {url_portal}...")
    try:
        page.goto(url_portal, wait_until="domcontentloaded", timeout=25000)
        time.sleep(2)
        
        # Preencher nome
        inp_nome = page.query_selector("input[name='nomeParte'], input[id='nomeParte'], input[type='text']")
        if inp_nome:
            inp_nome.fill(nome)
            print(f"   • Nome preenchido no Portal TJRJ: {nome}")
            
            # Clicar pesquisar
            btn_port = page.query_selector("input[type='submit'], button[type='submit'], input[value*='Pesquisar']")
            if btn_port:
                btn_port.click()
                print("   • Pesquisa Portal TJRJ submetida.")
                time.sleep(5)
                
                portal_txt = page.inner_text("body")
                ss_port = os.path.join(target_dir, "resultado_portal_tjrj_melquisedeque.png")
                page.screenshot(path=ss_port)
                
                with open(os.path.join(target_dir, "resultado_portal_tjrj_melquisedeque.txt"), "w", encoding="utf-8") as f:
                    f.write(portal_txt)
                    
                print(f"   • Captura Portal TJRJ realizada! Screenshot: {ss_port}")
                for l in [line.strip() for line in portal_txt.splitlines() if line.strip()][:30]:
                    print(f"     [Portal TJRJ] {l[:120]}")
    except Exception as e:
        print(f"   ❌ Erro no Portal TJRJ: {e}")

    browser.close()

print("\n=== SCRAPING CONCLUÍDO ===")
