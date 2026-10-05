# Dossiê Final — Busca da Íntegra da Sentença do Renan
## Data: 10/08/2026 16:24–16:50
## Status: FALHA TOTAL — todas as fontes públicas bloqueadas

## Fontes tentadas (todas falharam)

### 1. TJRJ Consulta Pública
- URL: `https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica`
- Resposta: "Mensagem Processo do PJe — clique no botão Acessar PJe"
- O botão "Acessar PJe" é uma chamada Angular interna (sem URL pública)
- **BLOQUEADO** — processo PJe não tem rota de conteúdo público

### 2. PJe URLs diretas (todas com DNS NOT RESOLVED)
- `https://pje.tjrj.jus.br/pje/login.seam` ❌
- `https://pje.tjrj.jus.br/pje/` ❌
- `https://pje.tjrj.jus.br/ConsultaPublica/ConsultaPublica/listView.seam` �
- **Subdomínio descontinuado/migrado**

### 3. PJe 2.x (todos com DNS NOT RESOLVED)
- `https://pje2.tjrj.jus.br/` ❌
- `https://consultapje.tjrj.jus.br/` ❌
- `https://tj-rj.pje.jus.br/` ❌
- **Novos subdomínios não existem ou não foram publicados**

### 4. PJe TRF2 (subdomínio existe mas não atende Maricá)
- `https://pje.trf2.jus.br/` → HTTP 500 (servidor existe)
- `https://pje.trf2.jus.br/pje/ConsultaPublica/...` → HTTP 404
- **TRF2 não tem jurisdição sobre Maricá (que é estadual)**

### 5. DJEN / DJERJ
- `https://comunica.pje.jus.br/consulta?siglaTribunal=TJRJ&meio=D` → **ERR_CONNECTION_TIMED_OUT**
- `https://www.tjrj.jus.br/dje` → página institucional genérica
- `https://dje-consulta.tjrj.jus.br/` → **DNS NOT RESOLVED**
- **DJeTJRJ publica apenas extratos, não íntegras**

### 6. DataJud API Pública do CNJ
- URL: `https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search`
- API keys testadas (todas retornaram HTTP 401):
  - `cDZHYzlSd0drRzR0eHBpVzU4czd1VnViU3BhVlpMOTY=` (key demo CNJ em docs)
  - `APIKey ...` 
  - `Bearer ...`
  - `Basic ...`
- **Não há chave pública funcional para este endpoint**

### 7. Bing/DuckDuckGo
- Bing retornou 20 links, **0 relevantes** para o número do processo
- DuckDuckGo retornou 0 resultados
- **Sentenças penais NÃO são indexadas publicamente** (LGPD/segredo de justiça)

## Análise Arquitetural

A sentença de um processo criminal **não tem rota pública** na arquitetura do TJRJ:
- Processos PJe (Processo Judicial Eletrônico) só são acessíveis com login OAB/CPF
- O DJERJ publica apenas **extratos** (sem conteúdo integral)
- Google/Bing respeitam segredo de justiça
- APIs públicas (DataJud) exigem credenciamento formal

## Caminhos viáveis (todos manuais)

### A. Login manual do advogado no PJe
1. Acessar `https://pje.tjrj.jus.br/pje/login.seam` (quando voltar a funcionar)
2. Login com certificado OAB ou gov.br
3. Buscar o processo 0821248-17.2025.8.19.0031
4. Exportar sentença em PDF
5. Salvar em `Clientes/Renan/03_Documentos_do_Processo/Decisoes_na_Integra/`

### B. Certidão de inteiro teor na Vara
1. Solicitar presencialmente na Vara Criminal de Maricá
2. Ou via OAB com procuração

### C. Solicitação via DJEN (não testado)
- Após login no PJe, é possível se cadastrar para receber intimações por DJEN
- Não é a sentença em si, mas futuras movimentações

## O que SE SABE da sentença (memória `relatorio_cliente_renan_marica.md`)

- Data: 03/07/2026
- Resultado: PROCEDÊNCIA (condenação)
- Status prisional: preso desde 30/11/2025 (preventiva mantida)
- Próximo passo crítico: verificar prazo recursal para Apelação

## Arquivos gerados nesta busca

- `Clientes/Renan/03_Documentos_do_Processo/_raspagem_10_08_2026/raspagem_sentenca_renan_*.json` (4 manifestos)
- `Clientes/Renan/03_Documentos_do_Processo/_raspagem_10_08_2026/tentativas_finais_*.json`
- `Clientes/Renan/03_Documentos_do_Processo/_raspagem_10_08_2026/frame_pje_link.html`
- `Clientes/Renan/03_Documentos_do_Processo/_raspagem_10_08_2026/pje_test_*.png`
- `Clientes/Renan/03_Documentos_do_Processo/_raspagem_10_08_2026/dje_portal.png`
- `Clientes/Renan/03_Documentos_do_Processo/_raspagem_10_08_2026/chrome_user_session.png`

## Scripts criados

- `scripts/ultima_tentativa_final.py` — pipeline consolidado das 7 tentativas
- `scripts/buscar_sentenca_renan.py` — TJRJ + DJEN + PJe
- `scripts/debug_pje_link.py`, `debug_pje_link_v2.py`, `debug_pje_link_v3.py`
- `scripts/debug_pje_urls.py`, `debug_pje_click.py`
- `scripts/descobrir_url_pje.py`
- `scripts/explorar_portal_tjrj.py`
- `scripts/ultima_tentativa_url.py`
