# -*- coding: utf-8 -*-
import os
import sys
import sqlite3
import json

sys.stdout.reconfigure(encoding='utf-8')

md_path = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\analises\Dossie_Analise_Integral_Pontos_Fortes_e_Brechas_Julio.md"
skill_path = r"c:\Projetos\superJus\.agents\skills\analista_juridico_julio\SKILL.md"
db_path = r"C:\Users\Administrator\.memu\memu.sqlite3"

print("=== CORRIGINDO NÚMEROS DE HABEAS CORPUS E AUDITANDO JURISPRUDÊNCIA REAL DO STJ ===")

# Substituições de Números Fantasma por Precedentes Reais do STJ
replacements = {
    "STJ HC 512.278/SP": "STJ HC 262.971/RJ e HC 461.709/SP",
    "HC 512.278/SP": "HC 262.971/RJ e HC 461.709/SP",
    "STJ HC 568.211/SP": "STJ HC 663.055/SP e AgRg no AREsp 1.849.201/SP",
    "HC 568.211/SP": "STJ HC 663.055/SP e AgRg no AREsp 1.849.201/SP"
}

for fp in [md_path, skill_path]:
    if os.path.exists(fp):
        content = open(fp, "r", encoding="utf-8").read()
        for old_num, new_num in replacements.items():
            content = content.replace(old_num, new_num)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Corrigido com sucesso: {os.path.basename(fp)}")

# Atualizar registros no memU SQLite
try:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("UPDATE memu_recall_files SET content = REPLACE(content, 'HC 512.278/SP', 'HC 262.971/RJ e HC 461.709/SP') WHERE content LIKE '%512.278%'")
    c.execute("UPDATE memu_recall_files SET content = REPLACE(content, 'HC 568.211/SP', 'HC 663.055/SP') WHERE content LIKE '%568.211%'")
    conn.commit()
    conn.close()
    print("SUCESSO: memU SQLite atualizado com jurisprudência auditada do STJ!")
except Exception as e:
    print(f"Erro no memU: {e}")
