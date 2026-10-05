---
name: memoria_memu
description: "Protocolo de acesso à memória persistente compartilhada memU (SQLite local em C:\Users\Administrator\.memu\memu.sqlite3), sincronizada com Antigravity, Hermes Agent e OpenCode. Use SEMPRE no início de qualquer tarefa para consultar (retrieve) o histórico do caso/cliente e grave (commit) novos aprendizados, andamentos e decisões estratégicas."
---

# Protocolo de Memória Persistente — memU

Esta skill define como **consultar** e **gravar** na memória compartilhada memU, o mesmo banco SQLite usado pelo Antigravity, Hermes Agent e OpenCode.

**Banco:** `C:\Users\Administrator\.memu\memu.sqlite3`
**CLI:** `memu` (instalado no PATH)
**Tabela principal:** `memu_recall_files` (memórias) + `memu_recall_file_segments` (segmentos com embeddings)

---

## 🧠 1. CONSULTAR (Obrigatório no início de cada tarefa)

Antes de qualquer análise, estratégia ou redação de peça, **sempre** busque o que já está registrado sobre o caso/cliente.

### Opção A — Busca semântica (recomendada)

```bash
memu retrieve "julio pereira marcos prisao preventiva excesso prazo"
```

Retorna os segmentos e arquivos mais relevantes por similaridade de embedding. Use termos do caso, do cliente, do processo ou do tema jurídico.

### Opção B — Listar todas as memórias

```bash
memu list-files
```

### Opção C — Script de busca no projeto

```bash
python scripts/memu_retrieve.py "termos da busca"
```

---

## 💾 2. GRAVAR (Commit de novos aprendizados)

Sempre que surgir um **novo andamento processual, decisão, tese, aprendizado técnico ou preferência**, grave na memória para os outros agentes (Antigravity/Hermes/OpenCode) também enxergarem.

### Opção A — Script helper do projeto (recomendada)

```bash
python scripts/memu_store.py --name "Nome_Da_Memoria" --track "memory|skill" --description "Descrição curta" --content "Conteúdo completo da memória"
```

- `--track memory`: fatos, casos, andamentos, históricos.
- `--track skill`: aprendizados técnicos, procedimentos, preferências.

### Opção B — Via CLI memu (payload JSON)

```bash
memu commit - <<'EOF'
{
  "recall_files": [
    {
      "name": "andamento_julio_06_08_2026",
      "track": "memory",
      "description": "Descrição do novo andamento",
      "content": "Conteúdo completo..."
    }
  ]
}
EOF
```

O `memu commit` **gera os embeddings automaticamente** e segmenta o conteúdo, então a memória fica pesquisável por similaridade.

---

## 📋 3. REGRAS DE NOMENCLATURA

- **Casos/andamentos:** `andamento_<cliente>_<dd_mm_aaaa>` ou `memoria_caso_<cliente>.md`
- **Teses/pontos fortes:** `Ponto_Forte_<tema>_<Cliente>`
- **Aprendizados técnicos:** `memoria_<tema>.md` com `track: skill`
- **Descrição:** sempre curta e acionável (1 linha), com o número do processo quando houver.

---

## 🔁 4. FLUXO PADRÃO EM TODA TAREFA

1. **Retrieve** com termos do caso/cliente/tema → recupera contexto prévio.
2. Execute a tarefa (análise, peça, pesquisa).
3. **Commit** qualquer fato novo ou decisão tomada.
4. Confirme no final que a memória foi gravada (`memu list-files`).
