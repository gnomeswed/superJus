# -*- coding: utf-8 -*-
import time, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

PROC="0001140-87.2024.8.19.0078"
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled","--no-sandbox"])
    ctx=browser.new_context(viewport={"width":1366,"height":900}, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/127.0.0.0 Safari/537.36")
    page=ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=45000)
    time.sleep(3)
    page.wait_for_selector("iframe#mainframe", timeout=30000)
    fr=page.query_selector("iframe#mainframe").content_frame()
    time.sleep(2)
    fr.evaluate(f"""() => {{
        const inp=Array.from(document.querySelectorAll('input')).find(i=>i.name==='numeroProcesso'||i.id==='numeroProcesso');
        if(inp){{ inp.value='{PROC}'; inp.dispatchEvent(new Event('input',{{bubbles:true}})); inp.dispatchEvent(new Event('change',{{bubbles:true}})); }}
    }}""")
    time.sleep(1)
    fr.evaluate("""() => { const btn=Array.from(document.querySelectorAll('button')).find(b=>b.offsetWidth>0&&(b.textContent||'').toLowerCase().includes('pesquisar')); if(btn) btn.click(); }""")
    time.sleep(7)
    body1=fr.inner_text("body")
    print("=== RESUMO ===")
    print(body1[:6000])
    print("\n=== TENTANDO TODOS OS MOVIMENTOS ===")
    try:
        clicked = fr.evaluate("""() => {
            const btn=Array.from(document.querySelectorAll('button')).find(b=>(b.textContent||'').toLowerCase().includes('todos os movimentos'));
            if(btn){ btn.click(); return true; } return false;
        }""")
        print(f"Clicked todos movimentos: {clicked}")
        time.sleep(7)
        body2=fr.inner_text("body")
        print(body2[:15000])
        print(f"\nBody len: {len(body2)} | Movimentos: {body2.count('Tipo do Movimento')}")
    except Exception as e:
        print(f"Erro todos movimentos: {e}")
    botoes=fr.evaluate("""() => {
        return Array.from(document.querySelectorAll('a, button')).filter(el=>el.offsetWidth>0&&el.offsetHeight>0).map(el=> (el.textContent||'').trim()).filter(t=> t.length>0 && t.length<80).slice(0,40);
    }""")
    print("\n=== BOTOES VISIVEIS ===")
    for b in botoes:
        print(repr(b))
    browser.close()
