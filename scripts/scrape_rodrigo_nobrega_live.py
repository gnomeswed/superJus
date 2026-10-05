# -*- coding: utf-8 -*-
import time
import os
import sys
import json
import re
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

nome = "Rodrigo dos Reis Nobrega"
nome_acentuado = "Rodrigo dos Reis Nóbrega"

target_dir = r"c:\Projetos\superJus\Clientes\Rodrigo_Nobrega"
os.makedirs(target_dir, exist_ok=True)

print(f"=== BUSCA AO VIVO NO PORTAL TJRJ E PJe: {nome_acentuado} (Saquarema) ===")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 900}
    )
    page = context.new_page()

    # 1. PJe TJRJ
    url_pje = "https://tjrj.pje.jus.br/pje/ConsultaPublica/listView.seam"
    print(f"\n1. Acessando PJe TJRJ: {url_pje}...")
    try:
        page.goto(url_pje, wait_until="domcontentloaded", timeout=25000)
        time.sleep(2)
        
        nome_input = page.query_selector("input[id*='nomeParte'], input[id*='NomeParte']")
        if nome_input:
            nome_input.fill(nome)
            
        time.sleep(1)
        btn = page.query_selector("input[id*='search'], input[value='Pesquisar'], button:has-text('Pesquisar')")
        if btn:
            btn.click()
            time.sleep(6)
            
        pje_txt = page.inner_text("body")
        page.screenshot(path=os.path.join(target_dir, "pje_resultado_rodrigo.png"))
        with open(os.path.join(target_dir, "pje_resultado_rodrigo.txt"), "w", encoding="utf-8") as f:
            f.write(pje_txt)
            
        print("   • Resultado PJe capturado:")
        lines = [l.strip() for l in pje_txt.splitlines() if l.strip()]
        for l in lines[:25]:
            print(f"     [PJe] {l[:120]}")
    except Exception as e:
        print(f"   ❌ Erro no PJe: {e}")

    # 2. PORTAL TJRJ POR NOME (1ª INSTÂNCIA - SAQUAREMA / GERAL)
    url_portal = "https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica"
    print(f"\n2. Acessando Portal TJRJ: {url_portal}...")
    try:
        page.goto(url_portal, wait_until="domcontentloaded", timeout=30000)
        time.sleep(4)
        
        iframe_el = page.query_selector("iframe#mainframe, iframe")
        if iframe_el:
            frame = iframe_el.content_frame()
            if frame:
                # Clicar Por Nome
                frame.evaluate("""() => {
                    const el = Array.from(document.querySelectorAll('*')).find(e => e.textContent && e.textContent.trim() === 'Por Nome');
                    if (el) el.click();
                }""")
                time.sleep(1)
                
                inp_nome = frame.query_selector("input[name='nomeParte']")
                if inp_nome:
                    inp_nome.fill(nome)
                    
                # Desmarcar somente em andamento
                chk = frame.query_selector("input[name='procEmAndamento']")
                if chk and chk.is_checked():
                    chk.uncheck()
                    
                time.sleep(1)
                frame.evaluate("""() => {
                    const btns = Array.from(document.querySelectorAll('button'));
                    const btn = btns.find(b => b.textContent && b.textContent.trim().toLowerCase().includes('pesquisar'));
                    if (btn) btn.click();
                }""")
                
                print("   • Pesquisa no Portal TJRJ enviada. Aguardando resultados...")
                time.sleep(10)
                
                frame_txt = frame.evaluate("document.body.innerText")
                page.screenshot(path=os.path.join(target_dir, "portal_tjrj_rodrigo.png"))
                with open(os.path.join(target_dir, "portal_tjrj_rodrigo.txt"), "w", encoding="utf-8") as f:
                    f.write(frame_txt)
                    
                print("   • Resultado Portal TJRJ capturado:")
                lines_port = [l.strip() for l in frame_txt.splitlines() if l.strip()]
                for l in lines_port[:35]:
                    print(f"     [Portal TJRJ] {l[:120]}")
    except Exception as e:
        print(f"   ❌ Erro Portal TJRJ: {e}")

    browser.close()

print("\n=== BUSCA AO VIVO CONCLUÍDA ===")
