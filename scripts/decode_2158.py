# -*- coding: utf-8 -*-
import base64
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\Administrator\.gemini\antigravity\brain\2187cd0c-a701-4a55-bea5-ce9e775530e8\.system_generated\steps\2158\content.md"
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

line = lines[116]
val = line.split('value="')[1].split('"')[0].strip()
pad = len(val) % 4
if pad:
    val += '=' * (4 - pad)
raw = base64.b64decode(val).decode('latin1', errors='ignore')

for term in ["0004301-33", "0105796-38", "DANIEL FERREIRA", "VILMA"]:
    idx = raw.find(term)
    if idx != -1:
        print(f"\n[Termo {term}] pos {idx}:")
        clean = re.sub(r'<[^>]+>', ' ', raw[max(0, idx-100):idx+1500])
        print(re.sub(r'\s+', ' ', clean))
