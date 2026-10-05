import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url_mov = "https://www3.tjrj.jus.br/consultaprocessual/api/processos/por-numero/movimentos"
headers = {
    "Content-Type": "application/json",
    "Origin": "https://www3.tjrj.jus.br",
    "Referer": "https://www3.tjrj.jus.br/consultaprocessual/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

tests = [
    (1, "2021.078.023002-1", "Principal Júlio"),
    (1, "2024.078.001138-0", "Apenso RSE"),
    (1, "2021.078.022964-0", "Originário"),
    (2, "2026.059.10770", "HC 7ª Camara"),
    (2, "2026.141.00580", "ROC 2ª Vice")
]

for tipo, cod, desc in tests:
    payload = json.dumps({
        "tipoProcesso": tipo,
        "codigoProcesso": cod,
        "indProcVolumoso": "N",
        "ultimaOrdemExibida": None
    }).encode("utf-8")
    req = urllib.request.Request(url_mov, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            movs = json.loads(r.read().decode("utf-8"))
            print(f"\n==========================================")
            print(f"{desc} ({cod}) - Total de Movimentos retornados: {len(movs)}")
            for m in movs[:3]:
                print(f"  • {m.get('dtMovimento')} | {m.get('descrMov')}")
                if m.get('movimentosExibicao'):
                    for sub in m['movimentosExibicao'][:2]:
                        print(f"      - {sub.get('tipoMovimento')}: {sub.get('detalhesMovimento')[:100] if sub.get('detalhesMovimento') else ''}")
    except Exception as e:
        print(f"Erro {desc} ({cod}): {e}")
