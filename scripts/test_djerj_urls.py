# -*- coding: utf-8 -*-
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    "https://www3.tjrj.jus.br/consultadjerj/ConsultaDJERJ.aspx",
    "https://www3.tjrj.jus.br/ejud/ConsultaDJERJ.aspx",
    "https://www3.tjrj.jus.br/consultadjerj/default.aspx",
    "https://www3.tjrj.jus.br/consultadjerj/paginas/consultadjerj.aspx",
    "https://www3.tjrj.jus.br/consultadjerj/Paginas/Consultas.aspx",
    "https://www3.tjrj.jus.br/consultadjerj/site/default.aspx"
]

print("=== TESTANDO URLs DO DJERJ NO TJRJ ===")
for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
            code = resp.getcode()
            print(f"[OK {code}] -> {u}")
    except Exception as e:
        print(f"[ERRO {e}] -> {u}")
