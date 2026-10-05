# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8")
import urllib.request
import time

urls = [
    ("DJEN direto (VPS)", "https://comunica.pje.jus.br/"),
    ("DJEN consulta STJ", "https://comunica.pje.jus.br/consulta?siglaTribunal=STJ&meio=D"),
]

for nome, u in urls:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        t0 = time.time()
        resp = urllib.request.urlopen(req, timeout=15)
        body = resp.read(300)
        print(f"{nome}: HTTP {resp.status} em {time.time()-t0:.1f}s | {body[:100]}")
    except Exception as e:
        print(f"{nome}: {type(e).__name__}: {str(e)[:90]}")
