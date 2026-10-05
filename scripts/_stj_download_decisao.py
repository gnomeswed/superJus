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
    # Captura download via evento
    with page.expect_download(timeout=30000) as dl_info:
        page.goto(URL_DOC, wait_until="domcontentloaded", timeout=45000)
    dl = dl_info.value
    save_path = os.path.join(OUT_DIR, f"stj_hc_1116750_decisao_20260731_{dl.suggested_filename}")
    dl.save_as(save_path)
    print(f"Download salvo: {save_path} ({os.path.getsize(save_path)} bytes)")
    # Se for PDF, extrai texto
    if save_path.lower().endswith(".pdf"):
        try:
            import fitz
            doc = fitz.open(save_path)
            txt = "\n".join([pg.get_text() for pg in doc])
            print(f"PDF pages: {len(doc)} | chars: {len(txt)}\n{txt[:6000]}")
            with open(save_path + ".txt", "w", encoding="utf-8") as f:
                f.write(txt)
            print(f"TXT salvo: {save_path}.txt")
        except Exception as e:
            print(f"Extração PDF falhou: {e} — tentando pymupdf via subprocess")
            import subprocess, os as _os
            env=dict(_os.environ); env.pop("PYTHONPATH", None)
            r=subprocess.run([r"C:/Users/Administrator/AppData/Local/Programs/Python/Python312/python.exe","-m","pymupdf","--help"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=15)
            print(r.stdout[:500])
    elif save_path.lower().endswith(".html"):
        txt = open(save_path, encoding="utf-8", errors="replace").read()
        print(f"HTML chars: {len(txt)}\n{txt[:6000]}")
    else:
        # tenta ler como texto
        raw = open(save_path, "rb").read()
        print(f"Raw {len(raw)} bytes, head hex: {raw[:100].hex()}")
        try:
            txt = raw.decode("utf-8", errors="replace")
            print(txt[:6000])
        except: pass
    browser.close()
print("=== FIM DOWNLOAD ===")
