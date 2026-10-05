# -*- coding: utf-8 -*-
import base64
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for step in ["2036", "2096", "2110"]:
    file_path = f"C:\\Users\\Administrator\\.gemini\\antigravity\\brain\\2187cd0c-a701-4a55-bea5-ce9e775530e8\\.system_generated\\steps\\{step}\\content.md"
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if '__VIEWSTATE' in line and 'value="' in line:
                    val = line.split('value="')[1].split('"')[0].strip()
                    pad = len(val) % 4
                    if pad:
                        val += '=' * (4 - pad)
                    raw = base64.b64decode(val).decode('latin1', errors='ignore')
                    for term in ["0004301-33", "0105796-38", "DANIEL FERREIRA LIMA"]:
                        idx = raw.find(term)
                        if idx != -1:
                            print(f"\n==========================================")
                            print(f"[Step {step}] ENCONTRADO: {term} (pos {idx})")
                            print(f"==========================================")
                            snip = raw[max(0, idx-50):idx+1600]
                            clean = re.sub(r'<[^>]+>', ' ', snip)
                            clean = re.sub(r'\s+', ' ', clean)
                            print(clean)
    except Exception as e:
        print(f"Erro em {step}: {e}")
