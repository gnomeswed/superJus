# -*- coding: utf-8 -*-
import time
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

proc_fmt = "0827233-23.2026.8.19.0001"
cpf_fmt = "059.830.127-54"

print("=" * 80)
print(f"CONSULTA AO VIVO PJe 1G TJRJ — 26/09/2026 — LEANDRO DA SILVA")
print(f"Processo: {proc_fmt} | CPF: {cpf_fmt}")
print("=" * 80)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-blink-features=AutomationControlled'])
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    page.on("dialog", lambda dialog: (print(f"Dialog interceptado: {dialog.message}"), dialog.accept()))

    print("1. Acessando Consulta Pública do PJe...")
    page.goto("https://tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam", wait_until="commit", timeout=60000)
    page.wait_for_selector("#fPP\\:searchProcessos", timeout=45000)
    print("2. Página carregada com sucesso!")

    # Inserir número do processo
    print(f"3. Inserindo número do processo {proc_fmt}...")
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

    print("4. Clicando em Pesquisar...")
    page.click("#fPP\\:searchProcessos")
    time.sleep(8)

    # Pegar texto da tabela de resultados
    txt_res = page.inner_text("#fPP\\:processosTable")
    print(f"--- RESUMO DA BUSCA ---\n{txt_res}\n-----------------------")

    # Localizar link de detalhes
    proc_link = page.locator(f"a:has-text('{proc_fmt}')").first
    if not proc_link.is_visible():
        print("Buscando por texto 'VER DETALHES'...")
        proc_link = page.locator("a:has-text('VER DETALHES')").first

    if proc_link.is_visible():
        print("✓ Abrindo autos digitais detalhados...")
        with context.expect_page(timeout=25000) as new_page_info:
            proc_link.click()
        dp = new_page_info.value
        dp.wait_for_load_state("domcontentloaded", timeout=25000)
        time.sleep(5)

        detalhes_txt = dp.inner_text("body")
        out_f = r"c:\Projetos\superJus\Clientes\Leandro_Mecanico\detalhes_pje_leandro_live_26_09_2026.txt"
        with open(out_f, "w", encoding="utf-8") as f:
            f.write(detalhes_txt)
        print(f"✅ Espelho atualizado salvo em: {out_f}")

        # Identificar documentos juntados e verificar se há novas decisões
        print("\n--- MOVIMENTAÇÕES E DOCUMENTOS RECENTES NO PJe ---")
        lines = [l.strip() for l in detalhes_txt.splitlines() if l.strip()]
        for l in lines[120:220]:
            print(f"  • {l}")

        # Verificar se há despacho ou decisão posterior a 09/09/2026
        doc_links = dp.locator("a:has-text('VISUALIZAR DOCUMENTOS')").all()
        print(f"\nTotal de atos judiciais com documentos visualizáveis: {len(doc_links)}")
        if len(doc_links) > 0:
            print("Abrindo o ato mais recente para extrair o inteiro teor...")
            try:
                with context.expect_page(timeout=10000) as doc_page_info:
                    doc_links[0].click()
                doc_p = doc_page_info.value
                doc_p.wait_for_load_state("domcontentloaded", timeout=15000)
                time.sleep(4)
                txt_doc = doc_p.inner_text("body")
                out_doc = r"c:\Projetos\superJus\Clientes\Leandro_Mecanico\ultimo_ato_pje_26_09_2026.txt"
                with open(out_doc, "w", encoding="utf-8") as f:
                    f.write(txt_doc)
                print(f"✅ Inteiro teor do último ato salvo em: {out_doc}")
                print("\n--- TEOR DO ATO MAIS RECENTE ---")
                print(txt_doc[:1500])
            except Exception as e:
                print(f"Aviso ao abrir ato mais recente: {e}")
    else:
        print("⚠️ Link de detalhes não encontrado.")

    browser.close()

print("\n=== CONSULTA FINALIZADA COM SUCESSO ===")
