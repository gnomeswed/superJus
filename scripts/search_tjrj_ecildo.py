# -*- coding: utf-8 -*-
import json
import urllib.request

DATAJUD_API_KEY = __import__('os').getenv('DATAJUD_API_KEY','')

def search_tjrj():
    url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
    headers = {
        "Authorization": DATAJUD_API_KEY,
        "Content-Type": "application/json"
    }
    
    # Query by name variations and CPF
    queries = [
        {"query_string": {"query": "\"Ecildo\""}},
        {"query_string": {"query": "\"080.730.972-90\""}},
        {"query_string": {"query": "\"08073097290\""}},
        {"match": {"numeroProcesso": "08073097290"}}
    ]
    
    for q in queries:
        req = urllib.request.Request(url, data=json.dumps({"query": q, "size": 50}).encode('utf-8'), headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                hits = data.get('hits', {}).get('hits', [])
                print(f"Query {q}: {len(hits)} hits em TJRJ")
                for h in hits:
                    src = h['_source']
                    print("Processo TJRJ:", src.get('numeroProcesso'), "| Classe:", src.get('classe', {}).get('nome'))
        except Exception as e:
            print(f"Error querying {q}: {e}")

search_tjrj()
