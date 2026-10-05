import sys, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
# -*- coding: utf-8 -*-
import json
import urllib.request
import ssl

url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

payload = {
    "query": {
        "match": {
            "numeroProcesso": "00230135120218190078"
        }
    }
}

print("Executando consulta direta ao DataJud TJRJ...")
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        hits = res.get('hits', {}).get('hits', [])
        print(f"\n========================================================")
        print(f"🎉 SUCESSO CONFIRMADO! Encontrados {len(hits)} registro(s) no DataJud!")
        print(f"========================================================\n")
        if hits:
            src = hits[0]['_source']
            print(f"• Processo: {src.get('numeroProcesso')}")
            print(f"• Classe Processual: {src.get('classe', {}).get('nome')}")
            print(f"• Órgão Julgador: {src.get('orgaoJulgador', {}).get('nome')}")
            print(f"• Data de Ajuizamento: {src.get('dataAjuizamento')}")
            print(f"• Última Atualização: {src.get('dataHoraUltimaAtualizacao')}")
            print(f"• Total de Movimentações: {len(src.get('movimentos', []))}")
            print("\nÚltimas movimentações:")
            for m in src.get('movimentos', [])[:3]:
                print(f"  - {m.get('dataHora')[:19].replace('T', ' ')} | {m.get('nome')}")
            
            with open("resultado_positivo_datajud.json", "w", encoding="utf-8") as f:
                json.dump(src, f, indent=2, ensure_ascii=False)
except Exception as e:
    print(f"Erro: {e}")
