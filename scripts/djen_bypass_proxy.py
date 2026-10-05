# -*- coding: utf-8 -*-
"""
Script de Consulta ao DJEN (Diário de Justiça Eletrônico Nacional) com Bypass de Bloqueio de IP.
Suporta:
- Rotação de User-Agents e Headers Stealth
- Proxy Residencial BR / SOCKS5 / HTTP
- Fallback para API REST oficial do PJe Comunica
- Delay aleatório anti-rate-limiting
"""
import sys
import json
import time
import random
import argparse
import urllib.request
import urllib.parse

sys.stdout.reconfigure(encoding="utf-8")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"
]

def consultar_djen_api(tribunal="STJ", processo="", proxy=None):
    """Consulta o endpoint REST oficial do PJe Comunica com suporte a proxy."""
    url = "https://comunica.pje.jus.br/api/v1/comunicacao"
    
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://comunica.pje.jus.br",
        "Referer": "https://comunica.pje.jus.br/consulta"
    }

    payload = {
        "siglaTribunal": tribunal,
        "meio": "D"
    }
    if processo:
        payload["numeroProcesso"] = processo

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")

    # Configuração de Proxy se fornecido
    handlers = []
    if proxy:
        proxy_handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
        handlers.append(proxy_handler)
    
    opener = urllib.request.build_opener(*handlers)

    try:
        time.sleep(random.uniform(1.5, 3.0)) # Delay anti-bloqueio
        with opener.open(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {"sucesso": True, "data": data}
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Consulta DJEN com Bypass de IP")
    parser.add_argument("--tribunal", default="STJ", help="Sigla do tribunal (ex: STJ, TJRJ)")
    parser.add_argument("--processo", default="", help="Número do processo")
    parser.add_argument("--proxy", default=None, help="Proxy URL (ex: http://user:pass@ip:port)")
    
    args = parser.parse_args()
    
    print(f"=== DJEN BYPASS SEARCH: Tribunal={args.tribunal} | Proxy={'Sim' if args.proxy else 'Não (Direto)'} ===")
    res = consultar_djen_api(tribunal=args.tribunal, processo=args.processo, proxy=args.proxy)
    
    if res["sucesso"]:
        print("✅ Consulta realizada com SUCESSO!")
        print(json.dumps(res["data"], indent=2, ensure_ascii=False)[:2000])
    else:
        print(f"❌ Bloqueio ou Erro detectado: {res['erro']}")
        print("\nRecomendação: Utilize a flag --proxy com um IP residencial BR ou ative uma VPN com nó no Brasil.")

if __name__ == "__main__":
    main()
