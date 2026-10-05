# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
target_dir = r"c:\Projetos\superJus\Clientes\Rodrigo_Nobrega"

processos = [
    ("0800060-52.2023.8.19.0058", "08000605220238190058", "Proc 1 - Roubo Majorado"),
    ("0800262-29.2023.8.19.0058", "08002622920238190058", "Proc 2 - Roubo e Flagrante")
]

print("=== CONSOLIDANDO TODAS AS MOVIMENTAÇÕES, DESPACHOS E DECISÕES (G1 E G2) ===")

for num_cnj, clean_num, desc in processos:
    proc_folder = os.path.join(target_dir, "processos", num_cnj)
    os.makedirs(proc_folder, exist_ok=True)
    raw_path = os.path.join(proc_folder, "todos_graus_raw.json")
    
    if not os.path.exists(raw_path):
        url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
        headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}
        q = {"query": {"match": {"numeroProcesso": clean_num}}, "size": 10}
        req = urllib.request.Request(url, data=json.dumps(q).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
    else:
        hits = json.load(open(raw_path, encoding="utf-8"))

    md_lines = []
    md_lines.append(f"# ⚖️ AUTOS INTEGRAIS: PROCESSO `{num_cnj}`")
    md_lines.append(f"**Cliente:** Rodrigo dos Reis Nóbrega  ")
    md_lines.append(f"**Identificação:** {desc}  ")
    md_lines.append(f"**Origem:** 2ª Vara da Comarca de Saquarema / TJRJ  \n")
    md_lines.append("---\n")

    for h in hits:
        src = h["_source"]
        grau = src.get("grau")
        orgao = src.get("orgaoJulgador", {}).get("nome")
        classe = src.get("classe", {}).get("nome")
        dt_aj = src.get("dataAjuizamento")
        assuntos = [a.get("nome", "") for a in src.get("assuntos", [])]
        movs = src.get("movimentos", [])
        movs_desc = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)

        md_lines.append(f"## 🏛️ Instância: `{grau}` — {orgao}")
        md_lines.append(f"- **Classe:** {classe}")
        md_lines.append(f"- **Assuntos:** {', '.join(assuntos)}")
        md_lines.append(f"- **Data de Ajuizamento:** {dt_aj}")
        md_lines.append(f"- **Total de Movimentações:** {len(movs)}\n")

        md_lines.append("### 📜 Histórico Cronológico de Todas as Movimentações (Mais Recente ao Início):")
        for idx, m in enumerate(movs_desc, 1):
            dt = m.get("dataHora", "")[:19].replace("T", " ")
            comps = m.get("complementosTabelados", [])
            comp_str = " | ".join([f"{c.get('descricao')}: {c.get('nome')}" for c in comps])
            md_lines.append(f"{idx}. **`{dt}`** — **{m.get('nome')}** (Cód. `{m.get('codigo')}`)" + (f" *({comp_str})*" if comp_str else ""))
        
        md_lines.append("\n---\n")

    out_file = os.path.join(proc_folder, "historico_completo_movimentacoes_e_decisoes.md")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"✅ Salvo histórico de {num_cnj} em: {out_file}")

print("\n=== HISTÓRICOS DE 1ª E 2ª INSTÂNCIA CONCLUÍDOS COM SUCESSO ===")
