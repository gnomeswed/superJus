# -*- coding: utf-8 -*-
"""
Script de Consulta DataJud Resiliente & Teste de Conexão com Múltiplos Fallbacks.
Garante recuperação de dados processuais oficiais do CNJ.
"""
import json
import urllib.request
import time
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

HEADERS = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}

def clean_num(num_str: str) -> str:
    return re.sub(r"\D", "", num_str)

def consultar_processo_datajud(processo_formatado: str):
    num_limpo = clean_num(processo_formatado)
    print(f"=== TESTANDO CONSULTA DATAJUD (CNJ) PARA: {processo_formatado} (Limpo: {num_limpo}) ===")
    
    # Determina o tribunal pelo código CNJ (caracteres 14 a 16)
    # Exemplo: 0023013-51.2021.8.19.0078 -> TR = 19 (TJRJ)
    tr_code = num_limpo[14:16] if len(num_limpo) == 20 else "19"
    
    uf_map = {
        '01': 'ac', '02': 'al', '03': 'ap', '04': 'am', '05': 'ba', '06': 'ce',
        '07': 'dft', '08': 'es', '09': 'go', '10': 'ma', '11': 'mt', '12': 'ms',
        '13': 'mg', '14': 'pa', '15': 'pb', '16': 'pr', '17': 'pe', '18': 'pi',
        '19': 'rj', '20': 'rn', '21': 'rs', '22': 'ro', '23': 'rr', '24': 'sc',
        '25': 'se', '26': 'sp', '27': 'to'
    }
    
    sigla_tj = f"tj{uf_map.get(tr_code, 'rj')}"
    endpoints = [f"api_publica_{sigla_tj}", "api_publica_stj", "api_publica_tjrj"]
    
    for ep in endpoints:
        url = f"https://api-publica.datajud.cnj.jus.br/{ep}/_search"
        payload = {
            "query": {
                "bool": {
                    "should": [
                        {"match": {"numeroProcesso": num_limpo}},
                        {"match": {"numeroProcesso": processo_formatado}}
                    ]
                }
            },
            "size": 5
        }
        
        print(f"Consultando Endpoint: {ep}...")
        try:
            req_data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(url, data=req_data, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=10) as resp:
                res = json.loads(resp.read().decode('utf-8'))
                hits = res.get('hits', {}).get('hits', [])
                if hits:
                    print(f"✅ SUCESSO ABSOLUTO! {len(hits)} registro(s) retornado(s) de {ep}!")
                    src = hits[0]['_source']
                    print(f"  • Processo: {src.get('numeroProcesso')}")
                    print(f"  • Classe: {src.get('classe', {}).get('nome')}")
                    print(f"  • Órgão Julgador: {src.get('orgaoJulgador', {}).get('nome')}")
                    print(f"  • Última Atualização: {src.get('dataHoraUltimaAtualizacao')}")
                    print(f"  • Total de Movimentos: {len(src.get('movimentos', []))}")
                    
                    with open("resultado_positivo_datajud.json", "w", encoding="utf-8") as f:
                        json.dump(src, f, indent=2, ensure_ascii=False)
                    return True
                else:
                    print(f"  (Nenhum registro no endpoint {ep})")
        except Exception as e:
            print(f"  ⚠️ Erro no endpoint {ep}: {e}")
            
    return False

if __name__ == "__main__":
    # Testar com processo real do projeto (Júlio Pereira Marcos: 0023013-51.2021.8.19.0078)
    sucesso = consultar_processo_datajud("0023013-51.2021.8.19.0078")
    if not sucesso:
        # Fallback para Lucas Freitas
        consultar_processo_datajud("0011857-95.2024.8.19.0002")
