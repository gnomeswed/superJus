# -*- coding: utf-8 -*-
"""Varredura COMPLETA — todos os processos do Júlio (inclui original desmembrado) — 15/08/2026
Captura: espelho + Todos Os Movimentos + Ver Íntegra + DJERJ novo + tentativa API chain 1ª inst.

Alvos (case_meta.json):
  0023013-51.2021.8.19.0078  — Ação Penal Búzios 2ª Vara (desmembrado do Júlio)
  0022975-39.2021.8.19.0078  — Ação Penal principal (original, desmembrou o Júlio em 30/05/2022)
  0029845-67.2026.8.19.0000  — HC TJRJ 7ª Câmara (gera ROC 2026.141.00580)
  0001140-87.2024.8.19.0078  — Execução/Medida Búzios (apenso)
  0001492-25.2016.8.19.0046  — Correlato antigo (case_meta.json)
  0012801-74.2022            — visto em Andamentos_Oficiais_PDF (varre também)
Saída: C:/Projetos/superJus/Clientes/Júlio_Pereira_Marcos/Caso_Principal/documentos_processo/_varredura_15_08_2026/
"""
import time, os, sys, re, json, pathlib
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

OUT_BASE = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\_varredura_15_08_2026"
os.makedirs(OUT_BASE, exist_ok=True)

PROCS_1A = [
    ("0023013-51.2021.8.19.0078", "1A-Desmembrado-Julio"),
    ("0022975-39.2021.8.19.0078", "1A-Principal-Original-Desmembrou"),
    ("0001140-87.2024.8.19.0078", "1A-Apenso-Medida"),
    ("0001492-25.2016.8.19.0046", "1A-Correlato-2016"),
    ("0012801-74.2022.8.19.0046", "1A-Correlato-0012801"),
]

PROC_2A = "0029845-67.2026.8.19.0000"

def slug(s): return re.sub(r'[^0-9A-Za-z._-]+','_',s)[:120]

def save_text(path, txt):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f: f.write(txt)

def scrape_1a(page, cnj, label):
    print(f"\n{'='*70}\n[1ª] {label} — {cnj}\n{'='*70}")
    out_dir = os.path.join(OUT_BASE, slug(label+"__"+cnj))
    os.makedirs(out_dir, exist_ok=True)
    try:
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=45000)
        time.sleep(3)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        fr = page.query_selector("iframe#mainframe").content_frame()
        time.sleep(2)
        fr.evaluate(f"""() => {{
            const inp = Array.from(document.querySelectorAll('input')).find(i => i.name==='numeroProcesso' || i.id==='numeroProcesso');
            if(inp){{ inp.value='{cnj}'; inp.dispatchEvent(new Event('input',{{bubbles:true}})); inp.dispatchEvent(new Event('change',{{bubbles:true}})); }}
        }}""")
        time.sleep(1)
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth>0 && (b.textContent||'').toLowerCase().includes('pesquisar'));
            if(btn) btn.click();
        }""")
        time.sleep(8)
        pje = fr.evaluate("""() => {
            const el = Array.from(document.querySelectorAll('h4, div, p')).find(e => (e.innerText||'').includes('Mensagem Processo do PJe'));
            return !!el;
        }""")
        if pje:
            body = fr.inner_text("body")
            print(">> BLOQUEIO PJe")
            print(body[:3000])
            save_text(os.path.join(out_dir, "_PJE_BLOQUEIO.txt"), body)
            html = fr.evaluate("document.documentElement.outerHTML")
            save_text(os.path.join(out_dir, "_PJE_BLOQUEIO.html"), html)
            try: page.screenshot(path=os.path.join(out_dir, "_PJE_BLOQUEIO.png"), full_page=True)
            except: pass
            return {"pje": True}
        # expandir
        expanded=False
        for attempt in range(2):
            has_btn = fr.evaluate("""() => Array.from(document.querySelectorAll('button')).some(b => (b.textContent||'').toLowerCase().includes('todos os movimentos'))""")
            if has_btn:
                fr.evaluate("""() => {
                    const btn = Array.from(document.querySelectorAll('button')).find(b => (b.textContent||'').toLowerCase().includes('todos os movimentos'));
                    if(btn) btn.click();
                }""")
                time.sleep(10)
                expanded=True
            else:
                time.sleep(2)
        body = fr.inner_text("body")
        # html do iframe
        try: html = fr.evaluate("document.documentElement.outerHTML")
        except: html = page.content()
        save_text(os.path.join(out_dir, "espelho_TODOS_MOVIMENTOS.html" if expanded else "espelho_RESUMO.html"), html)
        save_text(os.path.join(out_dir, "espelho_TODOS_MOVIMENTOS.txt" if expanded else "espelho_RESUMO.txt"), body)
        try: page.screenshot(path=os.path.join(out_dir, "espelho.png"), full_page=True)
        except: pass
        print(body[:7000])
        print(f"\n>>> Body len={len(body)} | 'Tipo do Movimento:' x{body.count('Tipo do Movimento:')} | expanded={expanded}")
        if "Processo Principal" in body:
            idx=body.index("Processo Principal"); print(">>> Processo Principal:", body[idx:idx+400].replace("\n"," | "))
        if "Localização na Serventia" in body:
            idx=body.index("Localização na Serventia"); print(">>> Localização:", body[idx:idx+500].replace("\n"," | "))
        # modais Ver Íntegra
        botoes = fr.evaluate("""() => {
            const t_exatos = ['ver íntegra do(a) decisão (original)','ver íntegra do(a) decisão (simplificado)','ver íntegra','visualizar ato assinado digitalmente','visualizar ato'];
            return Array.from(document.querySelectorAll('a, button')).filter(el => el.offsetWidth>0 && el.offsetHeight>0).filter(el => {
                const t=(el.textContent||'').toLowerCase().trim(); return t_exatos.some(te=>t.startsWith(te)||t===te);
            }).map(el=>({text:(el.textContent||'').trim(), tag:el.tagName}))
        }""")
        print(f">>> Botões Ver Íntegra encontrados: {len(botoes)} — {[b['text'][:60] for b in botoes]}")
        integrais=[]
        for b in botoes:
            txt = b["text"]
            # re-acha por texto exato e clica
            clicked = fr.evaluate("""(t) => {
                const alvo = Array.from(document.querySelectorAll('a, button')).find(el => el.offsetWidth>0 && (el.textContent||'').trim()===t);
                if(alvo){ alvo.click(); return true;} return false;
            }""", txt)
            if not clicked:
                print(f"  - falha click: {txt[:60]}")
                continue
            try:
                fr.wait_for_selector('.modal-body, .ui-dialog-content, div[role="dialog"], .modal.show, .modal-content', timeout=10000, state="visible")
            except: pass
            time.sleep(4)
            modal_text = fr.evaluate("""() => {
                const containers = Array.from(document.querySelectorAll('.modal-body, .ui-dialog-content, div[role="dialog"] .modal-body, .modal.show .modal-body')).filter(c=>c.offsetWidth>0&&c.offsetHeight>0);
                if(containers.length>0){const txt=containers.map(c=>c.innerText||c.textContent).join('\\n\\n---\\n\\n'); if(txt&&txt.trim().length>30) return txt;}
                const mc = Array.from(document.querySelectorAll('.modal.show .modal-content, .modal-content')); if(mc.length>0) return mc.map(c=>c.innerText||c.textContent).join('\\n\\n---\\n\\n'); return document.body.innerText;
            }""")
            print(f"  - modal '{txt[:40]}' => {len(modal_text)} chars | preview: {modal_text[:200].replace(chr(10),' ')}")
            safe = slug(txt)[:60]
            save_text(os.path.join(out_dir, f"INTEGRA__{safe}__{len(integrais)+1}.txt"), f"BOTÃO: {txt}\nTAMANHO: {len(modal_text)}\n\n{modal_text}")
            # tenta html do modal também
            try:
                modal_html = fr.evaluate("""() => {
                    const c=document.querySelector('.modal.show, .ui-dialog-content, div[role="dialog"]');
                    return c?c.outerHTML.slice(0,15000):'';
                }""")
                if modal_html: save_text(os.path.join(out_dir, f"INTEGRA__{safe}__{len(integrais)+1}.html"), modal_html)
            except: pass
            integrais.append({"botao":txt, "tamanho":len(modal_text)})
            # fecha
            fr.evaluate("""() => {
                const close=document.querySelector('.modal.show .btn-close, .modal.show .close, button[aria-label="Close"], .ui-dialog-titlebar-close');
                if(close){close.click(); return;}
                ['keydown','keyup'].forEach(t=>{const e=new KeyboardEvent(t,{key:'Escape',code:'Escape',keyCode:27,which:27,bubbles:true}); document.dispatchEvent(e); window.dispatchEvent(e);});
            }""")
            time.sleep(3)
        # API chain tentativa (por-numeracao-unica)
        try:
            # tenta API via fetch dentro do browser context (mantém cookies)
            api_res = fr.evaluate("""async (cnj) => {
                try{
                    const r1 = await fetch('/consultaprocessual/api/processos/por-numeracao-unica?numProcesso='+encodeURIComponent(cnj)+'&tipoProcesso=1', {credentials:'include'});
                    const t1 = await r1.text();
                    let j1=null; try{j1=JSON.parse(t1);}catch(e){j1=t1.slice(0,3000)}
                    let interno=null;
                    if(j1 && typeof j1==='object' && j1.numProcesso) interno=j1.numProcesso;
                    if(j1 && Array.isArray(j1) && j1[0] && j1[0].numProcesso) interno=j1[0].numProcesso;
                    if(!interno && j1 && j1.processo && j1.processo.numProcesso) interno=j1.processo.numProcesso;
                    let r2txt=null;
                    if(interno){
                        const r2 = await fetch('/consultaprocessual/api/processos/por-numero/movimentos?numProcesso='+encodeURIComponent(interno), {credentials:'include'});
                        r2txt = (await r2.text()).slice(0,8000);
                    }
                    return JSON.stringify({status1:r1.status, body1:(typeof j1==='string'?j1.slice(0,4000):JSON.stringify(j1).slice(0,4000)), interno, r2txt: r2txt?r2txt.slice(0,6000):null});
                }catch(e){ return JSON.stringify({error:String(e)})}
            }""", cnj)
            save_text(os.path.join(out_dir, "_API_chain_por-numeracao-unica.json"), api_res)
            print(f">>> API chain: {api_res[:600]}")
        except Exception as e:
            print(f">>> API chain erro: {e}")
        return {"body_len": len(body), "expanded": expanded, "botoes": len(botoes), "integrais": integrais}
    except Exception as e:
        print(f"ERRO {cnj}: {e}")
        import traceback; traceback.print_exc()
        return {"error": str(e)}

def scrape_2a(page, cnj):
    print(f"\n{'='*70}\n[2ª] HC/ROC — {cnj}\n{'='*70}")
    out_dir = os.path.join(OUT_BASE, slug("2A-HC-ROC__"+cnj))
    os.makedirs(out_dir, exist_ok=True)
    try:
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=60000)
        time.sleep(4)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        fr = page.query_selector("iframe#mainframe").content_frame()
        time.sleep(2)
        fr.evaluate(f"""() => {{
            const inp = Array.from(document.querySelectorAll('input')).find(i => i.name==='numeroProcesso' || i.id==='numeroProcesso');
            if(inp){{ inp.value='{cnj}'; inp.dispatchEvent(new Event('input',{{bubbles:true}})); inp.dispatchEvent(new Event('change',{{bubbles:true}})); }}
        }}""")
        time.sleep(1)
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth>0 && (b.textContent||'').toLowerCase().includes('pesquisar'));
            if(btn) btn.click();
        }""")
        time.sleep(9)
        body_res = fr.inner_text("body")
        save_text(os.path.join(out_dir, "busca_RESUMO.html"), fr.evaluate("document.documentElement.outerHTML"))
        save_text(os.path.join(out_dir, "busca_RESUMO.txt"), body_res)
        try: page.screenshot(path=os.path.join(out_dir, "busca_RESUMO.png"), full_page=True)
        except: pass
        print(body_res[:6000])
        links = fr.evaluate("""() => Array.from(document.querySelectorAll('table a')).map(a=>({text:(a.textContent||'').trim(), href:a.getAttribute('href')||''})).slice(0,20)""")
        print(f">>> Links tabela 2ª: {links}")
        # abrir cada alvo (os dois números internos do TJRJ para esse CNJ)
        for alvo in ["2026.059.10770", "2026.141.00580"]:
            print(f"\n--- Abrindo detalhe {alvo} ---")
            try:
                page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=60000)
                time.sleep(4)
                page.wait_for_selector("iframe#mainframe", timeout=30000)
                fr = page.query_selector("iframe#mainframe").content_frame()
                time.sleep(2)
                fr.evaluate(f"""() => {{
                    const inp = Array.from(document.querySelectorAll('input')).find(i => i.name==='numeroProcesso' || i.id==='numeroProcesso');
                    if(inp){{ inp.value='{cnj}'; inp.dispatchEvent(new Event('input',{{bubbles:true}})); inp.dispatchEvent(new Event('change',{{bubbles:true}})); }}
                }}""")
                time.sleep(1)
                fr.evaluate("""() => {
                    const btn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth>0 && (b.textContent||'').toLowerCase().includes('pesquisar'));
                    if(btn) btn.click();
                }""")
                time.sleep(9)
                # acha link pelo texto contendo alvo e clica
                clicked = fr.evaluate("""(alvo) => {
                    const a = Array.from(document.querySelectorAll('table a')).find(el => (el.textContent||'').includes(alvo));
                    if(a){ a.click(); return true;} return false;
                }""", alvo)
                if not clicked:
                    print(f"Link {alvo} não encontrado")
                    save_text(os.path.join(out_dir, f"DETALHE_{slug(alvo)}__NAO_ENCONTRADO.txt"), fr.inner_text("body"))
                    continue
                time.sleep(9)
                fr = page.query_selector("iframe#mainframe").content_frame()
                try: fr.evaluate("""() => {
                    const btn = Array.from(document.querySelectorAll('button')).find(b => (b.textContent||'').toLowerCase().includes('todos os movimentos'));
                    if(btn) btn.click();
                }""")
                except: pass
                time.sleep(7)
                body = fr.inner_text("body")
                html = fr.evaluate("document.documentElement.outerHTML")
                save_text(os.path.join(out_dir, f"DETALHE_{slug(alvo)}.html"), html)
                save_text(os.path.join(out_dir, f"DETALHE_{slug(alvo)}.txt"), body)
                try: page.screenshot(path=os.path.join(out_dir, f"DETALHE_{slug(alvo)}.png"), full_page=True)
                except: pass
                print(body[:8000])
                # integrais da ficha 2ª (raro, mas tenta)
                botoes = fr.evaluate("""() => {
                    const t_exatos = ['ver íntegra do(a) decisão (original)','ver íntegra do(a) decisão (simplificado)','ver íntegra','visualizar ato assinado digitalmente','visualizar ato'];
                    return Array.from(document.querySelectorAll('a, button')).filter(el => el.offsetWidth>0 && el.offsetHeight>0).filter(el => {
                        const t=(el.textContent||'').toLowerCase().trim(); return t_exatos.some(te=>t.startsWith(te)||t===te);
                    }).map(el=>({text:(el.textContent||'').trim()}))
                }""")
                print(f">>> Botões íntegra detalhe {alvo}: {len(botoes)} { [b['text'][:50] for b in botoes]}")
                for b in botoes:
                    txt=b["text"]
                    fr.evaluate("""(t) => {
                        const a=Array.from(document.querySelectorAll('a, button')).find(el=>el.offsetWidth>0 && (el.textContent||'').trim()===t);
                        if(a) a.click();
                    }""", txt)
                    try: fr.wait_for_selector('.modal-body, .ui-dialog-content, div[role="dialog"], .modal.show', timeout=8000, state="visible")
                    except: pass
                    time.sleep(4)
                    mt=fr.evaluate("""() => {
                        const cs=Array.from(document.querySelectorAll('.modal-body, .ui-dialog-content, div[role="dialog"] .modal-body, .modal.show .modal-body')).filter(c=>c.offsetWidth>0);
                        if(cs.length>0) return cs.map(c=>c.innerText||c.textContent).join('\\n\\n---\\n\\n');
                        const mc=Array.from(document.querySelectorAll('.modal.show .modal-content')); if(mc.length>0) return mc.map(c=>c.innerText).join('\\n---\\n'); return document.body.innerText;
                    }""")
                    safe=slug(txt)[:50]
                    save_text(os.path.join(out_dir, f"INTEGRA__{slug(alvo)}__{safe}.txt"), mt)
                    fr.evaluate("""() => {
                        const c=document.querySelector('.modal.show .btn-close, .modal.show .close, button[aria-label="Close"]');
                        if(c) c.click(); else ['keydown','keyup'].forEach(t=>{const e=new KeyboardEvent(t,{key:'Escape',code:'Escape',keyCode:27,which:27,bubbles:true}); document.dispatchEvent(e); window.dispatchEvent(e);});
                    }""")
                    time.sleep(2)
            except Exception as e:
                print(f"Erro detalhe {alvo}: {e}")
                import traceback; traceback.print_exc()
    except Exception as e:
        print(f"ERRO 2ª: {e}")
        import traceback; traceback.print_exc()

def check_djerj(page):
    print(f"\n{'='*70}\n[DJERJ novo consultadje] 01/08 a 15/08/2026\n{'='*70}")
    out_dir = os.path.join(OUT_BASE, "_DJERJ_consultadje")
    os.makedirs(out_dir, exist_ok=True)
    for proc in ["0023013-51.2021.8.19.0078","0022975-39.2021.8.19.0078","0029845-67.2026.8.19.0000","0001140-87.2024.8.19.0078","0001492-25.2016.8.19.0046"]:
        url = f"https://www3.tjrj.jus.br/consultadje/Result.aspx?dtInicio=01%2F08%2F2026&dtFim=15%2F08%2F2026&txtPesq={proc}&tipoPesq=PROC"
        print(f"\n>> {proc}")
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            time.sleep(5)
            body = page.evaluate("document.body.innerText")
            html = page.content()
            save_text(os.path.join(out_dir, slug(proc)+".html"), html)
            save_text(os.path.join(out_dir, slug(proc)+".txt"), body)
            print(body[:3500])
            if "Não foram encontradas" in body:
                print(">>> SEM publicação")
            else:
                print(">>> POSSÍVEL publicação!")
        except Exception as e:
            print(f"Erro DJERJ {proc}: {e}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled","--no-sandbox"])
    ctx = browser.new_context(viewport={"width":1366,"height":900}, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/127.0.0.0 Safari/537.36", locale="pt-BR")
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});")
    page = ctx.new_page()
    for cnj, label in PROCS_1A:
        scrape_1a(page, cnj, label)
        time.sleep(2)
    scrape_2a(page, PROC_2A)
    time.sleep(2)
    check_djerj(page)
    browser.close()
print(f"\n=== FIM VARREDURA — saída em {OUT_BASE} ===")
