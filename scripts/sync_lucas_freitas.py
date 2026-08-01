# -*- coding: utf-8 -*-
import os
import shutil
import json

src_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Processo_0011857-95.2024.8.19.0002"
dst_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal"

os.makedirs(os.path.join(dst_dir, "documentos_processo"), exist_ok=True)
os.makedirs(os.path.join(dst_dir, "pecas"), exist_ok=True)
os.makedirs(os.path.join(dst_dir, "analises"), exist_ok=True)

# Copiar arquivos de raiz de Processo_0011857 para documentos_processo
if os.path.exists(src_dir):
    for item in os.listdir(src_dir):
        sp = os.path.join(src_dir, item)
        if os.path.isfile(sp):
            dp = os.path.join(dst_dir, "documentos_processo", item)
            shutil.copy2(sp, dp)
            print(f"Copiado: {item} -> {dp}")

# Atualizar case_meta.json no Lucas_Freitas
meta = {
    "nome": "Lucas de Souza Freitas",
    "apelido": "Motoboy Lucas",
    "numero_processo": "0011857-95.2024.8.19.0002",
    "juizo": "3ª Vara Criminal - Tribunal do Júri de Niterói",
    "juiza": "Dra. Nearis dos S. Carvalho Arce",
    "correus": ["Ronny Batalha Fernandes"],
    "artigo": "Art. 121, § 2º, I, III e IV (Homicídio Triplamente Qualificado) e Art. 211 (Ocultação de Cadáver) do CP",
    "pena_total": "22 anos de reclusão em regime inicial FECHADO",
    "dosimetria": {
        "homicidio": "21 anos de reclusão",
        "ocultacao_cadaver": "1 ano de reclusão e 10 dias-multa"
    },
    "status": "Condenado pelo Tribunal do Júri (22/04/2026) - Preso Preventivo",
    "data_sentenca": "2026-04-22",
    "recurso_cabivel": "Apelação Criminal (Art. 593, III, 'c' e 'd' do CPP - Nulidades e Erro na Dosimetria)"
}

with open(os.path.join(dst_dir, "case_meta.json"), "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2, ensure_ascii=False)

print("Sincronização e organização do caso do Motoboy Lucas concluída!")
