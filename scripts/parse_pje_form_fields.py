# -*- coding: utf-8 -*-
import urllib.request
import sys
import re
import ssl

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url_pub = "https://tjrj.pje.jus.br/pje/ConsultaPublica/listView.seam"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

req = urllib.request.Request(url_pub, headers=headers)
with urllib.request.urlopen(req, context=ctx) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# Find all form inputs
inputs = re.findall(r'<input.*?>', html)
print("=== CAMPOS ENCONTRADOS NA TELA DE CONSULTA PÚBLICA DO PJe ===")
for inp in inputs:
    name_m = re.search(r'name="(.*?)"', inp)
    id_m = re.search(r'id="(.*?)"', inp)
    type_m = re.search(r'type="(.*?)"', inp)
    val_m = re.search(r'value="(.*?)"', inp)
    n = name_m.group(1) if name_m else "N/I"
    i = id_m.group(1) if id_m else "N/I"
    t = type_m.group(1) if type_m else "text"
    v = val_m.group(1) if val_m else ""
    print(f"  • Input id='{i}' name='{n}' type='{t}' val='{v}'")

print("\n=== FIM DOS CAMPOS ===")
