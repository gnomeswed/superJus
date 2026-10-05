# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

def ddg_search(query):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"})
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            snippets = re.findall(r'<a class="result__snippet[^"]*"[^>]*>(.*?)</a>', html, re.DOTALL)
            clean = [re.sub(r'<.*?>', '', s).strip() for s in snippets]
            return clean[:3]
    except Exception as e:
        return [f"Erro: {e}"]

test_cases = [
    # 1. Processos citados pelo MPRJ nas Contrarrazões
    ("TJRJ APL 0014392-14.2009.8.19.0037 Paulo Rangel", '"0014392-14.2009.8.19.0037"'),
    ("STJ HC 462.253 Nefi Cordeiro", '"462.253" "Nefi Cordeiro"'),
    ("STJ AgRg no HC 902.892 Antonio Saldanha", '"902.892" "Saldanha Palheiro"'),
    ("STF HC 233825 André Mendonça", '"233825" "André Mendonça"'),

    # 2. Precedentes citados na análise defensiva
    ("STJ motivo futil discussao anterior", '"discussão anterior" "motivo fútil" STJ ementa'),
    ("STJ REsp 1.480.898", '"1.480.898" STJ'),
    ("STJ HC 512.651", '"512.651" STJ'),
    ("STJ detracao art 387 juiz sentenciante", '"387, § 2º" "juiz sentenciante" "regime inicial" STJ'),
    ("STJ fuga do reu pena-base", '"fuga do réu" "pena-base" STJ')
]

for desc, q in test_cases:
    print(f"\n==================================================")
    print(f"AUDITANDO: {desc}")
    print(f"QUERY: {q}")
    print(f"==================================================")
    results = ddg_search(q)
    if not results:
        print("  [Nenhum resultado encontrado]")
    for r in results:
        print(f"  -> {r[:200]}")
