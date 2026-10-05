# Dossiê de Busca — Sentença Integra do Renan
## Data: 10/08/2026 16:24–16:30

## Status da busca

A íntegra da sentença **NÃO foi encontrada** em fontes públicas. Motivos:

1. **TJRJ consulta pública** (`www3.tjrj.jus.br/consultaprocessual/#/consultapublica`): retornou mensagem "Este é um processo do PJe, clique em Acessar PJe". O link "Acessar PJe" é uma chamada Angular sem URL pública direta.
2. **PJe URL direta** (`pje.tjrj.jus.br/pje/login.seam`): **DNS NOT RESOLVED** — o subdomínio está descontinuado ou migrado.
3. **DJEN** (`comunica.pje.jus.br`): **ERR_CONNECTION_TIMED_OUT** (padrão registrado para todos os casos).
4. **DataJud API pública** (`api-publica.datajud.cnj.jus.br`): requer **API key válida** (HTTP 401 sem auth).
5. **DJe-TJRJ** (`www.tjrj.jus.br/dje`): página institucional genérica, sem rota para conteúdo de processos PJe.

## Bloqueios arquiteturais do TJRJ

- Processos PJe **não têm rota pública** para o conteúdo integral (sentença, decisões)
- Acesso requer login com certificado digital OAB/CPF ou credencial gov.br
- Subdomínio `pje.tjrj.jus.br` foi descontinuado — provável migração para novo portal
- Diário Oficial (DJERJ) publica **extratos resumidos**, não a íntegra

## Caminhos possíveis (não automatizáveis)

1. **Login manual no PJe** via `pje.tjrj.jus.br` (se a URL voltar) com credencial OAB
2. **Acesso presencial** na Vara Criminal de Maricá para consulta física dos autos
3. **Solicitação via OAB** de certidão de inteiro teor
4. **Pesquisa direta no Google** por `0821248-17.2025.8.19.0031 sentença` (pode achar índices de Jurisprudência)

## O que SE SABE da sentença (memória `relatorio_cliente_renan_marica.md`)

- Data: 03/07/2026
- Resultado: PROCEDÊNCIA (condenação)
- Status prisional: preso desde 30/11/2025 (preventiva)
- Próximo passo: verificar prazo recursal para Apelação

## Próxima ação recomendada

Pedir ao usuário para fazer **login manual no PJe** com credencial OAB e exportar a íntegra, ou autorizar o envio da consulta diretamente pelo escritório em Maricá.

## Arquivos gerados nesta busca
- `Clientes/Renan/03_Documentos_do_Processo/_raspagem_10_08_2026/raspagem_sentenca_renan_*.json` (3 manifestos)
- `Clientes/Renan/03_Documentos_do_Processo/_raspagem_10_08_2026/frame_pje_link.html` (HTML do frame com botão PJe)
- `Clientes/Renan/03_Documentos_do_Processo/_raspagem_10_08_2026/pje_test_*.png` (screenshots tentativas)
- `Clientes/Renan/03_Documentos_do_Processo/_raspagem_10_08_2026/dje_portal.png` (portal TJRJ)
