import urllib.request
import json

DATAJUD_API_KEY = 'cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=='
headers = {'Authorization': f'APIKey {DATAJUD_API_KEY}', 'Content-Type': 'application/json'}

procs = {
    'Principal_1A_Buzios': '00230135120218190078',
    'Apenso_1A_Buzios': '00011408720248190078',
    'Original_1A_Buzios': '00229753920218190078',
    '2A_TJRJ_HC_ROC': '00298456720268190000'
}

for name, cnj in procs.items():
    url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
    payload = json.dumps({'query': {'match': {'numeroProcesso': cnj}}, 'size': 5}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        hits = data.get('hits', {}).get('hits', [])
        print(f'=== {name} ({cnj}) ===')
        for h in hits:
            src = h['_source']
            print('Orgao:', src.get('orgaoJulgador', {}).get('nome'))
            print('Classe:', src.get('classe', {}).get('nome'))
            print('Ultima Atualizacao:', src.get('dataHoraUltimaAtualizacao'))
            movs = sorted(src.get('movimentos', []), key=lambda m: m.get('dataHora', ''), reverse=True)
            print(f'Total movs: {len(movs)}')
            for m in movs[:8]:
                comps = m.get('complementosTabelados', [])
                comp_list = []
                for c in comps:
                    comp_list.append(str(c.get('nome')) + ': ' + str(c.get('descricao')))
                comp_str = (' | ' + ', '.join(comp_list)) if comp_list else ''
                print(f"  - {m.get('dataHora')} | {m.get('nome')}{comp_str}")
        print()
