# -*- coding: utf-8 -*-
"""Verificação ao vivo 16/08/2026 — Júlio Pereira Marcos — todos os processos + DJERJ novo"""
import time, sys, os
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

PROCS_1A = [
    ("0023013-51.2021.8.19.0078", "Ação Penal Búzios 2ª Vara"),
    ("0001140-87.2024.8.19.0078", "Execução/Medida Búzios"),
]
PROC_2A = "0029845-67.2026.8.19.0000"

def check_1a(page, proc_num, titulo):
    print(f"\n{'='*70}\n[1ª] {titulo} — {proc_num}\n{'='*70}")
    try:
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=45000)
        time.sleep(3)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        fr = page.query_selector("iframe#mainframe").content_frame()
        time.sleep(2)
        fr.evaluate(f"""() => {{
            const inp = Array.from(document.querySelectorAll('input')).find(i => i.name==='numeroProcesso' || i.id==='numeroProcesso');
            if(inp){{ inp.value='{proc_num}'; inp.dispatchEvent(new Event('input',{{bubbles:true}})); inp.dispatchEvent(new Event('change',{{bubbles:true}})); }}
        }}""")
        time.sleep(1)
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth>0 && (b.textContent||'').toLowerCase().includes('pesquisar'));
            if(btn) btn.click();
        }""")
        time.sleep(7)
        # check PJe modal
        pje = fr.evaluate("""() => {
            const el = Array.from(document.querySelectorAll('h4, div, p')).find(e => (e.innerText||'').includes('Mensagem Processo do PJe'));
            return !!el;
        }""")
        if pje:
            body = fr.inner_text("body")
            print(">> BLOQUEIO PJe detectado")
            print(body[:3000])
            return {"pje": True, "body": body}
        # try expand
        try:
            fr.evaluate("""() => {
                const btn = Array.from(document.querySelectorAll('button')).find(b => (b.textContent||'').toLowerCase().includes('todos os movimentos'));
                if(btn) btn.click();
            }""")
            time.sleep(6)
        except: pass
        body = fr.inner_text("body")
        print(body[:7000])
        # extract localizacao
        loc = ""
        if "Localização na Serventia" in body:
            idx = body.index("Localização na Serventia")
            loc = body[idx:idx+500].replace("\n"," | ")
            print(f"\n>>> LOCALIZAÇÃO: {loc}")
        # ultima movimentacao
        if "Última Movimentação" in body or "Tipo do Movimento" in body:
            print(f"\n>>> Body length: {len(body)} | Movimentos: {body.count('Tipo do Movimento:')}")
        return {"pje": False, "body": body, "loc": loc}
    except Exception as e:
        print(f"ERRO {titulo}: {e}")
        import traceback; traceback.print_exc()
        return {"error": str(e)}

def check_2a_detail(page):
    print(f"\n{'='*70}\n[2ª] HC/ROC — {PROC_2A}\n{'='*70}")
    try:
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=60000)
        time.sleep(4)
        frame = page.frame_locator("iframe#mainframe")
        frame.locator("input[name='numeroProcesso']").fill(PROC_2A)
        time.sleep(1)
        frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
        time.sleep(8)
        real_frame = page.query_selector("iframe#mainframe").content_frame()
        body_res = real_frame.inner_text("body")
        print("Resultado busca 2ª inst (resumo):")
        print(body_res[:6000])
        # collect links
        links = real_frame.locator("table a")
        n = links.count()
        print(f"Links na tabela: {n}")
        textos = []
        for i in range(n):
            try: textos.append(links.nth(i).inner_text(timeout=3000))
            except: pass
        print("Textos links:", textos)
        # abrir cada detalhe
        for alvo in ["2026.059.10770", "2026.141.00580"]:
            print(f"\n--- Abrindo detalhe {alvo} ---")
            try:
                page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=60000)
                time.sleep(4)
                frame = page.frame_locator("iframe#mainframe")
                frame.locator("input[name='numeroProcesso']").fill(PROC_2A)
                time.sleep(1)
                frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
                time.sleep(8)
                real_frame = page.query_selector("iframe#mainframe").content_frame()
                links = real_frame.locator("table a")
                n2 = links.count()
                idx=None
                for i in range(n2):
                    t = links.nth(i).inner_text(timeout=3000)
                    if alvo in t:
                        idx=i; break
                if idx is None:
                    print(f"Link {alvo} não encontrado")
                    continue
                links.nth(idx).click()
                time.sleep(8)
                real_frame = page.query_selector("iframe#mainframe").content_frame()
                try:
                    real_frame.locator("button:has-text('Todos Os Movimentos')").first.click(timeout=5000)
                    time.sleep(5)
                except: pass
                body = real_frame.inner_text("body")
                print(body[:8000])
                if "FASE ATUAL" in body:
                    s = body.index("FASE ATUAL")
                    print("\n>>> FASE ATUAL:", body[s:s+600].replace("\n"," | "))
                if "Localização" in body:
                    s = body.index("Localização")
                    print("\n>>> LOCALIZAÇÃO 2ª:", body[s:s+500].replace("\n"," | "))
            except Exception as e:
                print(f"Erro detalhe {alvo}: {e}")
                import traceback; traceback.print_exc()
    except Exception as e:
        print(f"ERRO 2ª inst: {e}")
        import traceback; traceback.print_exc()

def check_djerj(page):
    print(f"\n{'='*70}\n[DJERJ novo consultadje] — 01/08 a 16/08/2026\n{'='*70}")
    for proc in ["0023013-51.2021.8.19.0078", "0029845-67.2026.8.19.0000", "0001140-87.2024.8.19.0078"]:
        url = f"https://www3.tjrj.jus.br/consultadje/Result.aspx?dtInicio=01%2F08%2F2026&dtFim=16%2F08%2F2026&txtPesq={proc}&tipoPesq=PROC"
        print(f"\n>> {proc} => {url}")
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            time.sleep(5)
            body = page.evaluate("document.body.innerText")
            print(body[:4000])
            if "Não foram encontradas" in body:
                print(">>> SEM publicação para este processo no período")
            else:
                print(">>> POSSÍVEL publicação encontrada!")
        except Exception as e:
            print(f"Erro DJERJ {proc}: {e}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled","--no-sandbox"])
    ctx = browser.new_context(viewport={"width":1366,"height":900}, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/127.0.0.0 Safari/537.36")
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
    for proc, titulo in PROCS_1A:
        check_1a(page, proc, titulo)
        time.sleep(2)
    check_2a_detail(page)
    time.sleep(2)
    check_djerj(page)
    browser.close()
print("\n=== FIM VERIFICAÇÃO 15/08 ===")
