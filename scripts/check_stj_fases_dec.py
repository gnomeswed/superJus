# -*- coding: utf-8 -*-
import time, sys, re
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

URL = "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo=202603112107&totalRegistrosPorPagina=40&aplicacao=processos.ea"
print("=== STJ — checando abas Fases e Decisões ===")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox","--disable-blink-features=AutomationControlled","--disable-dev-shm-usage"])
    ctx = browser.new_context(
        viewport={"width":1366,"height":900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        locale="pt-BR",
    )
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});")
    page = ctx.new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=50000)
    time.sleep(7)
    # tenta clicar em Fases
    for tab in ["Fases", "Decisões", "Decisoes", "Petições"]:
        try:
            clicked = page.evaluate("""(name) => {
                const els = Array.from(document.querySelectorAll('a, button, span, li'));
                for(const e of els){
                    const t=(e.textContent||'').trim();
                    if(t.toLowerCase()===name.toLowerCase() && e.offsetWidth>0){ e.click(); return t; }
                }
                for(const e of els){
                    const t=(e.textContent||'').trim();
                    if(t.toLowerCase().includes(name.toLowerCase()) && e.offsetWidth>0 && t.length<30){ e.click(); return t; }
                }
                return null;
            }""", tab)
            print(f"TAB {tab}: clicked={clicked}")
            time.sleep(5)
            txt = page.evaluate("document.body.innerText")
            # extrai trecho relevante
            # procura por datas 2026
            dates = re.findall(r'\d{2}/\d{2}/2026[^\n]{0,120}', txt)
            print(f"  datas encontradas: {dates[:10]}")
            # procura por conclusos/decisao
            for kw in ["CONCLUSOS", "Decisão", "Petição", "Parecer", "MPF", "Vista"]:
                if kw.lower() in txt.lower():
                    idx = txt.lower().find(kw.lower())
                    print(f"  [{kw}] ...{txt[max(0,idx-80):idx+250].replace(chr(10),' | ')}")
            print(f"  body chars: {len(txt)} | preview 800: {txt[:800].replace(chr(10),' | ')}")
            page.screenshot(path=f"C:\Projetos\superJus\_stj_{tab}.png", full_page=True)
            if tab=="Fases":
                # extrai tabela
                rows = page.evaluate("""() => {
                    const trs = Array.from(document.querySelectorAll('table tr'));
                    return trs.slice(0,20).map(tr => Array.from(tr.querySelectorAll('td,th')).map(c=>c.innerText.trim().slice(0,180)).join(' | ')).filter(s=>s.trim());
                }""")
                print("  TABELA FASES:")
                for r in rows[:15]:
                    print(f"    {r}")
            if tab=="Decisões" or tab=="Decisoes":
                rows = page.evaluate("""() => {
                    const trs = Array.from(document.querySelectorAll('table tr'));
                    return trs.slice(0,20).map(tr => Array.from(tr.querySelectorAll('td,th')).map(c=>c.innerText.trim().slice(0,200)).join(' | ')).filter(s=>s.trim());
                }""")
                print("  TABELA DECISOES:")
                for r in rows[:15]:
                    print(f"    {r}")
        except Exception as e:
            print(f"  ERRO tab {tab}: {e}")
    browser.close()
print("=== FIM ===")
