import json, urllib.request

DATAJUD_API_KEY = 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=='
url = 'https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search'
headers = {'Authorization': DATAJUD_API_KEY, 'Content-Type': 'application/json'}
data = json.dumps({'query': {'match': {'numeroProcesso': '01862010920243000000'}}}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers=headers)
with urllib.request.urlopen(req) as response:
    result = json.loads(response.read().decode('utf-8'))
    hits = result.get('hits', {}).get('hits', [])
    if hits:
        source = hits[0]['_source']
        print('Partes do STJ:')
        for polo in source.get('polos', []):
            for parte in polo.get('partes', []):
                print(f"- {polo.get('polo', 'N/A')}: {parte.get('pessoa', {}).get('nome', 'N/A')}")
