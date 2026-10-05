# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
url = "https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}
q = {"query": {"match": {"numeroProcesso": "03112101020263000000"}}}

req = urllib.request.Request(url, data=json.dumps(q).encode("utf-8"), headers=headers)
with urllib.request.urlopen(req, timeout=30) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    hits = data.get("hits", {}).get("hits", [])
    if hits:
        stj_data = hits[0]["_source"]
        p_num = stj_data.get("numeroProcesso")
        classe = stj_data.get("classe", {}).get("nome")
        dt_up = stj_data.get("dataHoraUltimaAtualizacao")
        movs = stj_data.get("movimentos", [])
        movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
        print(f"STJ Processo: {p_num} | Classe: {classe} | Ultima Atualizacao: {dt_up}")
        top_movs = []
        for m in movs_sorted[:10]:
            dt_m = m.get("dataHora", "")[:19].replace("T", " ")
            nome_m = m.get("nome", "")
            compl = m.get("complementosTabelados", [])
            print(f"  • {dt_m} | {nome_m} | Compl: {compl}")
            top_movs.append({"dataHora": dt_m, "nome": nome_m, "complementos": compl})

        stj_entry = {
            "numeroProcesso": p_num,
            "classe": classe,
            "ultimaAtualizacao": dt_up,
            "ultimosMovimentos": top_movs
        }

        # Atualiza nos dois JSONs
        for json_path in [
            r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\consulta_ao_vivo_16_09_2026.json",
            r"C:\Projetos\swedsystem\docs\consulta_ao_vivo_16_09_2026.json"
        ]:
            if os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as f:
                    curr = json.load(f)
                curr["datajud_stj"] = [stj_entry]
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(curr, f, ensure_ascii=False, indent=2)
                print(f"Atualizado STJ em {json_path}")
