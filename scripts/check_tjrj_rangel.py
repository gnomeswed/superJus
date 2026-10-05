import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    "Authorization": "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==",
    "Content-Type": "application/json"
}

url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
payload = {
    "query": {
        "match": {
            "numeroProcesso": "00143921420098190037"
        }
    }
}
req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
try:
    with urllib.request.urlopen(req, timeout=12, context=ctx) as r:
        res = json.loads(r.read().decode("utf-8"))
        hits = res.get("hits", {}).get("hits", [])
        print("Hits TJRJ APL Paulo Rangel:", len(hits))
        for h in hits:
            src = h["_source"]
            print("Órgão:", src.get("orgaoJulgador", {}).get("nome"))
            print("Classe:", src.get("classe", {}).get("nome"))
except Exception as e:
    print("Erro:", e)
