# -*- coding: utf-8 -*-
import json
import os

meta_file = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\case_meta.json"

with open(meta_file, "r", encoding="utf-8") as f:
    meta = json.load(f)

meta["processo_antigo"] = {
    "numero_1a_instancia": "0000253-78.2017.8.19.0004",
    "comarca": "Comarca de Niterói",
    "vara": "2ª Vara Criminal de Niterói",
    "data_distribuicao": "05/01/2017",
    "capitulacao": "Art. 157, § 2º, II do CP (Roubo Majorado)",
    "advogado_constituido": "Dr. José Guilherme Roder Saliba (OAB/RJ 111.872)",
    "habeas_corpus": {
        "numero": "0046418-98.2017.8.19.0000",
        "orgao": "3ª Câmara Criminal do TJRJ",
        "relator": "Des. Paulo Sérgio Rangel do Nascimento",
        "impetrante": "Dra. Vivian Baptista Gonçalves (Defensoria Pública - DP/860.696-4)",
        "data_julgamento_soltura": "29/08/2017"
    },
    "transito_em_julgado": "09/10/2017",
    "data_arquivamento": "08/11/2017",
    "local_arquivamento": "Arquivo Geral do TJRJ - Maço 1310262"
}

with open(meta_file, "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2, ensure_ascii=False)

print("case_meta.json do Lucas atualizado com sucesso com os dados do processo antigo de 2017 e HC!")
