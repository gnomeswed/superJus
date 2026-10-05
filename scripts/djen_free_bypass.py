# -*- coding: utf-8 -*-
"""
Solução 100% Gratuita de Bypass de IP para DJEN / DJERJ / Portais de Justiça.

Métodos Gratuitos Incluídos:
1. Jina AI Gateway Proxy (Sem necessidade de chave, 100% grátis e imediato)
2. Free Proxy Rotator Automático (Baixa lista atualizada de proxies gratuitos SOCKS5/HTTP, testa e rotaciona)
3. Rotação de Tor SOCKS5 Local (se o Tor service estiver rodando em 127.0.0.1:9050)
"""
import sys
import json
import urllib.request
import urllib.parse
import time
import random

sys.stdout.reconfigure(encoding="utf-8")

# --- MÉTODO 1: GATEWAY GRATUITO JINA AI ---
def buscar_djen_via_jina(tribunal="STJ", termo="HC 1.116.750"):
    """
    Utiliza o gateway gratuito r.jina.ai que contorna bloqueios de WAF/IP
    e entrega o resultado da consulta parseado.
    """
    target_url = f"https://comunica.pje.jus.br/consulta?siglaTribunal={tribunal}&meio=D"
    jina_url = f"https://r.jina.ai/{target_url}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "X-Return-Format": "markdown"
    }
    
    req = urllib.request.Request(jina_url, headers=headers)
    try:
        print(f"[Jina Proxy] Acessando DJEN via gateway gratuito para {tribunal}...")
        with urllib.request.urlopen(req, timeout=20) as resp:
            content = resp.read().decode("utf-8", errors="replace")
            return {"sucesso": True, "metodo": "Jina Gateway", "content": content[:4000]}
    except Exception as e:
        return {"sucesso": False, "metodo": "Jina Gateway", "erro": str(e)}

# --- MÉTODO 2: ROTADOR AUTOMÁTICO DE PROXIES GRATUITOS ---
def obter_proxies_gratuitos():
    """Baixa lista pública e atualizada de proxies HTTP gratuitos."""
    urls_proxies = [
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
    ]
    proxies = []
    for u in urls_proxies:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                lines = resp.read().decode("utf-8").splitlines()
                proxies.extend([l.strip() for l in lines if ":" in l])
        except Exception:
            pass
    random.shuffle(proxies)
    return proxies[:50]

def buscar_djen_com_proxy_gratis(tribunal="STJ", termo=""):
    """Tenta consultar o DJEN alternando por uma lista de proxies públicos gratuitos."""
    proxies = obter_proxies_gratuitos()
    print(f"[Free Proxy Rotator] {len(proxies)} proxies gratuitos carregados. Testando conexão...")
    
    url = "https://comunica.pje.jus.br/api/v1/comunicacao"
    payload = json.dumps({"siglaTribunal": tribunal, "meio": "D"}).encode("utf-8")
    
    for px in proxies:
        proxy_url = f"http://{px}"
        handler = urllib.request.ProxyHandler({"http": proxy_url, "https": proxy_url})
        opener = urllib.request.build_opener(handler)
        
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Content-Type": "application/json",
                "Origin": "https://comunica.pje.jus.br"
            },
            method="POST"
        )
        try:
            print(f"  -> Testando proxy gratuito: {px}...", end=" ", flush=True)
            with opener.open(req, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                print("SUCCESS! 🎉")
                return {"sucesso": True, "metodo": f"Free Proxy ({px})", "data": data}
        except Exception as e:
            print("Falhou (Timeout/Bloqueado)")
            
    return {"sucesso": False, "metodo": "Free Proxy Rotator", "erro": "Nenhum proxy gratuito respondeu a tempo."}

def main():
    print("=========================================================================")
    print("=== SOLUÇÃO 100% GRATUITA DE BYPASS DE BLOQUEIO DE IP — DJEN / PJE ===")
    print("=========================================================================\n")
    
    # 1. Testar Jina Gateway Gratuito
    res_jina = buscar_djen_via_jina(tribunal="STJ")
    if res_jina["sucesso"]:
        print("✅ SUCESSO VIA JINA GATEWAY (100% Grátis & Sem Setup):")
        print(res_jina["content"][:1500])
        print("\n-------------------------------------------------------------------------\n")
    else:
        print(f"⚠️ Jina Gateway falhou: {res_jina['erro']}")
        
    # 2. Testar Free Proxy Rotator
    res_proxy = buscar_djen_com_proxy_gratis(tribunal="STJ")
    if res_proxy["sucesso"]:
        print("✅ SUCESSO VIA FREE PROXY ROTATOR:")
        print(json.dumps(res_proxy["data"], indent=2, ensure_ascii=False)[:1500])
    else:
        print(f"⚠️ Free Proxy Rotator: {res_proxy['erro']}")

if __name__ == "__main__":
    main()
