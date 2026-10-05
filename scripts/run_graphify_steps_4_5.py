# -*- coding: utf-8 -*-
import sys, json
from pathlib import Path
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate
from graphify.export import to_json

extraction = json.loads(Path("graphify-out/.graphify_extract.json").read_text(encoding="utf-8"))
detection = json.loads(Path("graphify-out/.graphify_detect.json").read_text(encoding="utf-8"))
root_path = str(Path(Path("graphify-out/.graphify_root").read_text(encoding="utf-8").strip()))

# Build graph
G = build_from_json(extraction, root=root_path, directed=False)
print(f"Grafo construído: {G.number_of_nodes()} nós, {G.number_of_edges()} arestas")

communities = cluster(G)
cohesion = score_all(G, communities)
gods = god_nodes(G)
surprises = surprising_connections(G, communities)

# Curadoria inteligente de nomes para as comunidades jurídicas
node_labels = {n["id"]: n.get("label", n["id"]) for n in extraction["nodes"]}
community_labels = {}

for cid, node_ids in communities.items():
    labels_in_c = [node_labels.get(nid, nid) for nid in node_ids]
    text_c = " ".join(labels_in_c).lower()
    if "stj" in text_c or "og fernandes" in text_c or "benjamin" in text_c or "razões finais" in text_c:
        community_labels[cid] = "Gabinete Og Fernandes e Recursos STJ"
    elif "delegado" in text_c or "instrução" in text_c or "audiência" in text_c or "perícia" in text_c:
        community_labels[cid] = "Audiência de Instrução e Provas Policiais"
    elif "originário" in text_c or "corréus" in text_c or "rese" in text_c or "búzios" in text_c:
        community_labels[cid] = "Processos 1ª Instância Búzios e Isonomia"
    elif "rio bonito" in text_c or "primariedade" in text_c or "reincidência" in text_c:
        community_labels[cid] = "Primariedade Técnica e Certidão de Rio Bonito"
    elif "hc" in text_c or "tjrj" in text_c or "câmara" in text_c:
        community_labels[cid] = "2ª Instância TJRJ e Habeas Corpus"
    elif "excesso" in text_c or "prazo" in text_c or "580" in text_c:
        community_labels[cid] = "Teses de Excesso de Prazo e Isonomia"
    elif "adversarial" in text_c or "debate" in text_c or "estratégia" in text_c:
        community_labels[cid] = "Inteligência Estratégica e Debates"
    else:
        community_labels[cid] = f"Núcleo Jurídico {cid}"

print("\nComunidades Identificadas:")
for cid, name in community_labels.items():
    print(f"  [{cid}] {name} ({len(communities[cid])} nós)")

# Regenerar questões
questions = suggest_questions(G, communities, community_labels)

# Exportar graph.json
to_json(G, communities, "graphify-out/graph.json", community_labels=community_labels)

# Gerar GRAPH_REPORT.md
tokens = {"input": extraction.get("input_tokens", 0), "output": extraction.get("output_tokens", 0)}
report = generate(G, communities, cohesion, community_labels, gods, surprises, detection, tokens, root_path, suggested_questions=questions)
Path("graphify-out/GRAPH_REPORT.md").write_text(report, encoding="utf-8")

# Salvar labels e analysis
Path("graphify-out/.graphify_labels.json").write_text(json.dumps({str(k): v for k, v in community_labels.items()}, ensure_ascii=False, indent=2), encoding="utf-8")
analysis = {
    "communities": {str(k): v for k, v in communities.items()},
    "cohesion": {str(k): v for k, v in cohesion.items()},
    "gods": gods,
    "surprises": surprises,
    "questions": questions,
}
Path("graphify-out/.graphify_analysis.json").write_text(json.dumps(analysis, indent=2, ensure_ascii=False), encoding="utf-8")

print("\nStep 4 e Step 5 concluídos com sucesso!")
