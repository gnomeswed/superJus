# -*- coding: utf-8 -*-
"""STJ — captura fases/decisões/petições do HC 1116750/RJ via tabs Ajax."""
import time, os, sys, re, json
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

HC_REG_URL = "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo=202603112107&totalRegistrosPorPagina=40&aplicacao=processos.ea"
OUT_DIR = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(OUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled","--no-sandbox","--disable-dev-shm-usage"])
    ctx = browser.new_context(
        viewport={"width":1366,"height":900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        locale="pt-BR",
    )
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});")
    page = ctx.new_page()
    page.on("response", lambda r: print(f"[RESP] {r.status} {r.url[:160]}") if any(k in r.url for k in ["fases","decis","petic","pauta","andamento","detalhe"]) else None)

    # Navegação direta por num_registro (resolve o CSID com sessão antidetecção)
    print(f">> GET {HC_REG_URL}")
    page.goto(HC_REG_URL, wait_until="domcontentloaded", timeout=45000)
    time.sleep(6)
    print(f"URL final: {page.url}")
    txt = page.evaluate("document.body.innerText")
    print(f"Body chars: {len(txt)}\n{txt[:6000]}")
    page.screenshot(path=os.path.join(OUT_DIR, "_stj_hc1116750_reg.png"), full_page=True)
    print("Screenshot reg salvo.")

    # Mapear tabs e XHR base
    html = page.content()
    with open(os.path.join(OUT_DIR, "stj_hc_1116750_RJ_reg.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML reg salvo ({len(html)} chars)")

    # Avalia JS da página para achar endpoints
    js_info = page.evaluate("""() => {
        const txt = document.documentElement.outerHTML;
        // procura por URLs de fases/decisoes nos scripts
        const snippets = [];
        const re = /\\/(processo|api)[^\"'\\s]*fases[^\"'\\s]*/gi;
        let m; while((m=re.exec(txt))!==null) snippets.push(m[0]);
        const re2 = /\\/(processo|api)[^\"'\\s]*decis[^\"'\\s]*/gi;
        while((m=re2.exec(txt))!==null) snippets.push(m[0]);
        // hrefs das tabs
        const tabs = Array.from(document.querySelectorAll('a')).map(a=>({text:(a.textContent||'').trim().slice(0,60), href:a.href, onclick:a.getAttribute('onclick')||''})).filter(x=>/Fases|Decis|Peti/i.test(x.text));
        // seq num
        const seq = (document.documentElement.outerHTML.match(/sequencial\\s*[=:]\\s*\\d+/gi)||[]).slice(0,5);
        return {snippets: snippets.slice(0,15), tabs, seq};
    }""")
    print(f"JS info: {json.dumps(js_info, ensure_ascii=False, indent=2)[:4000]}")

    # Clique nas abas e captura cada uma
    for tab_name in ["Fases", "Decisões", "Petições", "Pautas"]:
        print(f"\n{'='*60}\n>> TAB: {tab_name}\n{'='*60}")
        try:
            # tenta clicar
            clicked = page.evaluate("""(name)=> {
                const el = Array.from(document.querySelectorAll('a, button, li, span')).find(e=>{
                    const t=(e.textContent||'').trim();
                    return t.toLowerCase()===name.toLowerCase() && e.offsetWidth>0;
                });
                if(el){ el.click(); return true; }
                // fallback: procura por contains
                const el2 = Array.from(document.querySelectorAll('a')).find(e=>(e.textContent||'').trim().toLowerCase().includes(name.toLowerCase()));
                if(el2){ el2.click(); return true; }
                return false;
            }""", tab_name)
            print(f"clicked={clicked}")
            time.sleep(5)
            txt2 = page.evaluate("document.body.innerText")
            print(f"Body chars após {tab_name}: {len(txt2)} | Preview:\n{txt2[-8000:]}")
            # salva
            html2 = page.content()
            with open(os.path.join(OUT_DIR, f"stj_hc_1116750_RJ_{tab_name}.html"), "w", encoding="utf-8") as f:
                f.write(html2)
            with open(os.path.join(OUT_DIR, f"stj_hc_1116750_RJ_{tab_name}.txt"), "w", encoding="utf-8") as f:
                f.write(txt2)
            print(f"Salvo HTML/TXT {tab_name}")
            page.screenshot(path=os.path.join(OUT_DIR, f"_stj_hc1116750_{tab_name}.png"), full_page=True)
        except Exception as e:
            print(f"Erro tab {tab_name}: {e}")

    # Volta para Fases e extrai tabela com precisão
    try:
        page.evaluate("""()=>{ const el=Array.from(document.querySelectorAll('a')).find(e=>(e.textContent||'').trim()==='Fases'); if(el) el.click(); }""")
        time.sleep(5)
        fases = page.evaluate("""() => {
            const rows = Array.from(document.querySelectorAll('table tr'));
            return rows.slice(0,40).map(tr=>{
                const tds = Array.from(tr.querySelectorAll('td, th')).map(td=>(td.innerText||td.textContent||'').trim().slice(0,220));
                return tds;
            }).filter(r=> r.join('').trim().length>0);
        }""")
        print(f"\n=== TABELA FASES (rows={len(fases)}) ===")
        for r in fases:
            print(r)
        # decisões
        page.evaluate("""()=>{ const el=Array.from(document.querySelectorAll('a')).find(e=>(e.textContent||'').trim()==='Decisões'); if(el) el.click(); }""")
        time.sleep(5)
        decs = page.evaluate("""() => {
            const rows = Array.from(document.querySelectorAll('table tr'));
            return rows.slice(0,30).map(tr=> Array.from(tr.querySelectorAll('td, th')).map(td=>(td.innerText||'').trim().slice(0,300))).filter(r=>r.join('').trim());
        }""")
        print(f"\n=== TABELA DECISÕES (rows={len(decs)}) ===")
        for r in decs:
            print(r)
    except Exception as e:
        print(f"Erro extração tabelas: {e}")

    browser.close()
print("\n=== FIM CAPTURA TABS ===")
