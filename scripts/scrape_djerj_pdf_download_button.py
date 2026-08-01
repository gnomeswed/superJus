# -*- coding: utf-8 -*-
import time
import os
import fitz # PyMuPDF
from playwright.sync_api import sync_playwright

target_desktop_pdf = r"C:\Users\Administrator\Desktop\20260729_Caderno_Judicial_1Instancia.pdf"

print("=== BAIXANDO CADERNO JUDICIAL DE 1ª INSTÂNCIA VIA PLAYWRIGHT ===")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    # Navegar para o portal TJRJ para encontrar a área de downloads do DJERJ
    print("Acessando consulta pública do TJRJ para navegação...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
    time.sleep(3)
    
    # Verificar se conseguimos acessar a tela de downloads de cadernos do DJERJ
    print("Testando navegação na central de diários do TJRJ...")
    
    # Tentar abrir formulário do DJERJ
    page.goto("https://www3.tjrj.jus.br/consultadjerj/", timeout=20000)
    time.sleep(3)
    
    browser.close()

if os.path.exists(target_desktop_pdf):
    print(f"\nPDF baixado no Desktop: {target_desktop_pdf}")
    doc = fitz.open(target_desktop_pdf)
    print(f"Total de páginas: {len(doc)}")
    terms = ["0023013-51", "0022975-39", "Júlio Pereira Marcos", "Julio Pereira Marcos", "Vitor Vale", "Búzios"]
    for p_idx in range(len(doc)):
        txt = doc[p_idx].get_text("text")
        for t in terms:
            if t.lower() in txt.lower():
                print(f"🎯 [BINGO!] Página {p_idx+1} — Termo '{t}'")
                print(txt[:1500])
else:
    print("Download dinâmico requer interação direta no navegador.")
