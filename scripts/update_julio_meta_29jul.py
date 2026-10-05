# -*- coding: utf-8 -*-
import json
import os

meta_file = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\case_meta.json"
timeline_file = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\timeline.json"

# 1. Atualizar case_meta.json
with open(meta_file, "r", encoding="utf-8") as f:
    meta = json.load(f)

meta["ultima_movimentacao_1a_instancia"] = "29/07/2026 - Juntada - Petição (Manifestação do MP juntada de forma automática)"
meta["localizacao_atual"] = "Processos Com Manifestação do MP (2ª Vara de Armação dos Búzios)"
meta["data_ultima_atualizacao"] = "2026-07-29"

with open(meta_file, "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2, ensure_ascii=False)

# 2. Atualizar timeline.json
with open(timeline_file, "r", encoding="utf-8") as f:
    timeline = json.load(f)

datas_eventos = [(e.get("date"), e.get("event")) for e in timeline]

novo_evento = {
    "date": "2026-07-29",
    "event": "Juntada - Petição (Manifestação do MP juntada de forma automática). Localização na Serventia: Processos Com Manifestação do MP."
}

# Adicionar se não houver evento idêntico
if not any(e.get("date") == "2026-07-29" and "Manifestação do MP" in e.get("event") for e in timeline):
    timeline.append(novo_evento)

timeline_sorted = sorted(timeline, key=lambda x: x.get("date", ""))

with open(timeline_file, "w", encoding="utf-8") as f:
    json.dump(timeline_sorted, f, indent=2, ensure_ascii=False)

print("BINGO! case_meta.json e timeline.json do Júlio atualizados com sucesso com o parecer do MP de 29/07/2026!")
