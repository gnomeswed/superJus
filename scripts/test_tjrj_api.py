import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www3.tjrj.jus.br/consultaprocessual/api/processos/por-numeracao-unica"
headers = {
    "Content-Type": "application/json",
    "Origin": "https://www3.tjrj.jus.br",
    "Referer": "https://www3.tjrj.jus.br/consultaprocessual/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

for proc in ["0023013-51.2021.8.19.0078", "0001140-87.2024.8.19.0078", "0022975-39.2021.8.19.0078", "0029845-67.2026.8.19.0000"]:
    tipo = "1" if not proc.startswith("0029845") else "2"
    payload = json.dumps({"tipoProcesso": tipo, "codigoProcesso": proc}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            data = json.loads(r.read().decode("utf-8"))
            print(f"\n=== Processo {proc} (tipo {tipo}) ===")
            print("Status:", r.status)
            print("Resposta:", json.dumps(data, ensure_ascii=False, indent=2)[:800])
    except Exception as e:
        print(f"Erro {proc}: {e}")
