# -*- coding: utf-8 -*-
"""
Motor de Raspagem Direta no Portal do TJRJ (Playwright Headless com Stealth).
Captura os andamentos processuais oficiais em tempo real sem depender de APIs externas.
"""
import os
import sys
import time
import logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
sys.stdout.reconfigure(encoding="utf-8")

def consultar_tjrj_portal_direto(numero_processo: str):
    logging.info(f"=== CONSULTANDO PORTAL TJRJ AO VIVO PARA: {numero_processo} ===")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            viewport={"width": 1366, "height": 850}
        )
        page = ctx.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        try:
            url_portal = "https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica"
            logging.info(f"Acessando {url_portal}...")
            page.goto(url_portal, timeout=30000, wait_until="domcontentloaded")
            time.sleep(3)
            
            iframe_el = page.wait_for_selector("iframe#mainframe", timeout=15000)
            if iframe_el:
                frame = iframe_el.content_frame()
                if frame:
                    inp = frame.query_selector("input[name='numeroProcesso']")
                    if inp:
                        inp.fill(numero_processo)
                        logging.info("Número preenchido no formulário.")
                        
                        btns = frame.query_selector_all("button")
                        btn_pesquisa = None
                        for b in btns:
                            txt = b.inner_text().strip()
                            if any(w in txt.lower() for w in ["pesquisar", "buscar", "consultar"]):
                                btn_pesquisa = b
                                break
                        if not btn_pesquisa and btns:
                            btn_pesquisa = btns[0]
                            
                        if btn_pesquisa:
                            btn_pesquisa.click()
                            logging.info("Pesquisa disparada. Aguardando carregamento do processo...")
                            time.sleep(5)
                            
                            texto_resultado = frame.inner_text("body")
                            logging.info("✅ SUCESSO! Dados extraídos diretamente do Portal do TJRJ:")
                            print("\n" + "="*70)
                            print(texto_resultado[:3500])
                            print("="*70 + "\n")
                            
                            with open("tjrj_portal_captura_sucesso.txt", "w", encoding="utf-8") as f:
                                f.write(texto_resultado)
                            return True
        except Exception as e:
            logging.error(f"Erro ao acessar portal do TJRJ: {e}")
            
        browser.close()
    return False

if __name__ == "__main__":
    num = sys.argv[1] if len(sys.argv) > 1 else "0023013-51.2021.8.19.0078"
    consultar_tjrj_portal_direto(num)
