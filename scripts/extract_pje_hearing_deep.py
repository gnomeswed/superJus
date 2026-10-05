# -*- coding: utf-8 -*-
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

num_processo = "0807644-58.2025.8.19.0202"
target_dir = r"c:\Projetos\superJus\Clientes\Melquisedeque\processos\0807644-58.2025.8.19.0202"
os.makedirs(target_dir, exist_ok=True)

print("=== EXTRAÇÃO PROFUNDA DA ATA E DETALHES DA AUDIÊNCIA DE 25/03/2026 ===")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 900}
    )
    page = context.new_page()

    url_pje = "https://tjrj.pje.jus.br/pje/ConsultaPublica/listView.seam"
    print(f"1. Acessando PJe: {url_pje}...")
    page.goto(url_pje, wait_until="networkidle", timeout=35000)
    time.sleep(2)

    # Preencher nome
    nome_input = page.query_selector("input[id*='nomeParte'], input[id*='NomeParte']")
    if nome_input:
        nome_input.fill("Melquisedeque Rodrigues dos Santos")
        print("   • Nome preenchido no PJe.")
        
    time.sleep(1)
    btn = page.query_selector("input[id*='search'], input[value='Pesquisar'], button:has-text('Pesquisar')")
    if btn:
        btn.click()
        print("   • Pesquisa submetida. Aguardando resultado...")
        time.sleep(6)

    # Salvar screenshot do resultado
    page.screenshot(path=os.path.join(target_dir, "resultado_busca_pje.png"))

    # Localizar link com o número do processo ou "VER DETALHES DO PROCESSO"
    link = page.query_selector("a:has-text('0807644'), a:has-text('VER DETALHES DO PROCESSO'), td a")
    if link:
        print(f"   • Clicando no link: {link.inner_text()[:60]}...")
        
        # PJe abre popup via window.open ou nova aba
        with context.expect_page(timeout=15000) as new_page_info:
            link.click()
            
        detail_page = new_page_info.value
        detail_page.wait_for_load_state("networkidle", timeout=20000)
        time.sleep(6)
        
        print("   ✅ Janela de detalhes do processo carregada com sucesso!")
        detail_page.screenshot(path=os.path.join(target_dir, "detalhes_processo_completo.png"), full_page=True)
        
        # Extrair texto integral da página de detalhes (movimentações + documentos)
        det_text = detail_page.inner_text("body")
        det_html = detail_page.content()
        
        with open(os.path.join(target_dir, "detalhes_pje_completo.txt"), "w", encoding="utf-8") as f:
            f.write(det_text)
        with open(os.path.join(target_dir, "detalhes_pje_completo.html"), "w", encoding="utf-8") as f:
            f.write(det_html)
            
        print(f"   • Detalhes salvos em detalhes_pje_completo.txt ({len(det_text)} caracteres)")
        
        # Procurar por abas ou seções de Audiência / Documentos
        print("\n--- TRECHOS CAPTURADOS DA AUDIÊNCIA E ATOS ---")
        for line in det_text.splitlines():
            if any(k in line.lower() for k in ["audiência", "audiencia", "25/03/2026", "termo", "ata", "depoimento", "testemunha", "vítima", "vitima", "interrogatório", "interrogatorio", "desmembramento"]):
                print("  •", line.strip()[:140])
                
    else:
        print("   ❌ Link de detalhes não localizado na tabela.")

    browser.close()

print("\n=== EXTRAÇÃO CONCLUÍDA ===")
