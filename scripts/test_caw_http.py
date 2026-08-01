# -*- coding: utf-8 -*-
import urllib.request

url = "http://localhost:8080"
print(f"Testando conexão com servidor Caw em {url}...")

try:
    with urllib.request.urlopen(url, timeout=5) as resp:
        content = resp.read().decode('utf-8')
        print(f"Status: {resp.status}")
        print(f"Tamanho da resposta: {len(content)} bytes")
        print("Conteúdo HTML (primeiros 300 caracteres):")
        print(content[:300])
except Exception as e:
    print(f"Erro ao conectar com {url}: {e}")
