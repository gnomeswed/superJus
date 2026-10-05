# -*- coding: utf-8 -*-
"""Captura íntegra da Decisão Monocrática do STJ — HC 1116750 (sequencial 389054957) + converte."""
import time, os, sys, re
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

OUT_DIR = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(OUT_DIR, exist_ok=True)

# URL direta da decisão (endpoints mapeados no HTML salvo)
URL_DECISAO = "https://processo.stj.jus.br/processo/dj/documento/mediado/?tipo_documento=documento&componente=MON&sequencial=389054957&tipo_documento=documento&num_registro=202603112107&data=20260731&tipo=0"
URL_RE = "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo=202603112107&totalRegistrosPorPagina=40&aplicacao=processos.ea"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled","--no-sandbox"])
    ctx = browser.new_context(viewport={"width":1366,"height":900}, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/127.0.0.0 Safari/537.36", locale="pt-BR")
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});")
    page = ctx.new_page()
    # Primeiro visita o HC para obter cookies/sessão válida (Step Stone do bypass)
    print(f">> Sementeando sessão: {URL_RE}")
    page.goto(URL_RE, wait_until="domcontentloaded", timeout=45000)
    time.sleep(5)
    txt = page.evaluate("document.body.innerText")
    print(f"Sessão body chars: {len(txt)} | tem HC? {'1116750' in txt}")

    print(f"\n>> Acessando decisão: {URL_DECISAO}")
    page.goto(URL_DECISAO, wait_until="domcontentloaded", timeout=45000)
    time.sleep(6)
    print(f"URL final decisão: {page.url}")
    txt2 = page.evaluate("document.body.innerText")
    print(f"Decisão body chars: {len(txt2)}\nPreview:\n{txt2[:5000]}")
    html = page.content()
    print(f"HTML len: {len(html)}")
    with open(os.path.join(OUT_DIR, "stj_hc_1116750_RJ_decisao_HermanBenjamin_raw.html"), "w", encoding="utf-8") as f:
        f.write(html)
    with open(os.path.join(OUT_DIR, "stj_hc_1116750_RJ_decisao_HermanBenjamin_raw.txt"), "w", encoding="utf-8") as f:
        f.write(txt2)
    page.screenshot(path=os.path.join(OUT_DIR, "_stj_decisao_HermanBenjamin.png"), full_page=True)
    print("Decisão salva.")

    # Tenta extrair texto estruturado do documento mediado
    # Se for viewer, extrai iframe src
    iframe_src = page.evaluate("""() => {
        const f = document.querySelector('iframe');
        return f ? f.src : null;
    }""")
    print(f"iframe src: {iframe_src}")
    if iframe_src:
        print(f">> Seguindo iframe: {iframe_src}")
        page.goto(iframe_src if iframe_src.startswith('http') else 'https://processo.stj.jus.br'+iframe_src, wait_until="domcontentloaded", timeout=45000)
        time.sleep(6)
        txt3 = page.evaluate("document.body.innerText")
        print(f"Iframe body chars: {len(txt3)}\n{txt3[:8000]}")
        html3 = page.content()
        with open(os.path.join(OUT_DIR, "stj_hc_1116750_RJ_decisao_HermanBenjamin_iframe.html"), "w", encoding="utf-8") as f:
            f.write(html3)
        with open(os.path.join(OUT_DIR, "stj_hc_1116750_RJ_decisao_HermanBenjamin_iframe.txt"), "w", encoding="utf-8") as f:
            f.write(txt3)

    browser.close()
print("=== FIM DECISAO ===")
