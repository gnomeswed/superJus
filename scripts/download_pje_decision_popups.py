# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

target_dir = r"c:\Projetos\superJus\Clientes\Melquisedeque\processos\0807644-58.2025.8.19.0202\documentos"
os.makedirs(target_dir, exist_ok=True)

print("=== BAIXANDO O CONTEÚDO INTEGRAL DAS DECISÕES E DA ATA DE AUDIÊNCIA DO PJe ===")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    url_pje = "https://tjrj.pje.jus.br/pje/ConsultaPublica/listView.seam"
    page.goto(url_pje, wait_until="domcontentloaded", timeout=30000)
    time.sleep(2)

    # Preencher nome
    page.fill("input[id*='nomeParte']", "Melquisedeque Rodrigues dos Santos")
    time.sleep(1)
    page.click("input[id*='search'], input[value='Pesquisar'], button:has-text('Pesquisar')")
    time.sleep(5)

    link = page.query_selector("a:has-text('VER DETALHES DO PROCESSO'), a:has-text('0807644')")
    if link:
        with context.expect_page(timeout=15000) as new_page_info:
            link.click()
            
        detail_page = new_page_info.value
        detail_page.wait_for_load_state("domcontentloaded")
        time.sleep(5)
        
        # Localizar todos os links de "VISUALIZAR DOCUMENTOS" ou links de decisões
        vis_links = detail_page.query_selector_all("a:has-text('VISUALIZAR DOCUMENTOS'), a[title*='Visualizar'], a[id*='visualizar']")
        print(f"Encontrados {len(vis_links)} links de visualização de documentos.")
        
        for idx, vl in enumerate(vis_links):
            try:
                # Obter texto do elemento pai ou linha da tabela
                parent_txt = vl.evaluate("el => el.closest('tr') ? el.closest('tr').innerText : el.innerText")
                clean_name = f"doc_{idx+1}_" + "_".join([w for w in parent_txt.split() if w.isalnum()][:5])
                print(f"\nTentando abrir {clean_name} -> {parent_txt[:80]}...")
                
                # Clicar no link de visualização
                with context.expect_page(timeout=5000) as doc_page_info:
                    vl.click()
                doc_page = doc_page_info.value
                doc_page.wait_for_load_state("domcontentloaded")
                time.sleep(3)
                
                doc_txt = doc_page.inner_text("body")
                doc_html = doc_page.content()
                
                doc_txt_path = os.path.join(target_dir, f"{clean_name}.txt")
                doc_html_path = os.path.join(target_dir, f"{clean_name}.html")
                
                with open(doc_txt_path, "w", encoding="utf-8") as f:
                    f.write(doc_txt)
                with open(doc_html_path, "w", encoding="utf-8") as f:
                    f.write(doc_html)
                    
                print(f"  ✅ Documento salvo: {doc_txt_path} ({len(doc_txt)} chars)")
                doc_page.close()
            except Exception as e:
                print(f"  ⚠️ Falha ao abrir popup do doc {idx+1}: {e}")
                
    browser.close()

print("\n=== CONCLUÍDO ===")
