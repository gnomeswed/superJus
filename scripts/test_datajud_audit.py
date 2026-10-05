import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

def query_datajud(tribunal, proc_clean):
    url = f"https://api-publica.datajud.cnj.jus.br/api_publica_{tribunal}/_search"
    payload = {
        "query": {
            "match": {
                "numeroProcesso": proc_clean
            }
        },
        "size": 2
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            res = json.loads(r.read().decode('utf-8'))
            hits = res.get('hits', {}).get('hits', [])
            return hits
    except Exception as e:
        return [f"Erro: {e}"]

# 1. TJRJ APL 0014392-14.2009.8.19.0037
print("=== Checando TJRJ APL 0014392-14.2009.8.19.0037 ===")
hits = query_datajud("tjrj", "00143921420098190037")
print(f"Hits TJRJ: {len(hits)}")
for h in hits:
    if isinstance(h, dict):
        src = h.get('_source', {})
        print("Classe:", src.get('classe', {}).get('nome'))
        print("Órgão:", src.get('orgaoJulgador', {}).get('nome'))
        print("Data Ajuizamento:", src.get('dataAjuizamento'))

# 2. STF HC 233825
print("\n=== Checando STF HC 233825 ===")
url_stf = "https://api-publica.datajud.cnj.jus.br/api_publica_stf/_search"
req_stf = urllib.request.Request(url_stf, data=json.dumps({"query": {"query_string": {"query": "233825"}}, "size": 2}).encode('utf-8'), headers=headers)
try:
    with urllib.request.urlopen(req_stf, timeout=10, context=ctx) as r:
        res = json.loads(r.read().decode('utf-8'))
        hits_stf = res.get('hits', {}).get('hits', [])
        print(f"Hits STF: {len(hits_stf)}")
        for h in hits_stf:
            src = h.get('_source', {})
            print("Processo:", src.get('numeroProcesso'))
            print("Classe:", src.get('classe', {}).get('nome'))
            print("Relator/Órgão:", src.get('orgaoJulgador', {}).get('nome'))
except Exception as e:
    print(f"Erro STF: {e}")
