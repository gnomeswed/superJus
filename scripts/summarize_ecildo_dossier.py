# -*- coding: utf-8 -*-
import re

with open(r"c:\Projetos\Super Analista Jurídico\scripts\pdf_dossie_text.txt", "r", encoding="utf-8") as f:
    pdf_text = f.read()

print("=================== PDF DOSSIE CONTENT ===================")
print(pdf_text[:4000])
print("\n" + "="*50 + "\n")
print(pdf_text[4000:8000])

with open(r"c:\Projetos\Super Analista Jurídico\scripts\mhtml1_text.txt", "r", encoding="utf-8") as f:
    m1_text = f.read()

# Let's search for "Audiência", "Audiencia", "Ecildo", "080.730.972-90" in mhtml1
print("\n=== AUDIÊNCIAS ENCONTRADAS NO MHTML 1 ===")
aud_matches = [line.strip() for line in m1_text.split('\n') if 'audiência' in line.lower() or 'audiencia' in line.lower()]
for m in aud_matches[:30]:
    print("AUD:", m)
