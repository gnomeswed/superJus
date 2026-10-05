# -*- coding: utf-8 -*-
import urllib.request
import ssl
import sys

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0'}

print("=== CHECAGEM RÁPIDA DE EDIÇÃO DJERJ DE HOJE (05/08) ===")

date_str = "20260805"
fname = f"{date_str}4INDJETJRJ.pdf"
url = f"https://www3.tjrj.jus.br/consultadjerj/files/{fname}"

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=3) as resp:
        if resp.getcode() == 200:
            print("EDIÇÃO DISPONÍVEL NO SISTEMA!")
        else:
            print("Edição ainda não veiculada no arquivo direto.")
except Exception:
    print("Edição do DJERJ de hoje (05/08) ainda não foi disponibilizada nos arquivos abertos do portal.")

print("=== FIM DA CONSULTA ===")
