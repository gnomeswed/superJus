# -*- coding: utf-8 -*-
import sqlite3
import json
import uuid
import sys
from datetime import datetime

db_path = r"C:\Users\Administrator\.memu\memu.sqlite3"

memory_data = {
    "id": str(uuid.uuid4()),
    "name": "Consulta Processual TJRJ e Automação Playwright",
    "track": "TJRJ_Scraper_Workflow",
    "description": "Procedimento técnico e scripts para consulta em tempo real aos processos do TJRJ (1ª Instância Búzios, 7ª Câmara Criminal) e integração com Datajud API",
    "content": json.dumps({
        "ferramentas": ["Playwright Python (Chromium Headless)", "Datajud CNJ API", "memU SQLite"],
        "url_tjrj": "https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica",
        "iframe_target": "iframe#mainframe",
        "input_name": "numeroProcesso",
        "botao_movimentos": "Todos Os Movimentos",
        "processos_julio": {
            "acao_penal_buzios": "0023013-51.2021.8.19.0078",
            "hc_tjrj": "0029845-67.2026.8.19.0000",
            "hc_stj": "HC 1.116.750 / RJ (2026/0311210-7)",
            "execucao_medida": "0001140-87.2024.8.19.0078"
        },
        "instrucoes_consulta": "A consulta ao vivo deve utilizar Playwright acessando o iFrame mainframe, preenchendo o número formatado e clicando em Todos Os Movimentos para extrair o texto completo do espelho processual.",
        "registrado_em": datetime.now().isoformat()
    }, ensure_ascii=False, indent=2)
}

print("=== GRAVANDO MEMÓRIA PERSISTENTE NO MEMU SQLITE ===")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    now_str = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO memu_recall_files (id, created_at, updated_at, name, track, description, content, user_id, agent_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (memory_data["id"], now_str, now_str, memory_data["name"], memory_data["track"], memory_data["description"], memory_data["content"], "default_user", "antigravity"))
    
    conn.commit()
    conn.close()
    print(f"SUCESSO: Memória persistida com sucesso! (ID: {memory_data['id']})")
except Exception as e:
    print(f"Erro ao gravar memória: {e}")
