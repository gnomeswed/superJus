# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import sys
import re
import ssl

sys.stdout.reconfigure(encoding='utf-8')

print("=== DECODIFICAÇÃO DIRETA DA CONSULTA PÚBLICA PJe — LEANDRO DA SILVA ===")

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

# Extract JSF ViewState
vs_match = re.search(r'name="javax\.faces\.ViewState" id=".*?" value="(.*?)"', html)
viewstate = vs_match.group(1) if vs_match else "j_id1"

# 2. Form submission by Process Number
form_data = {
    "fPP": "fPP",
    "fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso": "0827233-23.2026.8.19.0001",
    "fPP:searchProcessos": "Pesquisar",
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
        print(f"✅ Resposta da busca por número recebida! ({len(res_html)} bytes)")
        
        # Clean HTML tags
        clean_text = re.sub(r'<script.*?>.*.*?<\/script>', '', res_html, flags=re.DOTALL)
        clean_text = re.sub(r'<style.*?>.*.*?<\/style>', '', clean_text, flags=re.DOTALL)
        clean_text = re.sub(r'<.*?>', ' ', clean_text)
        lines = [l.strip() for l in clean_text.split('\n') if l.strip()]
        
        print("\n--- RESULTADOS ENCONTRADOS DA BUSCA POR NÚMERO ---")
        found = False
        for i, l in enumerate(lines):
            if any(w in l.upper() for w in ["LEANDRO", "0827233", "SANTA CRUZ", "PROCEDIMENTO", "RECEPTAÇÃO", "MOVIMENTAÇÃO"]):
                found = True
                print(f"  📍 [Linha {i+1}]: {l}")
                for ctx_l in lines[max(0, i-2):min(len(lines), i+5)]:
                    print(f"      {ctx_l}")
                print("-" * 50)
        
        if not found:
            print("  ⚠️ Nenhum resultado textual direto exibido na busca pública por número.")

        # Save HTML response
        out_html = r"c:\Projetos\superJus\Clientes\Leandro_Mecanico\scraping_2026-08-16\pje_consulta_resultado.html"
        with open(out_html, "w", encoding="utf-8") as f:
            f.write(res_html)

except Exception as e:
    print(f"Erro no POST por número: {e}")

# 3. Form submission by Name
form_data_name = {
    "fPP": "fPP",
    "fPP:dnp:nomeParte": "Leandro da Silva",
    "fPP:searchProcessos": "Pesquisar",
    "javax.faces.ViewState": viewstate
}

encoded_data_name = urllib.parse.urlencode(form_data_name).encode('utf-8')
req_post_name = urllib.request.Request(url_pub, data=encoded_data_name, headers=headers_post)

try:
    with urllib.request.urlopen(req_post_name, context=ctx) as resp_name:
        res_name_html = resp_name.read().decode('utf-8', errors='ignore')
        print(f"\n✅ Resposta da busca por nome recebida! ({len(res_name_html)} bytes)")
        
        clean_name = re.sub(r'<script.*?>.*.*?<\/script>', '', res_name_html, flags=re.DOTALL)
        clean_name = re.sub(r'<style.*?>.*.*?<\/style>', '', clean_name, flags=re.DOTALL)
        clean_name = re.sub(r'<.*?>', ' ', clean_name)
        lines_name = [l.strip() for l in clean_name.split('\n') if l.strip()]
        
        print("\n--- RESULTADOS ENCONTRADOS DA BUSCA POR NOME ---")
        for i, l in enumerate(lines_name):
            if any(w in l.upper() for w in ["0827233", "SANTA CRUZ", "RECEPTAÇÃO"]):
                print(f"  📍 [Linha {i+1}]: {l}")

except Exception as e:
    print(f"Erro no POST por nome: {e}")

print("\n=== CONSULTA PÚBLICA PJe CONCLUÍDA ===")
