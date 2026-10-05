# -*- coding: utf-8 -*-
import time
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

proc_fmt = "0827233-23.2026.8.19.0001"
print(f"=== TESTE LIVE PJe 1G TJRJ: {proc_fmt} ===", flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-blink-features=AutomationControlled'])
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    
    url = "https://tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam"
    print(f"1. Acessando {url} (wait_until='commit', timeout=60s)...", flush=True)
    page.goto(url, wait_until="commit", timeout=60000)
    print("2. Navegação inicial efetuada. Aguardando input...", flush=True)
    
    page.wait_for_selector("input[id*='inputNumeroProcesso']", timeout=60000)
    print("3. Campo localizado. Preenchendo...", flush=True)
    page.fill("input[id*='inputNumeroProcesso']", proc_fmt)
    time.sleep(1)
    
    print("4. Clicando em pesquisar...", flush=True)
    btn = page.locator("button[id*='searchProcessos'], input[id*='searchProcessos']").first
    btn.click()
    
    print("5. Aguardando tabela de resultados...", flush=True)
    time.sleep(10)
    
    # Checar se encontrou o processo na tabela
    link_detalhes = page.locator(f"a:has-text('{proc_fmt}')").first
    if link_detalhes.is_visible():
        print("✓ Processo encontrado na listagem! Clicando para abrir detalhes...", flush=True)
        with context.expect_page(timeout=25000) as new_page_info:
            link_detalhes.click()
        
        detalhes_page = new_page_info.value
        detalhes_page.wait_for_load_state("domcontentloaded", timeout=25000)
        time.sleep(5)
        
        body_text = detalhes_page.inner_text("body")
        print(f"✅ Detalhes extraídos! Tamanho: {len(body_text)} caracteres.", flush=True)
        
        out_path = r"c:\Projetos\superJus\Clientes\Leandro_Mecanico\detalhes_pje_leandro_live_latest.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(body_text)
        print(f"Salvo em: {out_path}", flush=True)
        
        # Exibir as primeiras 60 linhas
        lines = [l.strip() for l in body_text.splitlines() if l.strip()]
        for l in lines[:60]:
            print(f"  • {l}", flush=True)
    else:
        print("⚠️ Link do processo não apareceu. Conteúdo retornado da página de busca:", flush=True)
        body = page.inner_text("body")
        for l in [x.strip() for x in body.splitlines() if x.strip()][:30]:
            print(f"  > {l}", flush=True)
            
    browser.close()

print("=== FIM DA CONSULTA ===", flush=True)
