# -*- coding: utf-8 -*-
import sys, time, json, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

proc_fmt = "0821248-17.2025.8.19.0031"
print(f"🏛️ CONSULTA PJe 1G TJRJ AO VIVO — PROCESSO {proc_fmt} (RENAN RODRIGUES DE SOUZA)")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
    )
    ctx = browser.new_context(
        viewport={"width": 1400, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()
    page.on("dialog", lambda dialog: (print(f"Dialog: {dialog.message}"), dialog.accept()))

    url = "https://tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam"
    print(f"1. Acessando {url} com wait_until='commit'...")
    try:
        page.goto(url, timeout=60000, wait_until="commit")
        print("2. Aguardando seletor do botão pesquisar...")
        page.wait_for_selector("#fPP\\:searchProcessos", timeout=45000)
        print("3. Página carregada com sucesso!")

        print("4. Preenchendo número do processo via DOM...")
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

        print("5. Clicando em Pesquisar...")
        page.click("#fPP\\:searchProcessos")
        print("6. Aguardando resposta AJAX...")
        time.sleep(8)

        # Checar se encontrou o processo na tabela
        link_detalhes = page.locator(f"a:has-text('{proc_fmt}')").first
        if link_detalhes.is_visible():
            print("✓ Link de detalhes do processo localizado! Abrindo autos digitais...")
            with ctx.expect_page(timeout=25000) as new_page_info:
                link_detalhes.click()

            dp = new_page_info.value
            dp.wait_for_load_state("domcontentloaded", timeout=25000)
            time.sleep(4)

            txt_detalhes = dp.inner_text("body")
            out_dir = r"c:\Projetos\superJus\Clientes\Renan\03_Documentos_do_Processo"
            os.makedirs(out_dir, exist_ok=True)
            out_txt = os.path.join(out_dir, "detalhes_pje_renan_live_latest.txt")
            with open(out_txt, "w", encoding="utf-8") as f:
                f.write(txt_detalhes)
            print(f"✅ Detalhes salvos com sucesso em: {out_txt}")

            print("\n=== DADOS CAPTURADOS DO PJe ===")
            for line in txt_detalhes.splitlines():
                l = line.strip()
                if any(k in l.upper() for k in ["RÉU", "AUTOR", "ADVOGADO", "PARTICIPANTE", "POLO", "ASSUNTO", "CLASSE", "DISTRIBUIÇÃO"]):
                    print(f"  • {l}")

            print("\n=== ÚLTIMAS MOVIMENTAÇÕES NO PJe ===")
            mov_lines = []
            capture = False
            for line in txt_detalhes.splitlines():
                l = line.strip()
                if "Movimentações do Processo" in l:
                    capture = True
                    continue
                if "Documentos juntados ao processo" in l:
                    capture = False
                if capture and l:
                    mov_lines.append(l)
            for ml in mov_lines[:25]:
                print(f"  {ml}")

            print("\n=== DOCUMENTOS JUNTADOS NO PJe ===")
            doc_lines = []
            cap_doc = False
            for line in txt_detalhes.splitlines():
                l = line.strip()
                if "Documentos juntados ao processo" in l:
                    cap_doc = True
                    continue
                if cap_doc and l:
                    doc_lines.append(l)
            for dl in doc_lines[:25]:
                print(f"  📄 {dl}")

        else:
            print("⚠️ Link de detalhes não encontrado diretamente na tabela.")
            body_txt = page.inner_text("body")
            print(body_txt[:1000])

    except Exception as e:
        print(f"❌ Erro durante consulta: {e}")
    finally:
        browser.close()
