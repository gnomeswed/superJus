# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

print("=== DECODIFICAÇÃO DE CONSULTA PÚBLICA PJe — LEANDRO DA SILVA ===")

url_pub = "https://tjrj.pje.jus.br/pje/ConsultaPublica/listView.seam"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

try:
    req = urllib.request.Request(url_pub, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print(f"✅ Conexão estabelecida com PJe Consulta Pública! Tamanho da página: {len(html)} bytes")
        
        # Extrair ViewState do JSF
        vs_match = re.search(r'name="javax\.faces\.ViewState" id=".*?" value="(.*?)"', html)
        if vs_match:
            viewstate = vs_match.group(1)
            print(f"   • ViewState JSF capturado: {viewstate[:30]}...")
        else:
            print("   • ViewState JSF não encontrado diretamente no HTML.")
            
except Exception as e:
    print(f"Erro ao conectar com PJe: {e}")

print("\n=== CONSULTA FINALIZADA ===")
