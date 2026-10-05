# Catálogo Operacional de Servidores MCP — SuperJus
**Guia Prático: Quando e Como Usar Cada Servidor MCP**

Este guia estabelece a finalidade, ferramentas disponíveis, critérios de acionamento ("A Hora de Usar") e boas práticas para cada servidor MCP configurado no ambiente SuperJus.

---

## 1. `superjus-jurisprudencia` (Tribunais Superiores)
- **Tipo:** Nativo Local (FastMCP / Python 3.12)
- **Custo:** 100% Gratuito
- **Ferramentas:**
  - `pesquisar_jurisprudencia_stf(query: str, max_resultados: int)`: Pesquisa em tempo real de acórdãos e ementas oficiais no portal do STF.
  - `consultar_precedentes_julio(tema: str)`: Consulta imediata à base validada de precedentes do STF e STJ específicos para a defesa de Júlio Pereira Marcos.
- **🎯 A HORA DE USAR:**
  - Na redação ou fundamentação de **Habeas Corpus, Recursos Ordinários (RHC), Agravos Regimentais, Respostas à Acusação e Memoriais**.
  - Sempre que precisar de precedentes vinculantes ou de Turmas do STF/STJ sobre:
    - Extensão de benefício a corréus (Art. 580 do CPP).
    - Excesso de prazo na instrução criminal com réu preso.
    - Nulidade de prisão preventiva por gravidade abstrata (art. 312 do CPP).
    - Ausência de materialidade direta em tráfico/associação.
  - **Regra de Ouro:** NUNCA redigir tese de soltura baseada em ementas genéricas ou jurisprudência sem conferência; use este MCP para resgatar os precedentes oficiais íntegros.

---

## 2. `mcp-juridico-brasil` (DataJud / CNJ)
- **Tipo:** Nativo Local (DataJud API CNJ / Python 3.12)
- **Custo:** 100% Gratuito (Chave pública do CNJ)
- **Ferramentas:**
  - `buscar_processo_por_numero(numero_processo: str, tribunal: str)`: Consulta dados cadastrais, partes, classe e assunto CNJ.
  - `listar_movimentacoes(numero_processo: str, tribunal: str)`: Linha do tempo completa das movimentações com códigos TPU.
  - `resumir_andamento(numero_processo: str, tribunal: str)`: Síntese inteligente do status atual.
  - `calcular_proximo_prazo(data_intimacao: str, tipo_prazo: str)`: Cálculo automatizado de tempestividade.
  - `listar_intimacoes(oab_numero: str, oab_uf: str)`: Consulta de publicações em nome do advogado.
- **🎯 A HORA DE USAR:**
  - Sempre que o advogado pedir: *"atualize o processo X"*, *"verifique o andamento"*, *"consulte o número CNJ"*, ou *"veja as intimações do Dr. Gabriel"*.
  - É a **Fase 2 do POP de Consulta Processual**.
  - **Atenção Crítica:** Atente-se aos códigos TPU ambíguos (ex: 12146, 12068, 198); verifique sempre `complementosTabelados[]` para não presumir resultado de custódia.

---

## 3. `superjus-sqlite` (Memória e Banco Relacional memU)
- **Tipo:** Nativo Local (FastMCP / SQLite)
- **Custo:** 100% Gratuito
- **Banco Padrão:** `C:\Users\Administrator\.memu\memu.sqlite3`
- **Ferramentas:**
  - `read_query(query: str, db_path: str)`: Executa queries SQL de leitura (`SELECT`).
  - `list_tables(db_path: str)`: Lista todas as tabelas do banco de dados.
  - `describe_table(table_name: str, db_path: str)`: Mostra colunas e tipos da tabela.
  - `write_query(query: str, db_path: str)`: Executa inserções/atualizações locais.
- **🎯 A HORA DE USAR:**
  - Para consultar dados persistidos de clientes, histórico de decisões anteriores, logs de sincronização e tabelas de inteligência do SuperJus.
  - Para auditoria e checagem de integridade dos registros locais.

---

## 4. `brasil-dados-abertos` (OSINT & Due Diligence Cadastral)
- **Tipo:** Nativo Local (FastMCP / BrasilAPI)
- **Custo:** 100% Gratuito
- **Ferramentas:**
  - `consultar_cnpj(cnpj: str)`: Quadro Societário (QSA), Razão Social, CNAE, Capital Social e Endereço.
  - `consultar_cep(cep: str)`: Endereço completo, bairro e coordenadas.
  - `consultar_feriados_nacionais(ano: int)`: Feriados nacionais oficiais para cômputo de prazos (CPP/CPC).
- **🎯 A HORA DE USAR:**
  - **Contagem de Prazos:** Antes de fechar prazos processuais críticos, consulte feriados nacionais para verificar suspensão de expediente forense.
  - **Investigação Defensiva e Qualificação:** Obtenção de dados cadastrais de testemunhas, vítimas, empresas envolvidas em lavagem de capitais ou pessoas jurídicas ligadas à acusação.

---

## 5. `superjus-markitdown` (Ingestão Documental Inteligente)
- **Tipo:** Nativo Local (FastMCP / Microsoft MarkItDown)
- **Custo:** 100% Gratuito
- **Ferramentas:**
  - `convert_to_markdown(file_path: str)`: Converte PDFs de autos, petições, sentenças, laudos, planilhas Excel ou imagens em Markdown limpo.
  - `convert_and_save_markdown(file_path: str, output_path: str)`: Converte e salva diretamente no disco.
- **🎯 A HORA DE USAR:**
  - Ao receber novos arquivos na pasta do cliente (`c:\Projetos\superJus\clientes\...`).
  - Para ler peças escaneadas, inquéritos policiais extensos, laudos periciais e decisões judiciais volumosas sem truncar ou poluir o contexto da IA.

---

## 6. `superjus-fetch` (Navegador HTTP / Requisições Web)
- **Tipo:** UVX Fetch Runner
- **Custo:** 100% Gratuito
- **Ferramentas:**
  - `fetch(url: str)`: Efetua requisição web com user-agent de navegador moderno, ignorando restrições de robôs estáticos.
- **🎯 A HORA DE USAR:**
  - Para baixar páginas institucionais de tribunais, portais de consulta pública simples, tabelas de custas e publicações de diários oficiais (DJe) que não possuam barreiras complexas de autenticação.

---

## 7. `firecrawl-mcp` (Raspagem Profunda e Extração Web)
- **Tipo:** NPX / Node.js
- **Custo:** Chave Firecrawl
- **Ferramentas:**
  - `firecrawl_scrape(url: str)`: Converte páginas da web complexas diretamente em Markdown estruturado.
  - `firecrawl_search(query: str)`: Pesquisa web avançada com extração de conteúdo.
  - `firecrawl_crawl(url: str)`: Mapeamento e raspagem recursiva de sites inteiros.
- **🎯 A HORA DE USAR:**
  - Quando o `superjus-fetch` falhar devido a rendering de Javascript pesado ou estrutura interativa de portais jurídicos.
  - Para extrair doutrinas, artigos acadêmicos ou relatórios de comissões parlamentares/jurídicas online.

---

## 8. `codebase-memory-mcp` (Memória Arquitetural do Código)
- **Tipo:** Binário Nativo Go/Rust
- **Ferramentas:** `search_graph`, `query_graph`, `get_code_snippet`, `search_code`.
- **🎯 A HORA DE USAR:**
  - Exclusivo para sessões de desenvolvimento de software, refatoração de scripts e evolução da arquitetura do repositório SuperJus.

---

## 9. Módulo Cripto (`crypto-bybit-analyzer` & `coingecko-mcp`)
- **Tipo:** Python 3.12 / NPX Node
- **🎯 A HORA DE USAR:**
  - Restrito a tarefas do projeto de automação quantitativa e análise de mercado de derivativos Bybit/CoinGecko. Não aplicável às rotinas jurídicas criminais.

---

## Matriz Resumida de Acionamento Rápido

| Necessidade do Advogado | Servidor MCP Recomendado | Ferramenta Principal |
| :--- | :--- | :--- |
| **"Pesquise precedentes do STF/STJ para a petição"** | `superjus-jurisprudencia` | `pesquisar_jurisprudencia_stf` / `consultar_precedentes_julio` |
| **"Veja o andamento do processo / intimações"** | `mcp-juridico-brasil` | `buscar_processo_por_numero` / `listar_movimentacoes` |
| **"Leia esse PDF/laudo na pasta do cliente"** | `superjus-markitdown` | `convert_to_markdown` |
| **"Verifique feriados para a contagem do prazo"** | `brasil-dados-abertos` | `consultar_feriados_nacionais` |
| **"Consulte dados de sócio / CNPJ de empresa"** | `brasil-dados-abertos` | `consultar_cnpj` |
| **"Acesse histórico de memórias e teses locais"** | `superjus-sqlite` | `read_query` (memU) |
| **"Extraia o texto de uma página/portal web complexo"** | `firecrawl-mcp` ou `superjus-fetch` | `firecrawl_scrape` / `fetch` |
