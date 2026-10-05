# -*- coding: utf-8 -*-
import os
import sys
import json
import sqlite3
import uuid
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

md_path = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\analises\Dossie_Analise_Integral_Pontos_Fortes_e_Brechas_Julio.md"
db_path = r"C:\Users\Administrator\.memu\memu.sqlite3"

print("=== ATUALIZANDO DOSSIÊ E MEMÓRIA MEMU COM O PONTO FORTE DE EXCESSO DE PRAZO DA AIJ ===")

new_strength_section = """
### 🛡️ Ponto Forte 5: Excesso de Prazo Injustificado na Instrução Criminal (Art. 400 do CPP & Limite dos 90 Dias)
* **Argumento:** Júlio foi preso em **12/05/2026** e permanece segregado cautelarmente há mais de 83 dias. A Audiência de Instrução e Julgamento (AIJ) do processo desmembrado (`0023013-51.2021.8.19.0078`) **sequer foi realizada ou concluída**, extrapolando o prazo legal de 60 dias (Art. 400 do CPP) e o limite jurisprudencial razoável de 90 dias sem qualquer contribuição da defesa.
* **Impacto:** Configura constrangimento ilegal por excesso de prazo na prisão cautelar, reforçando o pedido liminar no **STJ (`HC 1.116.750/RJ`)** e o relaxamento da prisão na 1ª Instância.
"""

# 1. Atualizar arquivo Markdown
if os.path.exists(md_path):
    content = open(md_path, "r", encoding="utf-8").read()
    if "Ponto Forte 5" not in content:
        content = content.replace("## 🚨 3. BRECHAS LEGAIS E NULIDADES MAPEADAS", new_strength_section + "\n\n## 🚨 3. BRECHAS LEGAIS E NULIDADES MAPEADAS")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("SUCESSO: Arquivo Markdown do Dossiê atualizado com Ponto Forte 5!")

# 2. Gravar Registro de Memória no memU SQLite
mem_id = str(uuid.uuid4())
now_str = datetime.now().isoformat()

memory_payload = {
    "cliente": "Júlio Pereira Marcos",
    "ponto_forte_adicionado": "Excesso de Prazo na Prisão Preventiva / AIJ não realizada (Art. 400 CPP)",
    "detalhes": {
        "data_prisao": "12/05/2026",
        "dias_preso_sem_aij": "Mais de 83 dias (completando 90 dias em meados de agosto/2026)",
        "violacao_legal": "Art. 400 do CPP (prazo legal de 60 dias para realização da AIJ) e jurisprudência do STJ/STF (90 dias para encerramento da instrução de réu preso)",
        "aplicacao_pratica": "Reforço imediato no RHC no STJ (HC 1.116.750/RJ) e no pedido de relaxamento por excesso de prazo em Búzios."
    }
}

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO memu_recall_files (id, created_at, updated_at, name, track, description, content, user_id, agent_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'default_user', 'antigravity')
    """, (
        mem_id,
        now_str,
        now_str,
        "Ponto_Forte_Excesso_Prazo_AIJ_Julio",
        "Julio_Pereira_Marcos_Caso_Principal",
        "Tese de Ponto Forte: Excesso de prazo indevido na prisão preventiva por ausência de realização da AIJ no feito desmembrado (Art. 400 CPP / 90 dias)",
        json.dumps(memory_payload, ensure_ascii=False, indent=2)
    ))
    conn.commit()
    conn.close()
    print(f"SUCESSO: Ponto Forte de Excesso de Prazo gravado no memU SQLite com ID: {mem_id}")
except Exception as e:
    print(f"Erro ao gravar no SQLite: {e}")
