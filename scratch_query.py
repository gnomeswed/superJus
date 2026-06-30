import json, urllib.request

DATAJUD_API_KEY = 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=='
url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjes/_search'
headers = {'Authorization': DATAJUD_API_KEY, 'Content-Type': 'application/json'}
data = json.dumps({'query': {'match': {'numeroProcesso': '00020482720208080035'}}}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers=headers)
with urllib.request.urlopen(req) as response:
    result = json.loads(response.read().decode('utf-8'))
    hits = result.get('hits', {}).get('hits', [])
    if hits:
        source = hits[0]['_source']
        print('Partes:')
        for polo in source.get('polos', []):
            for parte in polo.get('partes', []):
                print(f"- {polo.get('polo', 'N/A')}: {parte.get('pessoa', {}).get('nome', 'N/A')}")
        
        print('\nBuscando VEP pelo nome do passivo...')
        nome_reu = None
        for polo in source.get('polos', []):
            if polo.get('polo') == 'PA': # Polo Passivo
                nome_reu = polo.get('partes', [])[0].get('pessoa', {}).get('nome')
                break
        
        if nome_reu:
            url_search = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjes/_search'
            data_search = json.dumps({
                "query": {
                    "bool": {
                        "must": [
                            {"match_phrase": {"polos.partes.pessoa.nome": nome_reu}},
                            {"match": {"classe.nome": "Execução da Pena"}}
                        ]
                    }
                }
            }).encode('utf-8')
            req2 = urllib.request.Request(url_search, data=data_search, headers=headers)
            try:
                with urllib.request.urlopen(req2) as resp2:
                    res2 = json.loads(resp2.read().decode('utf-8'))
                    hits2 = res2.get('hits', {}).get('hits', [])
                    print(f"Processos de execução encontrados: {len(hits2)}")
                    for h in hits2:
                        print(h['_source']['numeroProcesso'])
            except Exception as e:
                print("Erro na busca VEP:", e)
