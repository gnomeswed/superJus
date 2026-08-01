# -*- coding: utf-8 -*-
import urllib.request
import ssl
import os
import fitz # PyMuPDF

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

date_str = "20260729"
target_dir = r"C:\Users\Administrator\Desktop"
out_pdf_name = f"{date_str}1INDJETJRJ.pdf"
out_pdf_path = os.path.join(target_dir, out_pdf_name)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://www3.tjrj.jus.br/consultadjerj/'
}

urls_to_try = [
    f"https://www3.tjrj.jus.br/consultadjerj/files/{out_pdf_name}",
    f"https://www3.tjrj.jus.br/consultadjerj/Paginas/{out_pdf_name}",
    f"https://www3.tjrj.jus.br/consultadjerj/pdf/{out_pdf_name}",
    f"https://www3.tjrj.jus.br/consultadjerj/{out_pdf_name}",
    f"https://www.tjrj.jus.br/documents/djerj/{out_pdf_name}"
]

print(f"=== TENTANDO DOWNLOAD DIRETO DO CADERNO JUDICIAL 1ª INSTÂNCIA ({out_pdf_name}) ===")

success = False
for u in urls_to_try:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = resp.read()
            if len(data) > 2000 and data.startswith(b'%PDF'):
                with open(out_pdf_path, "wb") as f:
                    f.write(data)
                print(f"🎯 [BINGO!] Sucesso ao baixar {u} ({len(data)} bytes) -> {out_pdf_path}")
                success = True
                break
            else:
                print(f"[Falha] Resposta de {u} não é um PDF válido (Tamanho: {len(data)})")
    except Exception as e:
        print(f"[Erro] {u}: {e}")

if not success:
    print("Tentando via Playwright navegando na central de downloads do TJRJ...")
    from playwright.sync_api import sync_playwright
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            ctx_pw = browser.new_context(viewport={"width": 1280, "height": 800})
            page = ctx_pw.new_page()
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
            print("Página da consulta pública acessada.")
            browser.close()
    except Exception as e_pw:
        print(f"Erro Playwright: {e_pw}")

if os.path.exists(out_pdf_path):
    print(f"\nAnalizando o PDF {out_pdf_path}...")
    doc = fitz.open(out_pdf_path)
    print(f"Total de páginas no Caderno Judicial 1ª Instância: {len(doc)}")
    terms = ["0023013-51", "0022975-39", "Júlio Pereira Marcos", "Julio Pereira Marcos", "Vitor Vale", "Búzios"]
    found = False
    for p_idx in range(len(doc)):
        txt = doc[p_idx].get_text("text")
        for t in terms:
            if t.lower() in txt.lower():
                found = True
                print(f"\n🎯 [BINGO NO CADERNO JUDICIAL 1ª INSTÂNCIA!] Página {p_idx+1} — Termo: '{t}'")
                print("="*60)
                print(txt)
                print("="*60)
    if not found:
        print("Termos do Júlio não encontrados no arquivo baixado.")
