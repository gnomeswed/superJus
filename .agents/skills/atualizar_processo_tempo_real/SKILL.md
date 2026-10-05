---
name: atualizar_processo_tempo_real
description: >
  Protocolo Operacional Padrão (POP) de consulta e atualização processual em tempo real.
  Integra MCPs (mcp-juridico-brasil, legal-datajud, superjus-sqlite, brasil-dados-abertos,
  superjus-fetch, superjus-markitdown), validação anti-alucinação de códigos TPU ambíguos,
  raspagem Playwright e persistência no memU. Ativar SEMPRE que o advogado pedir para
  "atualizar", "checar", "verificar", "consultar" ou "ver como está" um processo.
---

# Skill: Atualizar Processo em Tempo Real

## Quando Ativar
- Sempre que o advogado solicitar atualização, consulta ou verificação de qualquer processo.
- No monitoramento diário programado (cron das 10h).
- Quando receber uma notificação de movimentação via DJe/DJEN.

## Execução Rápida Automatizada (CLI Oficial)
Para executar toda a cadeia de 5 fases de forma automatizada com decodificador TPU e persistência:
```bash
python scripts/superjus_consultar.py --processo <NUMERO_CNJ> --cliente "<NOME_CLIENTE>"
```

---

## Cadeia de 5 Fases (Executar em Ordem)

### FASE 1 — Memória Persistente (OBRIGATÓRIA)
Antes de qualquer consulta externa, resgatar o que já sabemos.

**Ferramentas:**
- `superjus-sqlite` → `read_query`:
  ```sql
  SELECT name, description, content, created_at 
  FROM memu_recall_files 
  WHERE name LIKE '%{nome_cliente}%' 
     OR description LIKE '%{numero_processo}%'
  ORDER BY created_at DESC
  ```
- Ler `01_Dados_do_Cliente/ficha_cadastral_*.md` do diretório do cliente.

**Saída:** Números de processo conhecidos, última data de checagem, status cautelar vigente.

---

### FASE 2 — Consulta MCP Estruturada (Fonte Primária)
Obter dados oficiais do DataJud/CNJ via servidores MCP.

**Pipeline de chamadas (nesta ordem):**

1. **`mcp-juridico-brasil` → `buscar_processo_por_numero`**
   - Params: `numero_processo`, `tribunal` (ex: "TJRJ")
   - Retorna: metadados, classe, assuntos, órgão julgador, partes, movimentações

2. **`mcp-juridico-brasil` → `listar_movimentacoes`**
   - Params: `numero_processo`, `tribunal`, `limite: 30`
   - Retorna: top 30 movimentações com complementos tabelados

3. **`mcp-juridico-brasil` → `monitorar_processo`**
   - Params: `numero_processo`, `tribunal`, `desde_iso` (última checagem da Fase 1)
   - Retorna: se houve atualização desde a última consulta

4. **`mcp-juridico-brasil` → `listar_intimacoes`**
   - Params: `numero_processo` (opcional), `apenas_pendentes: true`
   - Retorna: intimações pendentes no Domicílio Judicial Eletrônico

5. **`mcp-juridico-brasil` → `calcular_proximo_prazo`**
   - Params: `numero_processo`, `tribunal`, `uf: "RJ"`, `tipo_ato` (se aplicável)
   - Retorna: data fatal do próximo prazo com feriados

6. **`brasil-dados-abertos` → `consultar_feriados_nacionais`**
   - Params: `ano` (ano corrente)
   - Para validação cruzada dos prazos calculados

> **AVISO CRÍTICO:** O DataJud pode ter defasagem de T+1 a T+7 dias.
> A ausência de um movimento NÃO significa que ele não ocorreu no tribunal.

---

### FASE 3 — Raspagem Viva (Confirmação em Tempo Real)
Acessar o portal do tribunal diretamente quando o DataJud for insuficiente ou ambíguo.

**Quando executar:**
- Quando a Fase 4 identificar código TPU ambíguo
- Quando o advogado pedir atualização "de hoje"
- Quando houver prazo correndo com menos de 5 dias úteis

**Por tribunal:**

| Tribunal | Método | URL |
|:---------|:-------|:----|
| TJRJ PJe 1G | Playwright | `tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam` |
| TJRJ Portal | Playwright | `www3.tjrj.jus.br/consultaprocessual` |
| STJ | `superjus-fetch` | `processo.stj.jus.br/processo/pesquisa` |
| DJEN | `superjus-fetch` | `comunicaapi.pje.jus.br/api/v1/comunicacao` |

**Regras:**
1. Salvar texto completo em `03_Documentos_do_Processo/detalhes_pje_{cliente}_live_{YYYY-MM-DD}.txt`
2. Timeout: 35s (TJRJ), 20s (STJ), 15s (APIs REST)
3. **Se o PJe redirecionar para login:** Registrar como "documento exige certificado digital" e NÃO inferir conteúdo

---

### FASE 4 — Validação Anti-Alucinação (GATE DE SEGURANÇA)

> **OBRIGATÓRIA para qualquer movimentação que afete custódia/liberdade.**

#### Lista de Códigos TPU Ambíguos (NÃO indicam resultado)

| Código | Nome | Armadilha |
|:------:|:-----|:----------|
| `12146` | Liberdade Provisória | Tanto deferimento quanto indeferimento |
| `12068` | Prisão Preventiva | Tanto decretação quanto revogação |
| `198` | Decisão | Qualquer deliberação interlocutória |
| `11383` | Ato Ordinatório | Mero expediente sem conteúdo decisório |
| `581` | Documento | Juntada genérica — pode ser qualquer coisa |
| `60` | Expedição de Documento | Não diferencia alvará de ofício de rotina |

#### Checklist Obrigatório

```
□ 1. O código TPU está na lista de ambíguos acima?
     → SIM: NÃO interpretar pelo nome. Buscar teor da decisão.
     → NÃO: Interpretar normalmente.

□ 2. Existe complementosTabelados[] com resultado explícito?
     → SIM: Usar o complemento ("deferido", "indeferido", "concedido").
     → NÃO: Marcar como "⚠️ APRECIAÇÃO SEM RESULTADO EXPLÍCITO".

□ 3. O mesmo código já apareceu antes no mesmo processo?
     → SIM: Comparar com a decisão anterior conhecida.
     → NÃO: Tratar como inédito. Não presumir resultado.

□ 4. Conseguimos ler o teor completo da decisão (Fase 3)?
     → SIM: Extrair dispositivo literal ("DEFIRO", "INDEFIRO", "MANTENHO").
     → NÃO: Informar ao advogado e sugerir acesso via login OAB/PJe.

□ 5. O status informado é compatível com o que o advogado sabe?
     → SIM: Confirmar.
     → NÃO: PARAR. Perguntar ao advogado antes de emitir relatório.
```

**MCP de apoio:** `legal-datajud` → `analyze_tpu_movement` para decodificar códigos.
**Skill de apoio:** `revisao_anti_alucinacao` para auditoria final.

---

### FASE 5 — Persistência e Atualização de Documentos

**Ações obrigatórias ao concluir:**

1. **Gravar no memU:**
   ```bash
   python scripts/memu_store.py \
     --name "atualizacao_{cliente}_{YYYY_MM_DD}" \
     --track "memory" \
     --description "Atualização processual {numero}: {resumo}" \
     --content "{dados_completos}"
   ```

2. **Atualizar arquivos do cliente:**
   - `01_Dados_do_Cliente/ficha_cadastral_*.md` → status cautelar atual
   - `03_Documentos_do_Processo/RESUMO_PROCESSO_*.md` → cronologia completa
   - `02_Movimentacoes/datajud_raw_*.json` → JSON bruto do DataJud com timestamp
   - `02_Movimentacoes/movimentacoes_*.md` → tabela cronológica Markdown

3. **Se houve decisão importante:** Converter PDFs com `superjus-markitdown` → `convert_and_save_markdown`.

---

## 7 Regras de Ouro

1. **Nunca interpretar código TPU pelo nome quando envolve liberdade.** Sempre validar pelo teor ou confirmação do advogado.
2. **Sempre consultar memória (Fase 1) antes de tribunais.** Evita trabalho duplicado e carrega contexto.
3. **DataJud é referência, não verdade absoluta.** Cruzar com PJe/portal quando crítico.
4. **Se PJe pedir login, NÃO inferir conteúdo.** Informar ao advogado.
5. **Sempre gravar no memU ao final.** Cada consulta gera aprendizado.
6. **Usar MCPs, não scripts avulsos.** Reutilizar ferramentas em vez de criar scripts descartáveis.
7. **Na dúvida, perguntar ao advogado.** Melhor ser cauteloso do que errar sobre liberdade de uma pessoa.
