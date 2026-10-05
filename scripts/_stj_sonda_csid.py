# -*- coding: utf-8 -*-
"""Sonda STJ — mapeia CSID e formulário de consulta processual (HC 1.116.750/RJ)."""
import time, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

CANDIDATOS = [
    "https://processo.stj.jus.br/processo/pesquisa/?aplicacao=processos.ea&tipoPesquisa=tipoPesquisaGenerica&termo=1116750",
    "https://processo.stj.jus.br/processo/pesquisa/",
    "https://www.stj.jus.br/sites/portalp/Processos/Consulta-Processual",
    "https://scon.stj.jus.br/SCON/",
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled","--no-sandbox","--disable-dev-shm-usage"])
    ctx = browser.new_context(
        viewport={"width":1366,"height":900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        locale="pt-BR",
        extra_http_headers={"Accept-Language":"pt-BR,pt;q=0.9,en;q=0.8"},
    )
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined}); delete navigator.__proto__.webdriver;")
    
    for url in CANDIDATOS:
        print(f"\n{'='*80}\n>> GET {url}\n{'='*80}")
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            time.sleep(5)
            status_note = f"URL final: {page.url}"
            print(status_note)
            # CSID detection
            body = page.content()
            has_csid = "CSID" in body or "csid" in body.lower()
            has_cloudflare = "cloudflare" in body.lower() or "cf-challenge" in body.lower()
            has_verificacao = "verifica" in body.lower() or "confirme que você é humano" in body.lower()
            print(f"CSID={has_csid} | cloudflare={has_cloudflare} | verificacao={has_verificacao}")
            print(f"Title: {page.title()}")
            txt = page.evaluate("document.body.innerText")
            print(f"Body chars: {len(txt)} | Preview:\n{txt[:4000]}")
            # Form mapping
            forms = page.evaluate("""() => {
                return Array.from(document.querySelectorAll('form')).map(f => ({
                    action: f.action, method: f.method, id: f.id, name: f.name,
                    inputs: Array.from(f.querySelectorAll('input, select, button')).map(i=>({tag:i.tagName, type:i.type||'', name:i.name||i.id||'', id:i.id||'', placeholder:i.placeholder||'', text:(i.textContent||'').trim().slice(0,60)}))
                }))
            }""")
            print(f"Forms: {len(forms)}")
            for fi, f in enumerate(forms):
                print(f"  Form {fi}: action={f['action']} method={f['method']} id={f['id']}")
                for inp in f['inputs'][:20]:
                    print(f"    {inp}")
            # Inputs globais
            inputs = page.evaluate("""() => Array.from(document.querySelectorAll('input, button, select')).slice(0,40).map(e=>({
                tag:e.tagName, type:e.type||'', name:e.name||'', id:e.id||'', placeholder:e.placeholder||'', text:(e.textContent||'').trim().slice(0,80), outer:e.outerHTML.slice(0,220)
            }))""")
            print(f"Inputs globais ({len(inputs)}):")
            for it in inputs:
                print(f"  {it}")
            page.screenshot(path=f"C:/Projetos/superJus/_stj_sonda_{CANDIDATOS.index(url)}.png", full_page=True)
            print(f"Screenshot: _stj_sonda_{CANDIDATOS.index(url)}.png")
        except Exception as e:
            print(f"ERRO {url}: {e}")
            import traceback; traceback.print_exc()
    browser.close()
print("\n=== FIM SONDA ===")
