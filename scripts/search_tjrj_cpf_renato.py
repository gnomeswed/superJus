# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

cpf = "12498197761"
nome = "Renato Bastos Rocha"
target_dir = r"c:\Projetos\superJus\Clientes\Renato_Bastos_Rocha"
os.makedirs(target_dir, exist_ok=True)

print(f"=== CONSULTA OFICIAL TJRJ POR CPF: {cpf} ({nome}) ===")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 900}
    )
    page = context.new_page()

    # 1. Portal TJRJ Consulta Processual
    url_portal = "https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica"
    try:
        print("Acessando Portal TJRJ...")
        page.goto(url_portal, wait_until="domcontentloaded", timeout=25000)
        time.sleep(4)

        # Clicar na aba "Por CPF/CNPJ"
        page.evaluate("""() => {
            const tabs = Array.from(document.querySelectorAll('*'));
            const tabCpf = tabs.find(e => e.textContent && e.textContent.trim() === 'Por CPF/CNPJ');
            if (tabCpf) tabCpf.click();
        }""")
        time.sleep(2)

        # Preencher CPF
        cpf_input = page.query_selector("input[formcontrolname='cpfCnpj'], input[placeholder*='CPF'], input[name*='cpf']")
        if not cpf_input:
            # Tentar inputs genéricos
            inputs = page.query_selector_all("input")
            for inp in inputs:
                vis = inp.is_visible()
                if vis:
                    cpf_input = inp
                    break
                    
        if cpf_input:
            cpf_input.fill(cpf)
            print("Campo CPF preenchido.")
            time.sleep(1)

        # Clicar em Pesquisar
        page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const btn = btns.find(b => b.textContent && b.textContent.trim().toLowerCase().includes('pesquisar'));
            if (btn) btn.click();
        }""")
        print("Pesquisa disparada. Aguardando 10 segundos...")
        time.sleep(10)

        page.screenshot(path=os.path.join(target_dir, "tjrj_cpf_resultado.png"))
        txt = page.inner_text("body")
        with open(os.path.join(target_dir, "tjrj_cpf_resultado.txt"), "w", encoding="utf-8") as f:
            f.write(txt)

        print("\nResultado capturado:")
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        for l in lines[:30]:
            print(f"  [TJRJ] {l}")

    except Exception as e:
        print(f"Erro no Portal: {e}")

    # 2. Consulta PJe TJRJ por CPF
    url_pje = "https://tjrj.pje.jus.br/pje/ConsultaPublica/listView.seam"
    try:
        print("\nConsultando PJe TJRJ...")
        page.goto(url_pje, wait_until="domcontentloaded", timeout=25000)
        time.sleep(2)

        inp_cpf_pje = page.query_selector("input[id*='numCpf'], input[id*='CpfCnpj'], input[name*='Cpf']")
        if inp_cpf_pje:
            inp_cpf_pje.fill(cpf)
            time.sleep(1)

        btn_pje = page.query_selector("input[id*='search'], input[value='Pesquisar'], button:has-text('Pesquisar')")
        if btn_pje:
            btn_pje.click()
            time.sleep(6)

        pje_txt = page.inner_text("body")
        page.screenshot(path=os.path.join(target_dir, "pje_cpf_resultado.png"))
        with open(os.path.join(target_dir, "pje_cpf_resultado.txt"), "w", encoding="utf-8") as f:
            f.write(pje_txt)

        print("Resultado PJe capturado:")
        lines_pje = [l.strip() for l in pje_txt.splitlines() if l.strip()]
        for l in lines_pje[:25]:
            print(f"  [PJe] {l}")
    except Exception as e:
        print(f"Erro no PJe: {e}")

    browser.close()

print("\n=== CONSULTA FINALIZADA ===")
