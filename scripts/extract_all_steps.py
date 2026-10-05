# -*- coding: utf-8 -*-
import re
import base64
import sys

sys.stdout.reconfigure(encoding='utf-8')

for step in ["2036", "2096", "2110"]:
    file_path = f"C:\\Users\\Administrator\\.gemini\\antigravity\\brain\\2187cd0c-a701-4a55-bea5-ce9e775530e8\\.system_generated\\steps\\{step}\\content.md"
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        m = re.search(r'name="__VIEWSTATE"\s+id="__VIEWSTATE"\s+value="([^"]+)"', text, re.DOTALL)
        if not m:
            m = re.search(r'__VIEWSTATE\|([^|]+)\|', text)
        if not m:
            # Pegar pelo início
            m = re.search(r'id="__VIEWSTATE"\s+value="([^"]+)"', text, re.DOTALL)
        if m:
            vs_val = m.group(1).replace('\n', '').replace('\r', '')
            raw = base64.b64decode(vs_val).decode('latin1', errors='ignore')
            for term in ["0004301-33", "0105796-38", "DANIEL FERREIRA"]:
                idx = raw.find(term)
                if idx != -1:
                    print(f"\n[Step {step}] Encontrado {term} em {idx}:")
                    snip = raw[max(0, idx-100):idx+1200]
                    clean = re.sub(r'<[^>]+>', ' ', snip)
                    print(re.sub(r'\s+', ' ', clean))
    except Exception as e:
        print(f"Erro no step {step}: {e}")
