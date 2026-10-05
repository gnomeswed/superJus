import sqlite3
import os
import uuid
from datetime import datetime

db_path = os.path.expanduser('~/.memu/memu.sqlite3')
os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Garantir que a tabela memu_recall_files existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS memu_recall_files (
    id TEXT PRIMARY KEY,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    name TEXT,
    track TEXT,
    description TEXT,
    embedding BLOB,
    content TEXT,
    user_id TEXT,
    agent_id TEXT
)
''')

memories = [
    {
        "name": "memoria_caso_julio_pereira_marcos.md",
        "track": "memory",
        "description": "Histórico completo, fatos, decisões táticas e andamentos do cliente Júlio Pereira Marcos",
        "content": """# Memória Defensiva — Júlio Pereira Marcos

## Fatos e Dados do Cliente
- **Nome:** Júlio Pereira Marcos
- **Ação Penal Originária:** Processo nº `0023013-51.2021.8.19.0078` (2ª Vara da Comarca de Saquarema/RJ - Operação Delivery)
- **Habeas Corpus TJRJ:** `0029845-67.2026.8.19.0000` (7ª Câmara Criminal, Rel. Des. Sidney Rosa da Silva - DENEGADO)
- **Habeas Corpus STJ:** `HC 1.116.750/RJ` (Relator: Ministro Og Fernandes / Presidência: Min. Herman Benjamin)

## Decisões Táticas e Estratégia de Defesa
1. **Perícia Vocal (DECISÃO DEFINITIVA):** NUNCA solicitar perícia na voz do Júlio nas interceptações telefônicas, para evitar produção de prova em desfavor do réu.
2. **Linha Telefônica:** Confirmado na instrução/transcrição que a linha interceptada está vinculada ao CPF do Júlio e foi reconhecida por sua mãe.
3. **Cronograma de Soltura:** Advogado projeta prazo médio de até 6 meses de custódia cautelar (com base na libertação dos corréus da mesma operação ocorrida em agosto de 2022).
4. **Andamento no STJ:** Em 31/07/2026 às 12:11, o TJRJ enviou o Ofício SEI 2026-06236234 com informações ao STJ. Processo aguarda parecer do MPF para apreciação de liminar/mérito pelo Min. Og Fernandes.
"""
    },
    {
        "name": "memoria_caso_ecildo_victor.md",
        "track": "memory",
        "description": "Mapeamento completo dos 8 processos, situação de prisão no RJ e teses defensivas do cliente Ecildo Victor dos Santos Ferreira",
        "content": """# Memória Defensiva — Ecildo Victor dos Santos Ferreira

## Fatos e Dados do Cliente
- **Nome:** Ecildo Victor dos Santos Ferreira
- **CPF:** `080.730.972-90`
- **Situação Cautelar:** Preso preventivamente na SEAP/RJ por ordem da Justiça de Mato Grosso (1ª Vara Criminal de Sinop/MT) há cerca de 8 meses, aguardando transferência (recambiamento).

## Mapeamento dos Processos (Sinop/MT)
- `1003524-57.2023.8.11.0015`: Ação Penal por Furto Simples (Art. 155 CP) — **Processo Principal / Risco Cautelar Ativo**.
- `1014036-36.2022.8.11.0015`: Processo em **Segredo de Justiça** — Arquivado definitivamente em 31/08/2022 (zero risco cautelar).
- `1013261-21.2022.8.11.0015` e `1017084-03.2022.8.11.0015`: Suspensos pelo Art. 366 do CPP.

## Teses Defensivas Fundamentais
1. **Excesso de Prazo:** 8 meses de custódia preventiva no RJ sem conclusão da instrução criminal ou oitiva do réu em Sinop/MT.
2. **Ausência de Revisão Trimestral (Art. 316, Parágrafo Único do CPP):** Prisão mantida sem reavaliação periódica fundamentada a cada 90 dias.
3. **Desproporcionalidade Cautelar (Art. 282, § 6º CPP):** Crime de furto simples sem violência. Eventual condenação geraria regime aberto/substituição de pena.
"""
    },
    {
        "name": "memoria_diretrizes_relatorios_pdf.md",
        "track": "skill",
        "description": "Regras de formatação, layout executivo e geração de PDFs sem erros visuais",
        "content": """# Diretrizes Técnicas de Geração de PDF

## Regras de Formatação e Estilo
1. **Limpeza de Tags HTML:** Em geradores ReportLab, NUNCA deixar vazar tags puras como `<b>`, `</b>` ou crases `` ` `` como texto visível no leitor de PDF.
2. **Remoção de Código Mermaid:** Filtrar completamente sintaxes de diagramas (`graph TD`, `subgraph`) para evitar que vazem texto simples nos relatórios.
3. **Cabeçalho e Rodapé Executivos:** Incluir numeração de páginas dinâmica ("Página X de Y"), régua divisória e selo de confidencialidade.
4. **Locais de Destino:** Salvar cópias sincronizadas na Área de Trabalho (`Desktop/`), na pasta do cliente e na raiz do projeto.
"""
    }
]

now = datetime.now().isoformat()

for m in memories:
    # Verificar se já existe registro com este nome
    cursor.execute("SELECT id FROM memu_recall_files WHERE name = ?", (m['name'],))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("""
            UPDATE memu_recall_files 
            SET updated_at = ?, track = ?, description = ?, content = ?
            WHERE name = ?
        """, (now, m['track'], m['description'], m['content'], m['name']))
        print(f"Atualizado na memória: {m['name']}")
    else:
        cursor.execute("""
            INSERT INTO memu_recall_files (id, created_at, updated_at, name, track, description, content, user_id, agent_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (str(uuid.uuid4()), now, now, m['name'], m['track'], m['description'], m['content'], 'user_default', 'antigravity_agent'))
        print(f"Inserido na memória: {m['name']}")

conn.commit()
conn.close()
print("Sincronização do histórico completo da conversa para o memU finalizada com SUCESSO!")
