# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
url_tjrj = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}

target_dir = r"c:\Projetos\superJus\Clientes\Rodrigo_Nobrega"
os.makedirs(target_dir, exist_ok=True)

processos = [
    ("0800060-52.2023.8.19.0058", "08000605220238190058", "Ação Penal 1 / Apelação - Roubo Majorado"),
    ("0800262-29.2023.8.19.0058", "08002622920238190058", "Ação Penal 2 / Apelação - Roubo e Flagrante")
]

dossie_lines = [
    "# 🏛️ DOSSIÊ PROCESSUAL: RODRIGO DOS REIS NÓBREGA",
    "**Cliente:** Rodrigo dos Reis Nóbrega  ",
    "**Comarca de Origem:** Saquarema / RJ (2ª Vara)  ",
    "**Data da Extração:** 29/08/2026  \n",
    "---\n"
]

for num_cnj, clean_num, desc in processos:
    proc_dir = os.path.join(target_dir, "processos", num_cnj)
    os.makedirs(proc_dir, exist_ok=True)
    
    q = {"query": {"match": {"numeroProcesso": clean_num}}, "size": 10}
    req = urllib.request.Request(url_tjrj, data=json.dumps(q).encode("utf-8"), headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        hits = data.get("hits", {}).get("hits", [])
        
        with open(os.path.join(proc_dir, "todos_graus_raw.json"), "w", encoding="utf-8") as f:
            json.dump(hits, f, ensure_ascii=False, indent=2)
            
        dossie_lines.append(f"## ⚖️ PROCESSO: `{num_cnj}` — {desc}")
        
        for idx, h in enumerate(hits, 1):
            src = h["_source"]
            grau = src.get("grau")
            orgao = src.get("orgaoJulgador", {}).get("nome")
            classe = src.get("classe", {}).get("nome")
            dt = src.get("dataAjuizamento")
            assuntos = src.get("assuntos", [])
            assunto_str = ", ".join([a.get("nome", "") for a in assuntos])
            
            polos = src.get("dadosBasicos", {}).get("polo", [])
            partes_nomes = []
            for p in polos:
                pol = p.get("polo", "")
                for part in p.get("parte", []):
                    pess = part.get("pessoa", {})
                    n = pess.get("nome")
                    doc = pess.get("numeroDocumentoPrincipal")
                    if n:
                        partes_nomes.append(f"**{pol}:** {n} ({doc if doc else 'sem doc'})")
                        
            movs = src.get("movimentos", [])
            movs_desc = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
            
            dossie_lines.append(f"### Instância: `{grau}` ({'1ª Instância - Comarca de Saquarema' if grau == 'G1' else '2ª Instância - TJRJ'})")
            dossie_lines.append(f"- **Órgão Julgador:** {orgao}")
            dossie_lines.append(f"- **Classe Processual:** {classe}")
            dossie_lines.append(f"- **Assuntos Imputados:** {assunto_str}")
            dossie_lines.append(f"- **Data de Ajuizamento:** {dt}")
            dossie_lines.append(f"- **Partes Envolvidas:** {', '.join(partes_nomes)}")
            dossie_lines.append(f"- **Total de Movimentações:** {len(movs)}")
            dossie_lines.append(f"- **Último Andamento Registrado:** `{movs_desc[0].get('dataHora') if movs_desc else ''}` — **{movs_desc[0].get('nome') if movs_desc else 'N/A'}**\n")
            
            dossie_lines.append("#### Principais Marcos e Decisões:")
            marcos = [m for m in movs_desc if any(k in m.get("nome", "").lower() for k in [
                "denúncia", "decis", "acórdão", "acordao", "sentença", "sentenca", "audiência", "audiencia", "baixa", "expedição", "mandado"
            ])]
            for mk in marcos[:8]:
                dt_mk = mk.get("dataHora", "")[:19].replace("T", " ")
                comps = mk.get("complementosTabelados", [])
                comp_str = " | ".join([f"{c.get('descricao')}: {c.get('nome')}" for c in comps])
                dossie_lines.append(f"- **`{dt_mk}`** — **{mk.get('nome')}**" + (f" *({comp_str})*" if comp_str else ""))
            dossie_lines.append("\n")
            
        dossie_lines.append("---\n")

master_file = os.path.join(target_dir, "DOSSIE_MASTER_RODRIGO_NOBREGA.md")
with open(master_file, "w", encoding="utf-8") as f:
    f.write("\n".join(dossie_lines))

print(f"✅ Dossiê Master compilado com sucesso em: {master_file}")
