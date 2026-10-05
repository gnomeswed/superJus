# -*- coding: utf-8 -*-
import time
import sys
import os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

proc_fmt = "0808595-36.2026.8.19.0002"

print("=" * 80)
print(f"CONSULTA AO VIVO PJe 1G TJRJ — 05/10/2026 — LUCAS DIAS OLIVEIRA (TAXISTA)")
print(f"Processo: {proc_fmt}")
print("=" * 80)

output_dir = r"c:\Projetos\superJus\Clientes\Lucas_Dias_Oliveira\03_Documentos_do_Processo"
os.makedirs(output_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-blink-features=AutomationControlled'])
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    page.on("dialog", lambda dialog: (print(f"Dialog: {dialog.message}"), dialog.accept()))

    print("1. Acessando Consulta Pública do PJe...")
    try:
        page.goto("https://tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam", wait_until="commit", timeout=60000)
        page.wait_for_selector("#fPP\\:searchProcessos", timeout=45000)
        print("2. Página de Consulta Pública carregada com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar página: {e}")
        browser.close()
        sys.exit(1)

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
    time.sleep(2)

    print("4. Clicando em Pesquisar...")
    page.click("#fPP\\:searchProcessos")
    
    print("5. Aguardando retorno da busca...")
    try:
        page.wait_for_selector("a:has-text('0808595'), a:has-text('VER DETALHES')", timeout=35000)
        txt_res = page.inner_text("#fPP\\:processosTable")
        print(f"--- RESUMO DA BUSCA NO PJe ---\n{txt_res}\n-----------------------")
        
        proc_link = page.locator("a:has-text('0808595'), a:has-text('VER DETALHES')").first
        print("✓ Link de detalhes localizado! Abrindo autos digitais...")
        
        with context.expect_page(timeout=25000) as new_page_info:
            proc_link.click()
        dp = new_page_info.value
        dp.wait_for_load_state("domcontentloaded", timeout=25000)
        time.sleep(5)

        detalhes_txt = dp.inner_text("body")
        out_f = os.path.join(output_dir, "detalhes_pje_lucas_taxista_live_05_10_2026.txt")
        with open(out_f, "w", encoding="utf-8") as f:
            f.write(detalhes_txt)
        print(f"✅ Espelho atualizado salvo em: {out_f}")

        # Extrair todas as movimentações
        print("\n--- MOVIMENTAÇÕES E DOCUMENTOS RECENTES NO PJe (05/10/2026) ---")
        lines = [l.strip() for l in detalhes_txt.splitlines() if l.strip()]
        
        # Localizar bloco de movimentações
        idx = -1
        for i, l in enumerate(lines):
            if "Movimentações do Processo" in l:
                idx = i
                break
        if idx != -1:
            for l in lines[idx:idx+45]:
                print(f"  • {l}")
        else:
            for l in lines[100:160]:
                print(f"  • {l}")

        # Verificar se há despacho ou decisão recente posterior a 14/09
        doc_links = dp.locator("a:has-text('VISUALIZAR DOCUMENTOS')").all()
        print(f"\nTotal de atos judiciais com documentos visualizáveis: {len(doc_links)}")
        if len(doc_links) > 0:
            print("Abrindo o ato judicial mais recente para verificar se é novo...")
            try:
                with context.expect_page(timeout=10000) as doc_page_info:
                    doc_links[0].click()
                doc_p = doc_page_info.value
                doc_p.wait_for_load_state("domcontentloaded", timeout=15000)
                time.sleep(4)
                txt_doc = doc_p.inner_text("body")
                out_doc = os.path.join(output_dir, "ultimo_ato_pje_lucas_taxista_05_10_2026.txt")
                with open(out_doc, "w", encoding="utf-8") as f:
                    f.write(txt_doc)
                print(f"✅ Inteiro teor do último ato salvo em: {out_doc}")
                print("\n--- CABEÇALHO DO ATO JUDICIAL MAIS RECENTE ---")
                print(txt_doc[:600])
            except Exception as e:
                print(f"Aviso ao abrir ato mais recente: {e}")

    except Exception as e:
        print("Erro / Timeout durante a consulta:", e)
        page.screenshot(path="scratch_pje_05out.png")

    browser.close()

print("\n=== CONSULTA 05/10/2026 FINALIZADA COM SUCESSO ===")
