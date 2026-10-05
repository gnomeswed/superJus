import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://portal.stf.jus.br/processos/listarProcessos.asp?numeroProcesso=233825&classe=HC"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=12) as r:
        html = r.read().decode("utf-8", errors="ignore")
        print("Tamanho resposta STF:", len(html))
        m = re.findall(r"MENDONÇA|Mendonça", html)
        print("Mendonça encontrado:", len(m))
        incidents = re.findall(r"incidente=(\d+)", html)
        print("Incidentes encontrados:", list(set(incidents)))
        # Search snippets
        for line in html.splitlines():
            if any(k in line for k in ["Mendonça", "HC 233", "233825", "detração"]):
                print("Line:", line.strip()[:160])
except Exception as e:
    print("Erro ao consultar STF:", e)
