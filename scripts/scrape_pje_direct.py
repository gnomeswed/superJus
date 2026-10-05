# -*- coding: utf-8 -*-
import time
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

proc_fmt = "0827233-23.2026.8.19.0001"
cpf = "05983012754"
cpf_fmt = "059.830.127-54"

print("=" * 80)
print(f"CONSULTA PJe 1G TJRJ AO VIVO: {proc_fmt} / CPF {cpf_fmt}")
print("=" * 80)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-blink-features=AutomationControlled'])
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    page.on("dialog", lambda dialog: (print(f"Dialog: {dialog.message}"), dialog.accept()))

    print("1. Abrindo listView.seam...")
    page.goto("https://tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam", wait_until="commit", timeout=60000)
    page.wait_for_selector("#fPP\\:searchProcessos", timeout=45000)
    print("2. Página carregada com sucesso!")

    # Preencher input via evaluate com jquery mask para garantir integridade
    print("3. Inserindo número do processo via DOM...")
    page.evaluate(f"""() => {{
        var inp = document.getElementById('fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso');
        if (inp) {{
            inp.value = '{proc_fmt}';
            inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
            inp.dispatchEvent(new Event('change', {{ bubbles: true }}));
            inp.dispatchEvent(new Event('blur', {{ bubbles: true }}));
        }}
    }}""")
    time.sleep(1)

    print("4. Clicando no botão Pesquisar...")
    # Clicar no botão
    page.click("#fPP\\:searchProcessos")

    print("5. Aguardando requisição AJAX do Richfaces...")
    time.sleep(8)

    # Verificar tabela de resultados
    html_res = page.inner_html("#fPP\\:processosTable")
    txt_res = page.inner_text("#fPP\\:processosTable")
    print(f"Resultado tabela ({len(txt_res)} chars):\n{txt_res}")

    # Checar se há links de processos encontrados
    links = page.locator("a[id*='processosTable']").all()
    print(f"Links encontrados na tabela: {len(links)}")

    if len(links) == 0:
        print("\nTentando busca alternativa por CPF no formulário...")
        page.evaluate(f"""() => {{
            var inpProc = document.getElementById('fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso');
            if (inpProc) inpProc.value = '';
            var inpCpf = document.getElementById('fPP:dpDec:documentoParte');
            if (inpCpf) {{
                inpCpf.value = '{cpf_fmt}';
                inpCpf.dispatchEvent(new Event('input', {{ bubbles: true }}));
                inpCpf.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        }}""")
        time.sleep(1)
        page.click("#fPP\\:searchProcessos")
        time.sleep(8)
        txt_res_cpf = page.inner_text("#fPP\\:processosTable")
        print(f"Resultado busca CPF:\n{txt_res_cpf}")
        links = page.locator("a[id*='processosTable']").all()

    # Se encontrar o processo, clicar para abrir a janela de detalhes
    proc_link = page.locator(f"a:has-text('{proc_fmt}')").first
    if proc_link.is_visible():
        print("✓ Link do processo visível! Abrindo detalhes...")
        with context.expect_page(timeout=20000) as new_page_info:
            proc_link.click()
        dp = new_page_info.value
        dp.wait_for_load_state("domcontentloaded", timeout=20000)
        time.sleep(4)
        detalhes_txt = dp.inner_text("body")
        out_f = r"c:\Projetos\superJus\Clientes\Leandro_Mecanico\detalhes_pje_leandro_live_18_09_2026.txt"
        with open(out_f, "w", encoding="utf-8") as f:
            f.write(detalhes_txt)
        print(f"✅ Detalhes salvos em: {out_f}")
        for l in [x.strip() for x in detalhes_txt.splitlines() if x.strip()][:50]:
            print(f"  • {l}")
    else:
        print("Aviso: Link específico não abriu automaticamente.")

    browser.close()

print("=== FIM ===")
