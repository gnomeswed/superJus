# -*- coding: utf-8 -*-
import urllib.request
import ssl
import fitz # PyMuPDF
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Nomes de arquivo prováveis para o Caderno IV (1ª Instância - Interior) do TJRJ em 29/07/2026
date_str = "20260729"
base_url = "https://www3.tjrj.jus.br/consultadjerj/Paginas/"

possible_files = [
    f"{date_str}4INDJETJRJ.pdf",
    f"{date_str}INTDJETJRJ.pdf",
    f"{date_str}1INDJETJRJ.pdf",
    f"{date_str}2INDJETJRJ.pdf",
    f"{date_str}JUDDJETJRJ.pdf",
    f"{date_str}EDIDJETJRJ.pdf",
    f"{date_str}ADMDJETJRJ.pdf"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

target_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"

print("=== BUSCANDO E TESTANDO DOWNLOAD DO CADERNO IV (29/07/2026) ===")

downloaded = False
for fname in possible_files:
    # Tentar diferentes caminhos de URL do TJRJ
    urls_to_try = [
        f"https://www3.tjrj.jus.br/consultadjerj/{fname}",
        f"https://www3.tjrj.jus.br/consultadjerj/files/{fname}",
        f"https://www3.tjrj.jus.br/consultadjerj/pdf/{fname}",
        f"https://www.tjrj.jus.br/documents/djerj/{fname}",
        f"https://www.tjrj.jus.br/c/document_library/get_file?uuid={fname}"
    ]
    
    for url in urls_to_try:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=6) as resp:
                if resp.getcode() == 200:
                    data = resp.read()
                    if len(data) > 1000 and data.startswith(b'%PDF'):
                        out_p = os.path.join(target_dir, f"DJERJ_{fname}")
                        with open(out_p, "wb") as f:
                            f.write(data)
                        print(f"🎯 [DOWNLOAD BINGO!] Baixado com sucesso: {url} ({len(data)} bytes) -> {out_p}")
                        downloaded = True
                        
                        # Inspecionar e buscar Júlio no PDF baixado
                        doc = fitz.open(out_p)
                        print(f"Total de páginas no PDF {fname}: {len(doc)}")
                        found = False
                        terms = ["0023013-51", "0022975-39", "Júlio Pereira Marcos", "Julio Pereira Marcos", "Vitor Vale", "Búzios"]
                        for p_idx in range(len(doc)):
                            txt = doc[p_idx].get_text("text")
                            for t in terms:
                                if t.lower() in txt.lower():
                                    found = True
                                    print(f"🎯 [BINGO NO CADERNO IV!] Página {p_idx+1} — Termo: '{t}'")
                                    print("="*50)
                                    print(txt[:2500])
                                    print("="*50)
                        if not found:
                            print(f"Termos do Júlio não encontrados nas {len(doc)} páginas do PDF {fname}.")
                        break
        except Exception:
            pass

if not downloaded:
    print("Nenhuma das URLs de PDF direto respondeu com download limpo. As publicações dependem de renderização via ASPX ou login de advogado no e-Proc.")
