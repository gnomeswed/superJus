# -*- coding: utf-8 -*-
import urllib.request
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")

url = "https://tjrj.pje.jus.br:443/pje/ConsultaPublica/DetalheProcessoConsultaPublica/documentoSemLoginHTML.seam?ca=4a247d1cb6b5d70efb49632a1a9c2981bb17ad1d126a7141688df8af4889ac55d67699f5e5c3915cbfe2e31a6753fddcdaab9db4fbc6c8b0&idProcessoDoc=299734030"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text("\n", strip=True)
        print("=== TEOR COMPLETO DA DECISÃO DE 10/08/2026 ===")
        print(text)
        with open(r"c:\Projetos\superJus\Clientes\Lucas_Dias_Oliveira\03_Documentos_do_Processo\decisao_10_08_2026_integra.txt", "w", encoding="utf-8") as f:
            f.write(text)
except Exception as e:
    print(f"Erro ao baixar: {e}")
