# Falhas Críticas Auditadas — Registro de Engenharia

Data da auditoria: 05/09/2026

## 1. Mocks Silenciosos em `fast_court_api_client.py`

O script `scripts/fast_court_api_client.py` retorna **dados fictícios** quando a API
do STJ ou DataJud falha, retorna HTTP 403, ou não encontra o processo. A função
`query_process` devolve `status: "ok"` com `resumo: "Processo em tramitação regular"`
mesmo quando o processo está em segredo de justiça ou a API caiu.

**Impacto:** O advogado recebe resposta positiva quando deveria receber alerta de erro.

**Correção necessária:** Substituir retornos mock por `status: "unavailable"` ou
`status: "not_found"` com o erro HTTP real logado.

## 2. Pop-up Bloqueante em `tjrj_extractor.py`

O script `scripts/tjrj_extractor.py` invoca `ctypes.windll.user32.MessageBoxW()`,
uma caixa de diálogo gráfica do Windows. Em ambiente headless ou automatizado,
a thread fica bloqueada eternamente esperando clique humano.

**Correção necessária:** Remover chamadas a `MessageBoxW` e substituir por logging.

## 3. Downloads Silenciosamente Omitidos em Scripts PJe

Scripts como `download_all_melquisedeque_pje_docs.py` usam
`expect_download(timeout=5000)` com `except Exception: pass`. Quando o PJe
redireciona para login (documento protegido), o timeout estoura e o erro é
engolido, reportando zero downloads sem qualquer alerta.

**Correção necessária:** Detectar redirect para página de login e logar explicitamente
que o documento requer certificado digital.

## 4. Chave DataJud Hardcoded em 30+ Scripts

A chave de API do DataJud CNJ está copiada literalmente em mais de 30 scripts
individuais. Se a chave expirar, será necessário atualizar todos manualmente.

**Correção necessária:** Centralizar em variável de ambiente `DATAJUD_API_KEY` ou
arquivo de configuração único.
