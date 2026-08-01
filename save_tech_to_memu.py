import sqlite3
import os
import uuid
from datetime import datetime

db_path = os.path.expanduser('~/.memu/memu.sqlite3')
os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

m = {
    "name": "memoria_arquitetura_scraping_tjrj.md",
    "track": "skill",
    "description": "Arquitetura técnica de monitoramento em tempo real do TJRJ/STJ via Playwright, DataJud e Cron Job",
    "content": """# Arquitetura de Monitoramento Processual em Tempo Real (TJRJ/STJ)

## Componentes do Sistema de Monitoramento
1. **Navegador Oculto (Headless Browser - Playwright):**
   - Utiliza Chromium em modo headless para acessar `https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica`.
   - Simula consulta por número de processo, lendo frames e tabelas de andamentos públicos em tempo real.
   - Script oficial: `scripts/tjrj_scraper_auto.py`.

2. **API Pública DataJud (CNJ):**
   - Requisições REST enviadas para `https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search`.
   - Consulta metadados nacionais unificados de processos e movimentações.

3. **Agendamento Recorrente em Segundo Plano (Cron Job):**
   - Configurado via ferramenta `schedule` com expressão cron `*/30 * * * *` (a cada 30 minutos).
   - Executa a verificação silenciosamente sem travar a interface do usuário e notifica apenas ao detectar novas movimentações.

4. **Tratamento de Segredo de Justiça:**
   - Processos sigilosos exibem dados gerais e certidões no portal público, mas exigem certificado digital OAB/PJe para o teor completo da decisão interna.
"""
}

now = datetime.now().isoformat()

cursor.execute("SELECT id FROM memu_recall_files WHERE name = ?", (m['name'],))
existing = cursor.fetchone()

if existing:
    cursor.execute("""
        UPDATE memu_recall_files 
        SET updated_at = ?, track = ?, description = ?, content = ?
        WHERE name = ?
    """, (now, m['track'], m['description'], m['content'], m['name']))
    print(f"Atualizado na memória memU: {m['name']}")
else:
    cursor.execute("""
        INSERT INTO memu_recall_files (id, created_at, updated_at, name, track, description, content, user_id, agent_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (str(uuid.uuid4()), now, now, m['name'], m['track'], m['description'], m['content'], 'user_default', 'antigravity_agent'))
    print(f"Gravado na memória memU: {m['name']}")

conn.commit()
conn.close()
print("Especificação técnica de scraping salva no memU com SUCESSO!")
