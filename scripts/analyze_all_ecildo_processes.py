# -*- coding: utf-8 -*-
import re
import json
import urllib.request

DATAJUD_API_KEY = __import__('os').getenv('DATAJUD_API_KEY','')

with open(r"c:\Projetos\Super Analista Jurídico\scripts\pdf_dossie_text.txt", "r", encoding="utf-8") as f:
    pdf_text = f.read()

with open(r"c:\Projetos\Super Analista Jurídico\scripts\mhtml1_text.txt", "r", encoding="utf-8") as f:
    m1_text = f.read()

with open(r"c:\Projetos\Super Analista Jurídico\scripts\mhtml2_text.txt", "r", encoding="utf-8") as f:
    m2_text = f.read()

# Extract CNJ process numbers
pattern = r'\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}'
all_matches = set(re.findall(pattern, pdf_text + m1_text + m2_text))

print(f"=== PROCESSOS ENCONTRADOS NAS FONTES ({len(all_matches)}) ===")
for p in sorted(all_matches):
    print(" -", p)

# Let's also parse the dossier text line by line or section by section to extract status in MT consultation
print("\n=== ANÁLISE DETALHADA DO DOSSIÊ PDF ===")
lines = pdf_text.split('\n')
current_proc = None
proc_details = {}

for line in lines:
    m = re.search(r'(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})', line)
    if m:
        current_proc = m.group(1)
        if current_proc not in proc_details:
            proc_details[current_proc] = []
    if current_proc:
        proc_details[current_proc].append(line)

for p, lns in proc_details.items():
    snippet = "\n".join(lns[:15])
    print(f"\n--- Processo {p} ---")
    print(snippet[:500])

# Query Datajud for EVERY process found
datajud_results = {}
for proc_num in sorted(all_matches):
    clean_num = re.sub(r'\D', '', proc_num)
    tb = "tjmt"
    if clean_num[13:16] == '819':
        tb = "tjrj"
    
    url = f"https://api-publica.datajud.cnj.jus.br/api_publica_{tb}/_search"
    headers = {
        "Authorization": DATAJUD_API_KEY,
        "Content-Type": "application/json"
    }
    query = {"query": {"match": {"numeroProcesso": clean_num}}, "size": 10}
    
    req = urllib.request.Request(url, data=json.dumps(query).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            hits = data.get('hits', {}).get('hits', [])
            if hits:
                sources = [h['_source'] for h in hits]
                datajud_results[proc_num] = sources
            else:
                datajud_results[proc_num] = []
    except Exception as e:
        datajud_results[proc_num] = f"Erro: {e}"

with open(r"c:\Projetos\Super Analista Jurídico\scripts\datajud_all_ecildo.json", "w", encoding="utf-8") as f:
    json.dump(datajud_results, f, ensure_ascii=False, indent=2)

print("\nDatajud consulta finalizada e salva.")
