# -*- coding: utf-8 -*-
import json
import urllib.request
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== COMPILANDO HISTÓRICO COMPLETO DO PROCESSO — ANTÔNIO VITOR ===")

base_dir = r"c:\Projetos\superJus\Clientes\Antonio_Vitor"
mov_dir = os.path.join(base_dir, "02_Movimentacoes")
doc_dir = os.path.join(base_dir, "03_Documentos_do_Processo")
os.makedirs(mov_dir, exist_ok=True)
os.makedirs(doc_dir, exist_ok=True)

headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

proc_clean = "01758038620238190001"
url_tjrj = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'

req_data = json.dumps({"query": {"match": {"numeroProcesso": proc_clean}}, "size": 20}).encode('utf-8')
req = urllib.request.Request(url_tjrj, data=req_data, headers=headers)

with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode('utf-8'))
    hits = res.get('hits', {}).get('hits', [])

# 1. Salvar JSON Bruto
json_out = os.path.join(mov_dir, "datajud_movimentacoes_completas.json")
with open(json_out, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print(f"✅ JSON das movimentações salvo em: {json_out}")

# 2. Gerar Markdown Completo
md_out = os.path.join(mov_dir, "Movimentacoes_Completas_Antonio_Vitor.md")
md_lines = [
    "# RELATÓRIO COMPLETO DE MOVIMENTAÇÕES E DECISÕES",
    "**Cliente:** ANTÔNIO VITOR",
    "**Processo Principal:** `0175803-86.2023.8.19.0001`",
    "**Vara de Origem:** 1ª Vara Criminal da Comarca de Petrópolis/RJ (Tribunal do Júri)",
    "**Segunda Instância:** Gabinete do Des. Geraldo da Silva Batista Júnior (TJRJ)",
    "**Data da Auditoria:** 16/08/2026",
    "\n---"
]

for idx, rec in enumerate(hits, start=1):
    src = rec['_source']
    orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
    classe = src.get('classe', {}).get('nome', 'N/I')
    movs = src.get('movimentos', [])
    movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
    
    md_lines.append(f"\n## 🏛️ REGISTRO PROCESSUAL #{idx}")
    md_lines.append(f"- **Órgão Julgador:** {orgao}")
    md_lines.append(f"- **Classe:** {classe}")
    md_lines.append(f"- **Total de Lançamentos:** {len(movs)}")
    md_lines.append("\n| # | Data/Hora | Movimentação / Ato | Código | Detalhes / Complementos |")
    md_lines.append("|---|---|---|---|---|")
    
    for m_idx, m in enumerate(movs_sorted, start=1):
        dt = m.get('dataHora', '')[:19].replace('T', ' ')
        nome = m.get('nome', '')
        code = m.get('codigo', '')
        comps = m.get('complementosTabelados', [])
        comp_str = ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) if comps else "-"
        md_lines.append(f"| {m_idx} | {dt} | **{nome}** | {code} | {comp_str} |")

with open(md_out, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print(f"✅ Relatório Markdown compilado em: {md_out}")

# 3. Gerar documento TXT/PDF do Espelho Oficial
txt_out = os.path.join(doc_dir, "Espelho_Oficial_Processo_Antonio_Vitor.txt")
with open(txt_out, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print(f"✅ Espelho oficial salvo em: {txt_out}")

print("\n=== COMPILAÇÃO E DOWNLOADS FINALIZADOS ===")
