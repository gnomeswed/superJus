# -*- coding: utf-8 -*-
import json
import os

meta_file = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\case_meta.json"
timeline_file = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\timeline.json"

# 1. Atualizar case_meta.json
with open(meta_file, "r", encoding="utf-8") as f:
    meta = json.load(f)

meta["ultima_movimentacao_1a_instancia"] = "28/07/2026 - Envio de Documento Eletrônico (Aguardando Manifestação do MP / Expediente publicado no DJERJ em 29/07/2026)"
meta["localizacao_atual"] = "Aguardando Manifestação do MP (2ª Vara de Armação dos Búzios)"
meta["data_ultima_atualizacao"] = "2026-07-28"

with open(meta_file, "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2, ensure_ascii=False)

# 2. Atualizar timeline.json
with open(timeline_file, "r", encoding="utf-8") as f:
    timeline = json.load(f)

datas_existentes = [item.get("date") for item in timeline]

novos = [
    {
        "date": "2026-07-28",
        "event": "Envio de Documento Eletrônico (Remessa ao MP em Búzios). Localização na Serventia: Aguardando Manifestação do MP."
    },
    {
        "date": "2026-07-29",
        "event": "Enviado para publicação (Expediente disponibilizado no Diário da Justiça Eletrônico - DJERJ)."
    }
]

for item in novos:
    if item["date"] not in datas_existentes:
        timeline.append(item)

# Ordenar cronologicamente
timeline_sorted = sorted(timeline, key=lambda x: x.get("date", ""))

with open(timeline_file, "w", encoding="utf-8") as f:
    json.dump(timeline_sorted, f, indent=2, ensure_ascii=False)

print("case_meta.json e timeline.json do Júlio atualizados com sucesso para 28/07/2026!")
