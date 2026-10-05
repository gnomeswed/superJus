# -*- coding: utf-8 -*-
"""
SUPERJUS — DJERJ Result.aspx — busca publicações de Leandro da Silva
Processo: 0827233-23.2026.8.19.0001
Período: 01/08/2026 a 04/09/2026
"""
import time, sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

PROC = "0827233-23.2026.8.19.0001"
DT_INI = "01/08/2026"
DT_FIM = "04/09/2026"

url = (f"https://www3.tjrj.jus.br/consultadje/Result.aspx"
       f"?dtInicio={DT_INI.replace('/', '%2F')}"
       f"&dtFim={DT_FIM.replace('/', '%2F')}"
       f"&txtPesq={PROC}"
       f"&tipoPesq=PROC")
print("URL:", url, flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(
        viewport={"width": 1366, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        time.sleep(8)
        body = page.evaluate("document.body.innerText")
        print("=== RESULTADO DJERJ LEANDRO ===", flush=True)
        print(body[:6000], flush=True)
        
        # Salvar resultado
        out_dje = r"c:\Projetos\superJus\Clientes\Leandro_Mecanico\djerj_leandro_ago_set_2026.txt"
        with open(out_dje, "w", encoding="utf-8") as f:
            f.write(body)
        print(f"Salvo em {out_dje}", flush=True)

        links = page.evaluate("Array.from(document.querySelectorAll('a')).map(a => (a.textContent||'').trim()+' => '+(a.href||'')).filter(s=>s.length>15).slice(0,25)")
        print("=== LINKS ===", flush=True)
        for l in links:
            print(l, flush=True)
    except Exception as e:
        print(f"Erro DJERJ: {e}", flush=True)
    browser.close()
