# -*- coding: utf-8 -*-
import urllib.request
import ssl
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

dates = ["20260805", "20260806"]
prefixes = ["4INDJETJRJ.pdf", "INTDJETJRJ.pdf", "1INDJETJRJ.pdf", "2INDJETJRJ.pdf", "JUDDJETJRJ.pdf", "EDIDJETJRJ.pdf", "ADMDJETJRJ.pdf"]

print("=== VERIFICANDO PUBLICAÇÃO DIRETA DE PDFs DJERJ (05/08 E 06/08) ===")

target_dir = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\Diarios_Oficiais"

found_any = False
for dt in dates:
    for pref in prefixes:
        fname = f"{dt}{pref}"
        urls = [
            f"https://www3.tjrj.jus.br/consultadjerj/files/{fname}",
            f"https://www3.tjrj.jus.br/consultadjerj/{fname}",
            f"https://www.tjrj.jus.br/documents/djerj/{fname}"
        ]
        for u in urls:
            try:
                req = urllib.request.Request(u, headers=headers)
                with urllib.request.urlopen(req, context=ctx, timeout=4) as resp:
                    if resp.getcode() == 200:
                        data = resp.read()
                        if len(data) > 1000 and data.startswith(b'%PDF'):
                            out_p = os.path.join(target_dir, f"DJERJ_{fname}")
                            with open(out_p, "wb") as f:
                                f.write(data)
                            print(f"🎯 [BINGO!] PDF DJERJ encontrado: {fname} ({len(data)} bytes) -> {out_p}")
                            found_any = True
                            
                            # Search for Julio's process in the downloaded PDF
                            import re
                            if b'0023013' in data or b'163342' in data or b'203902' in data or b'JULIO PEREIRA' in data.upper():
                                print(f"🔥 CITAÇÃO DO JÚLIO ENCONTRADA NO ARQUIVO {fname}!")
            except Exception:
                pass

if not found_any:
    print("ℹ️ Os PDFs da edição de hoje/amanhã ainda não foram veiculados de forma aberta via URL direta ou dependem da disponibilização formal de fim de expediente.")

print("=== FIM DA CHECAGEM DA EDIÇÃO ===")
