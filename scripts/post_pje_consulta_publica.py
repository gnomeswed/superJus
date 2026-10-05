# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import sys
import re
import ssl

sys.stdout.reconfigure(encoding='utf-8')

print("=== POST CONSULTA PÚBLICA PJe — PROCESSO 0827233-23.2026.8.19.0001 ===")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url_pub = "https://tjrj.pje.jus.br/pje/ConsultaPublica/listView.seam"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

# 1. GET initial page
req = urllib.request.Request(url_pub, headers=headers)
cookie_header = ""
with urllib.request.urlopen(req, context=ctx) as resp:
    cookies = resp.info().get_all('Set-Cookie')
    if cookies:
        cookie_header = "; ".join([c.split(';')[0] for c in cookies])
    html = resp.read().decode('utf-8', errors='ignore')

# Extract JSF ViewState & Form ID
vs_match = re.search(r'name="javax\.faces\.ViewState" id=".*?" value="(.*?)"', html)
viewstate = vs_match.group(1) if vs_match else ""

# 2. Form submission payload
form_data = {
    "fKss:fKss": "fKss:fKss",
    "fKss:numSequencial": "0827233",
    "fKss:numDigitoVerificador": "23",
    "fKss:ano": "2026",
    "fKss:ramoJustica": "8",
    "fKss:respectivoTribunal": "19",
    "fKss:orgaoJurisdicional": "0001",
    "fKss:btnPesquisar": "Pesquisar",
    "javax.faces.ViewState": viewstate
}

encoded_data = urllib.parse.urlencode(form_data).encode('utf-8')
headers_post = headers.copy()
headers_post["Content-Type"] = "application/x-www-form-urlencoded"
if cookie_header:
    headers_post["Cookie"] = cookie_header

req_post = urllib.request.Request(url_pub, data=encoded_data, headers=headers_post)

try:
    with urllib.request.urlopen(req_post, context=ctx) as resp_post:
        res_html = resp_post.read().decode('utf-8', errors='ignore')
        print(f"✅ Resposta do POST recebida! Tamanho: {len(res_html)} bytes")
        
        # Extrair texto limpo
        clean_text = re.sub(r'<script.*?>.*?</script>', '', res_html, flags=re.DOTALL)
        clean_text = re.sub(r'<style.*?>.*?</style>', '', clean_text, flags=re.DOTALL)
        clean_text = re.sub(r'<.*?>', ' ', clean_text)
        lines = [l.strip() for l in clean_text.split('\n') if l.strip()]
        
        print("\n--- TRECHO DA RESPOSTA DO PJe CONSULTA PÚBLICA ---")
        for l in lines[:40]:
            print(f"  • {l}")

        # Salvar em arquivo
        out_file = r"c:\Projetos\superJus\Clientes\Leandro_Mecanico\scraping_2026-08-16\pje_post_resultado.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"\n✅ Resultado em texto salvo em: {out_file}")

except Exception as e:
    print(f"Erro no POST: {e}")

print("\n=== FIM DA CONSULTA ===")
