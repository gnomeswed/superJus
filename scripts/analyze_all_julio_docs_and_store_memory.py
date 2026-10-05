# -*- coding: utf-8 -*-
import os
import sys
import json
import sqlite3
import uuid
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

db_path = r"C:\Users\Administrator\.memu\memu.sqlite3"
julio_dir = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos"

print("=== AUDITORIA INTEGRAL DOS DOCUMENTOS E MEMÓRIA DE JÚLIO PEREIRA MARCOS ===")

# 1. Mapeamento de Fatos Fundamentais dos Documentos
case_summary = {
    "cliente": "Júlio Pereira Marcos",
    "vulgo": "Julião",
    "mae": "Não constante expressamente na capa",
    "processos": {
        "acao_penal_desmembrada_1a_instancia": "0023013-51.2021.8.19.0078 (2ª Vara de Búzios)",
        "acao_penal_originaria": "0022975-39.2021.8.19.0078",
        "hc_tjrj": "0029845-67.2026.8.19.0000 (7ª Câmara Criminal)",
        "rhc_stj": "HC 1.116.750 / RJ (2026/0311210-7) - 6ª Turma, Min. Og Fernandes",
        "execucao_medida": "0001140-87.2024.8.19.0078"
    },
    "decisoes_chave": {
        "decretacao_preventiva": "27/01/2022 - Juízo da 2ª Vara de Búzios",
        "desmembramento": "30/05/2022 - Autos desmembrados quanto a Júlio e Rodrigo",
        "liberdade_correus": "02/08/2022 - Juíza Maíra Valéria concedeu Liberdade Provisória a TODOS os 5 corréus do feito originário (José Guilherme, Cristiano, Paulo Henrique, Emerson e Juliano)",
        "cumprimento_mandado_julio": "12/05/2026 - Efetuada a prisão após 4 anos",
        "denegacao_hc_tjrj": "11/06/2026 - Acórdão denegatório por unanimidade na 7ª Câmara Criminal (Publ. 16/06/2026)",
        "indeferimento_revogacao_1a_instancia": "24/07/2026 - Decisão do Juiz Danilo Marques Borges à fl. 1297 INDEFERINDO a revogação da preventiva por garantia da ordem pública (Publ. oficial no DJERJ em 29/07/2026)",
        "rhc_stj_autuacao": "29/07/2026 - Remessa externa do TJRJ ao STJ; autuado sob o HC 1.116.750/RJ",
        "oficio_tjrj_resposta_stj": "31/07/2026 (12:11h) - Ofício SEI 2026-06236234 transmitido pela 2VP TJRJ ao STJ"
    },
    "pontos_cegos_e_brechas_mapeadas": [
        "Vício de Isonomia (Art. 580 CPP): Todos os 5 corréus soltos desde 02/08/2022. Única apreensão física (218g maconha) correu com o corréu José Guilherme que está solto.",
        "Ausência de Materialidade com Júlio: Zero gramas de droga apreendidas com ele.",
        "Descaracterização do Art. 35 (Associação): Delegado Nelson Esquiba confessou em depoimento que não havia facção, hierarquia nem divisão organizada de tarefas.",
        "Prova Telemática / WhatsApp sem Perícia (Tema 1.062 STF): Ausência de confronto vocálico e integridade de hash dos áudios/prints de WhatsApp.",
        "Agravante da Calamidade (Art. 61, II, 'j' CP): Imputação genérica sem nexo causal concreto."
    ]
}

# 2. Gravar no memU SQLite
mem_id = str(uuid.uuid4())
now_str = datetime.now().isoformat()

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
        "Dossie_Mestre_Estrategico_Julio_Pereira_Marcos",
        "Julio_Pereira_Marcos_Caso_Principal",
        "Fatos completos, cronologia de decisões (inclusive indeferimento de 24/07/2026 fl. 1297 na 1ª Instância), brechas defensivas e RHC no STJ",
        json.dumps(case_summary, ensure_ascii=False, indent=2)
    ))
    
    conn.commit()
    conn.close()
    print(f"SUCESSO: Memória Mestra de Júlio gravada no memU SQLite com ID: {mem_id}")
except Exception as e:
    print(f"Erro ao gravar memória no SQLite: {e}")
