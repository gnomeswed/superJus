# Raspagem Completa Lucas — Memória para Hermes/CommandCode/OpenCode
## Data: 10/08/2026 14:14–14:33

## Resumo Executivo
Raspagem completa via API direta + Playwright do processo `0011857-95.2024.8.19.0002` (Lucas de Souza Freitas).
- **175 movimentos** salvos em TXT individuais em `Clientes/Lucas_Freitas/02_Movimentacoes_Individuais/` (formato `DD-MM-YYYY_NNN_Tipo.txt`)
- **3 integrais** capturadas via modal UI em `Clientes/Lucas_Freitas/03_Documentos_do_Processo/Decisoes_na_Integra/` (decisão 17/06/2026: Original + Simplificado + Ato Assinado)

## Achados Técnicos Importantes sobre TJRJ

### 1. A API `/api/processos/por-numero/movimentos` retorna TODOS os movimentos de uma vez
- Endpoint: POST `https://www3.tjrj.jus.br/consultaprocessual/api/processos/por-numero/movimentos`
- Body: `{"tipoProcesso":"1","codigoProcesso":"2024.002.011419-1","indProcVolumoso":"N","ultimaOrdemExibida":null}`
- Resposta: 473KB com **175 movimentos** (não 10 como mostra a UI!)
- **Pagination via cursor**: `ultimaOrdemExibida` recebe a ordem do último movimento
- O campo correto dos movimentos é `movimentosProc` (não `movimentos`)

### 2. NÃO existe "exibir 500 por página" configurável pelo usuário
- A UI exibe o dropdown `500` apenas quando a lista tem mais de 1 página
- Para processos com <10 movimentos (Lucas com 175 não entra nessa categoria mas a UI só mostra 10 resumidos), o paginador não aparece
- O número `500` é fixo no dropdown (default), mas isso não muda o comportamento real

### 3. Integrais (Ver íntegra / Visualizar Ato) NÃO são baixáveis programaticamente
- UI mostra apenas 3 botões por bloco visível (não há "expandir tudo")
- API retorna metadados (`codDocAtoAssinadoDig`, `resumoOuIntegra`) mas **NÃO o conteúdo integral**
- Endpoints `/api/atos/{codDoc}`, `/api/documentos/{codDoc}`, `/api/documento/download/{codDoc}` exigem **Bearer token** (HTTP 401)
- TJRJ usa Datadome anti-bot (cdn.rybena.com.br) — scraping agressivo pode ser bloqueado
- **Workaround manual**: usuário precisa clicar em cada bloco individualmente na UI

### 4. Resumo da captura final
| Item | Status | Localização |
|------|--------|-------------|
| 175 movimentos TXT | ✅ Salvos | `02_Movimentacoes_Individuais/` |
| 3 integrais (decisão 17/06) | ✅ Salvas | `03_Documentos_do_Processo/Decisoes_na_Integra/` |
| 30+ outras integrais (10/06, 12/05, 24/04 sentença, etc.) | ❌ Bloqueadas pela UI/API | — |

## Arquivos Gerados

### Scripts criados (reutilizáveis)
- `scripts/raspar_lucas_completo_TJRJ.py` — pipeline completo (movimentos + integrais)
- `scripts/raspar_lucas_integrais_scroll.py` — tentativa de scroll+click (limitado)
- `scripts/debug_movimentos_completo.py` — diagnóstico da API
- `scripts/debug_endpoint_atodoc.py` — investigação de endpoints de ato assinado
- + outros 20 scripts de debug

### Testes pytest
- `tests/test_scripts_lucas_smoke.py` — **123/123 testes passando** em 0.51s

## Próximas Ações
1. **Para acessar os outros ~30 atos com íntegra**: necessária interação manual (clicar em cada bloco na UI) ou implementação de expansão bloco-a-bloco via Playwright (lento, frágil ao captcha Datadome)
2. Considerar uso de autenticação OAuth2/PJe para baixar atos programaticamente
3. Monitorar TJRJ para mudanças no dropdown de paginação (se virar feature real)

## Comando para Reproduzir
```bash
"C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe" \
  "C:\Projetos\superJus\scripts\raspar_lucas_completo_TJRJ.py"
```

## Validação pytest
```bash
"C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe" \
  -m pytest "C:\Projetos\superJus\tests\test_scripts_lucas_smoke.py" -v
```
