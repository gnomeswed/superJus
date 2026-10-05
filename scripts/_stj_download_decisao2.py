# -*- coding: utf-8 -*-
import time, os, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

OUT_DIR = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(OUT_DIR, exist_ok=True)
URL_DOC = "https://processo.stj.jus.br/processo/dj/documento/?&sequencial=389054957&num_registro=202603112107&data=20260731&data_pesquisa=20260731&tipo=0&componente=MON"
URL_RE = "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo=202603112107&totalRegistrosPorPagina=40&aplicacao=processos.ea"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled","--no-sandbox"])
    ctx = browser.new_context(viewport={"width":1366,"height":900}, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/127.0.0.0 Safari/537.36", locale="pt-BR", accept_downloads=True)
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});")
    page = ctx.new_page()
    print(f">> Sementeando sessão")
    page.goto(URL_RE, wait_until="domcontentloaded", timeout=45000)
    time.sleep(5)
    # A navegação que dispara download deve usar expect_download envolvendo a ação que inicia o download
    print(f">> Disparando download via evaluate (evita goto-download race)")
    try:
        with page.expect_download(timeout=30000) as dl_info:
            page.evaluate(f"window.location.href = '{URL_DOC}'")
            page.wait_for_load_state("domcontentloaded", timeout=15000)
    except Exception as e:
        print(f"expect_download falhou (esperado se não for download): {e}")
        # tenta captura direta via request
        req = ctx.request if hasattr(ctx, 'request') else None
        html = page.content()
        print(html[:2000])
        browser.close()
        sys.exit(0)
    dl = dl_info.value
    save_path = os.path.join(OUT_DIR, f"stj_hc_1116750_decisao_20260731_{dl.suggested_filename}")
    dl.save_as(save_path)
    print(f"Download salvo: {save_path} ({os.path.getsize(save_path)} bytes)")
    raw = open(save_path, "rb").read()
    print(f"Head 300 bytes hex: {raw[:300].hex()[:600]}")
    print(f"Head 500 chars decode: {raw[:2000].decode('utf-8', errors='replace')[:3000]}")
    # Se for PDF, extrai
    if save_path.lower().endswith(".pdf") or raw[:4]==b"%PDF":
        try:
            import fitz
            doc = fitz.open(save_path)
            txt = "\n".join([pg.get_text() for pg in doc])
            print(f"PDF pages: {len(doc)} | chars: {len(txt)}\n{txt[:8000]}")
            with open(os.path.join(OUT_DIR, "stj_hc_1116750_decisao_HermanBenjamin.txt"), "w", encoding="utf-8") as f:
                f.write(txt)
            print("TXT salvo.")
        except Exception as e:
            import traceback; traceback.print_exc()
    browser.close()
print("=== FIM ===")
