# -*- coding: utf-8 -*-
"""Captura REAL ao vivo do HC 1116750/RJ no STJ — bypass CSID via Playwright antidetecção.
Estratégia: GET direto já retorna 4 registros incluindo o HC (sonda confirmou).
Agora clica no link do HC para capturar a página de detalhes (fases, decisões, petições).
"""
import time, os, re, sys, json
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

# Identificação do caso
HC_NUM = "1116750"
HC_REGISTRO = "2026/0311210-7"
URL_LISTA = "https://processo.stj.jus.br/processo/pesquisa/?aplicacao=processos.ea&tipoPesquisa=tipoPesquisaGenerica&termo=1116750"

OUT_DIR = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(OUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled","--no-sandbox","--disable-dev-shm-usage"])
    ctx = browser.new_context(
        viewport={"width":1366,"height":900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        locale="pt-BR",
        extra_http_headers={"Accept-Language":"pt-BR,pt;q=0.9,en;q=0.8"},
    )
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});")
    page = ctx.new_page()

    print(f"=== STJ — HC 1116750/RJ — Captura ao vivo {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
    print(f">> GET {URL_LISTA}")
    page.goto(URL_LISTA, wait_until="domcontentloaded", timeout=45000)
    time.sleep(6)

    # Extrair todos os links href
    links = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('a')).map(a => ({
            text: (a.textContent||'').trim().slice(0,120),
            href: a.href,
            outer: a.outerHTML.slice(0,400)
        })).filter(x => x.href.includes('processo.stj.jus.br') || /HC\\s*1116750/i.test(x.text) || /JULIO/i.test(x.text.toUpperCase()) || x.text.includes('1116750'))
    }""")
    print(f"Links candidatos: {len(links)}")
    for L in links:
        print(f"  text={L['text']!r} href={L['href']}\n  outer={L['outer'][:250]}")
    
    # Todos os links da página de lista
    all_links = page.evaluate("""() => Array.from(document.querySelectorAll('a')).slice(0,30).map(a=>({text:(a.textContent||'').trim().slice(0,100), href:a.href}))""")
    print("\n=== Todos os <a> (primeiros 30) ===")
    for a in all_links:
        print(f"  {a['text']!r} -> {a['href'][:180]}")

    # Tenta clicar no link do HC 1116750/RJ (última linha da tabela)
    hc_link = page.evaluate("""() => {
        const anchors = Array.from(document.querySelectorAll('a'));
        // Procura pelo que tem HC 1116750
        for(const a of anchors){
            const t=(a.textContent||'').toUpperCase();
            const h=a.href||'';
            if(t.includes('1116750') && t.includes('HC')) return a.href;
        }
        // fallback: procura linha da tabela com JULIO PEREIRA MARCOS
        for(const a of anchors){
            const row = a.closest('tr');
            if(row && row.innerText.toUpperCase().includes('JULIO PEREIRA MARCOS')) return a.href;
        }
        return null;
    }""")
    print(f"\nHC link href: {hc_link}")

    if not hc_link:
        # Extrai sequential direto dos links
        body_html = page.content()
        # STJ usa ?sequencial=...&num_registro=... como href do detalhe
        seq_match = re.search(r'sequencial=\d+', body_html)
        reg_match = re.search(r'num_registro=202603112107', body_html)
        print(f"seq_match={seq_match} reg_match={reg_match}")
        print(f"Body contains sequencial? {'sequencial' in body_html}")
        # dump snippet around JULIO
        idx = body_html.upper().find("JULIO PEREIRA")
        if idx != -1:
            print(f"Snippet around JULIO:\n{body_html[max(0,idx-2000):idx+2000][:4000]}")

    # Clique interativo com sessão protegida (superação CSID via evento real)
    clicked = False
    if hc_link:
        print(f"\n>> Clicando no link do HC (sessão antidetecção)...")
        clicked = page.evaluate("""(href) => {
            const a = Array.from(document.querySelectorAll('a')).find(x=>x.href===href);
            if(a){ a.scrollIntoView({block:'center'}); return true; } return false;
        }""", hc_link)
        print(f"scrollIntoView: {clicked}")
        time.sleep(1)
        # click real
        try:
            page.evaluate("""(href) => {
                const a = Array.from(document.querySelectorAll('a')).find(x=>x.href===href);
                if(a) a.click();
            }""", hc_link)
            page.wait_for_load_state("domcontentloaded", timeout=30000)
            time.sleep(6)
            print(f"URL após clique: {page.url}")
            txt = page.evaluate("document.body.innerText")
            print(f"Body chars detalhe: {len(txt)}\n{txt[:12000]}")
            page.screenshot(path=os.path.join(OUT_DIR, "_stj_hc1116750_detalhe.png"), full_page=True)
            print("Screenshot detalhe salvo.")
            
            # Tenta expandir abas: Fases, Decisões, Petições
            tabs = page.evaluate("""() => Array.from(document.querySelectorAll('a, button, li')).filter(e=>e.offsetWidth>0).map(e=>(e.textContent||'').trim()).filter(t=>t.length>0 && t.length<40).slice(0,50)""")
            print(f"\nTabs/botões visíveis: {tabs}")
            
            # Baixar HTML completo
            html = page.content()
            with open(os.path.join(OUT_DIR, "stj_hc_1116750_RJ_detalhe.html"), "w", encoding="utf-8") as f:
                f.write(html)
            print(f"HTML detalhe salvo ({len(html)} chars).")
            
            # Extrai texto estruturado
            body_text = page.evaluate("document.body.innerText")
            with open(os.path.join(OUT_DIR, "stj_hc_1116750_RJ_detalhe.txt"), "w", encoding="utf-8") as f:
                f.write(f"URL: {page.url}\nCapturado em: {time.strftime('%Y-%m-%d %H:%M:%S')}\n{'='*80}\n{body_text}")
            print(f"TXT detalhe salvo ({len(body_text)} chars).")
        except Exception as e:
            print(f"Erro ao clicar: {e}")
            import traceback; traceback.print_exc()
    else:
        print("ERRO: link do HC não encontrado — salvando HTML da lista.")
        html = page.content()
        with open(os.path.join(OUT_DIR, "stj_hc_1116750_RJ_lista.html"), "w", encoding="utf-8") as f:
            f.write(html)
        txt = page.evaluate("document.body.innerText")
        with open(os.path.join(OUT_DIR, "stj_hc_1116750_RJ_lista.txt"), "w", encoding="utf-8") as f:
            f.write(txt)
        page.screenshot(path=os.path.join(OUT_DIR, "_stj_hc1116750_lista.png"), full_page=True)

    # Intercepta requisições para descobrir API de fases
    print("\n=== Dump requests capturados ===")
    # Segunda navegação com request interception para mapear API
    page2 = ctx.new_page()
    reqs = []
    page2.on("request", lambda r: reqs.append(f"{r.method} {r.url[:250]}"))
    page2.goto(URL_LISTA, wait_until="domcontentloaded", timeout=45000)
    time.sleep(4)
    # clica de novo se achou link
    if hc_link:
        try:
            page2.evaluate("""(href) => {
                const a = Array.from(document.querySelectorAll('a')).find(x=>x.href===href);
                if(a) a.click();
            }""", hc_link)
            page2.wait_for_load_state("domcontentloaded", timeout=30000)
            time.sleep(5)
        except: pass
    print(f"Requests ({len(reqs)}):")
    for r in reqs[:40]:
        print(f"  {r}")

    browser.close()

print("\n=== FIM CAPTURA STJ ===")
