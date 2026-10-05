import sqlite3
import uuid
import sys
import os
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

db_path = r"C:\Users\Administrator\.memu\memu.sqlite3"

def save_mem(name, track, desc, content):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Check if already exists by name
    c.execute("SELECT id FROM memu_recall_files WHERE name = ?", (name,))
    existing = c.fetchone()
    
    now_str = datetime.now().isoformat()
    if existing:
        mem_id = existing[0]
        c.execute("""
            UPDATE memu_recall_files 
            SET updated_at = ?, track = ?, description = ?, content = ?
            WHERE id = ?
        """, (now_str, track, desc, content, mem_id))
        print(f"Atualizada memória existente '{name}' (ID: {mem_id})")
    else:
        mem_id = str(uuid.uuid4())
        c.execute("""
            INSERT INTO memu_recall_files (id, created_at, updated_at, name, track, description, content, user_id, agent_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'default_user', 'shared_agent')
        """, (mem_id, now_str, now_str, name, track, desc, content))
        print(f"Criada nova memória '{name}' (ID: {mem_id})")
        
    conn.commit()
    conn.close()

# 1. MCP Jurídico Architecture
mem1_content = """# Arquitetura de MCPs Jurídicos Brasileiros (SuperJus Ecosystem)

O ecossistema jurídico dispõe dos seguintes servidores Model Context Protocol (MCP) integrados globalmente:

## 1. mcp-juridico-brasil (DataJud / CNJ)
- **Execução:** `python -m mcp_juridico_brasil.server`
- **Variáveis:** `DATAJUD_API_KEY`, `PYTHONIOENCODING=utf-8`
- **Ferramentas Disponíveis:**
  * `buscar_processo_por_numero(numero_processo)`: Localiza qualquer processo judicial nos 90+ tribunais do Brasil pelo padrão CNJ (NNNNNNN-DD.AAAA.J.TR.OOOO).
  * `listar_movimentacoes(numero_processo)`: Histórico cronológico completo de fases, atos ordinatórios, despachos e decisões.
  * `resumir_andamento(numero_processo)`: Sumário executivo e inteligível do estado atual da causa.
  * `monitorar_processo(numero_processo)`: Adiciona o feito à lista de vigilância contínua.
  * `calcular_proximo_prazo(data_intimacao, dias_prazo, tipo_processo)`: Contagem estrita e sem alucinações (Dias úteis no CPC / Dias corridos no CPP).
  * `listar_intimacoes(nome_advogado, oab, uf)`: Consulta intimações e publicações por patrono.

## 2. superjus-jurisprudencia
- **Execução:** `python c:/Projetos/superJus/scripts/jurisprudencia_mcp_server.py`
- **Ferramentas:**
  * `pesquisar_jurisprudencia_stf(termo)`: Pesquisa de precedentes, acórdãos e súmulas vinculantes do STF.
  * `consultar_precedentes_julio(tema)`: Busca teses consolidadas no STJ/STF (e.g. Art. 580 CPP, excesso de prazo, bis in idem).

## 3. brasil-dados-abertos (BrasilAPI)
- **Execução:** `python c:/Projetos/superJus/scripts/brasilapi_mcp_server.py`
- **Ferramentas:**
  * `consultar_cnpj(cnpj)`: Razão social, QSA, CNAE, situação cadastral na RFB.
  * `consultar_cep(cep)`: Logradouro, bairro, comarca e UF.
  * `consultar_feriados_nacionais(ano)`: Calendário de feriados bancários e forenses nacionais.

## 4. superjus-sqlite
- **Execução:** `python c:/Projetos/superJus/scripts/sqlite_mcp_server.py`
- **Banco de Dados:** `C:/Projetos/superJus/database/superjus.db`
- **Ferramentas:** `list_tables`, `describe_table`, `read_query`, `write_query`.

## 5. superjus-markitdown
- **Execução:** `python c:/Projetos/superJus/scripts/markitdown_mcp_server.py`
- **Ferramentas:** `convert_to_markdown`, `convert_and_save_markdown` (conversão precisa de PDFs, petições e sentenças).

## 6. superjus-fetch
- **Execução:** `uvx mcp-server-fetch --ignore-robots-txt`
- **Ferramentas:** `fetch` para obtenção de páginas, diários e portais com headers de navegador real.
"""

# 2. Scraping Protocol
mem2_content = """# Protocolo Mestre de Consulta Processual em Tempo Real (TJRJ / DJERJ / STJ / DataJud)

## 1. Portal TJRJ (1ª e 2ª Instâncias)
- **URL Base:** `https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica`
- **Tecnologia:** SPA Angular com Iframe `#mainframe`.
- **Procedimento Playwright:**
  1. `page.goto(..., wait_until='domcontentloaded')`
  2. Selecionar Instância:
     - 1ª Instância: `page.click('label[for="radioOrigem1"]')`
     - 2ª Instância: `page.click('label[for="radioOrigem2"]')`
  3. Preencher processo: `inp = page.wait_for_selector('input[placeholder*="número do processo"]'); inp.fill(proc_num)`
  4. Clicar pesquisar: `page.click('button:has-text("Pesquisar")')`
  5. Aguardar iframe: `page.wait_for_selector('iframe#mainframe', timeout=30000)`
  6. Acessar iframe: `frame = page.query_selector('iframe#mainframe').content_frame()`
  7. Expandir movimentos: `todos = frame.query_selector('a:has-text("Todos Os Movimentos"), a:has-text("Todos")'); todos.click()`
  8. Capturar texto: `txt = frame.inner_text('body')`

## 2. DJERJ (Diário da Justiça Eletrônico do RJ)
- **Varredura:** Busca por número do processo ou nome dos patronos/partes.
- **Validação:** Desconsiderar menções burocráticas ou homônimos; verificar sempre o número do processo vinculado.

## 3. STJ (Superior Tribunal de Justiça)
- **Consulta:** Via API DataJud (`0311210-10.2026.3.00.0000` / `2026/0311210-7`) e scraping de fases.
- **Fase de Conclusão:** Monitorar data/hora da conclusão ao Ministro Relator e pareceres do MPF.
"""

# 3. Legal Intelligence 360
mem3_content = """# Diretrizes de Inteligência Jurídica Brasileira e Contagem de Prazos

## 1. Regras Fundamentais de Contagem de Prazos
- **Processo Penal (CPP - Art. 798):** Prazos correm em **dias corridos**. Não se interrompem nem suspendem por férias, domingos ou feriados forenses. O dia do início não se conta; o do vencimento se inclui. Se o vencimento cair em feriado/final de semana, prorroga-se para o primeiro dia útil seguinte.
- **Processo Civil (CPC - Art. 219):** Prazos correm exclusivamente em **dias úteis**. Sábados, domingos e feriados são desconsiderados na contagem.

## 2. Habeas Corpus e Excesso de Prazo
- **Art. 400 do CPP:** A instrução criminal deve ser concluída em prazo razoável (90 dias para réus presos).
- **Inércia Cartorária Estrita:** A paralisação dos autos por omissão exclusiva do cartório ou do magistrado (sem culpa da defesa) configura constrangimento ilegal flagrante, ensejando relaxamento imediato da prisão ou substituição por medidas cautelares alternativas (Art. 319 do CPP).
- **Extensão de Benefício (Art. 580 do CPP):** Quando corréus em mesma situação fático-processual obtêm liberdade provisória, a ordem deve ser estendida aos demais corréus.
"""

# 4. Latest Julio Status
with open(r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\andamento_julio_21_09_2026.md", "r", encoding="utf-8") as f:
    julio_21_content = f.read()

save_mem(
    "mcp_juridico_brasil_arquitetura_e_ferramentas.md",
    "skill",
    "Arquitetura completa de MCPs jurídicos brasileiros (DataJud, STF, BrasilAPI, SQLite, Markitdown, Fetch)",
    mem1_content
)

save_mem(
    "protocolo_mestre_consulta_processual_tjrj_stj_djerj_datajud.md",
    "skill",
    "Protocolo master de automação Playwright e consulta processual em tempo real no TJRJ, DJERJ, STJ e DataJud",
    mem2_content
)

save_mem(
    "diretrizes_inteligencia_juridica_e_contagem_prazos.md",
    "skill",
    "Diretrizes de inteligência jurídica brasileira, contagem de prazos CPC/CPP e excesso de prazo",
    mem3_content
)

save_mem(
    "andamento_julio_21_09_2026.md",
    "Julio_Pereira_Marcos_Caso_Principal",
    "Relatório oficial de andamento em 21/09/2026: 132 dias de prisão cautelar, 48 dias de inércia em Búzios, 39 dias concluso no STJ",
    julio_21_content
)

print("Todas as memórias foram salvas com sucesso no memU!")
