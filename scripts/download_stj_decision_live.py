# -*- coding: utf-8 -*-
import time, os, sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\04_RECURSOS_SUPERIORES_STJ\01_Decisoes"
os.makedirs(OUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(
        viewport={"width": 1366, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/127.0.0.0 Safari/537.36",
        locale="pt-BR",
        accept_downloads=True
    )
    ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
    page = ctx.new_page()

    # Visitar busca inicial
    url_home = "https://processo.stj.jus.br/processo/pesquisa/?aplicacao=processos.ea"
    print(f">> Acessando: {url_home}")
    page.goto(url_home, wait_until="domcontentloaded", timeout=45000)
    time.sleep(3)

    inp = page.query_selector("input#num_registro, input[name='parametroNumeroRegistro'], input[name='num_registro']")
    if not inp:
        inp = page.query_selector("input[type='text']")
        
    if inp:
        print(">> Buscando 202603112107...")
        inp.fill("202603112107")
        time.sleep(1)
        btn = page.query_selector("input#btnPesquisar, button#btnPesquisar, input[type='submit']")
        if btn:
            btn.click()
        else:
            inp.press("Enter")
        time.sleep(5)

        # Clicar na aba Decisões
        dec_btn = page.locator("a:has-text('Decisões'), [id*='decis'], [href*='decis']")
        if dec_btn.count() > 0:
            print(">> Clicando na aba Decisões...")
            dec_btn.first.click()
            time.sleep(4)
            print(f">> URL Decisões: {page.url}")
            
            # Procurar links de documentos ou decisões
            doc_links = page.evaluate("""() => {
                return Array.from(document.querySelectorAll('a')).map(a => ({
                    text: (a.textContent||'').trim(),
                    href: a.href,
                    onclick: a.getAttribute('onclick')
                })).filter(x => x.href.includes('documento') || x.href.includes('decisao') || (x.onclick && x.onclick.includes('documento')))
            }""")
            print(f">> Encontrados {len(doc_links)} links de decisão:")
            for dl in doc_links:
                print("   Link:", dl)
                
            page.screenshot(path=os.path.join(OUT_DIR, "STJ_Aba_Decisoes_Print.png"), full_page=True)
            txt = page.inner_text("body")
            with open(os.path.join(OUT_DIR, "STJ_Aba_Decisoes_Texto.txt"), "w", encoding="utf-8") as f:
                f.write(txt)
                
    browser.close()
