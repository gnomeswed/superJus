---
name: Organizar e Higienizar Pastas de Clientes
description: "Audita, higieniza, remove duplicatas por hash SHA256, elimina arquivos lixo/temporários e padroniza a taxonomia das pastas de clientes do escritório."
---

# Organizar e Higienizar Pastas de Clientes

Esta skill fornece uma rotina automatizada e padronizada para auditedar, higienizar, desduplicar e organizar as pastas e documentos dos clientes no repositório `c:\Projetos\superJus\Clientes`.

---

## 🎯 Objetivos da Skill

1. **Eliminar Arquivos Irrelevantes e Lixo Digital:**
   - Detectar e remover arquivos `.tmp`, `.bak`, `.swp`, `desktop.ini`, `Thumbs.db`, `.DS_Store` e arquivos de 0-byte sem utilidade jurídica.
2. **Desduplicação por Hash Seguro (SHA256):**
   - Comparar o conteúdo binário real dos arquivos. Se dois arquivos possuírem o mesmo hash, eliminar a cópia duplicada (ex: `reportPDF (7).pdf` x `reportPDF (5).pdf` ou `DENUNCIA (1).pdf` x `DENUNCIA.pdf`).
3. **Padronização da Taxonomia do Cliente:**
   - Estruturar a pasta do cliente no padrão institucional:
     ```text
     Clientes/[Nome_Sobrenome]/
     └── Caso_Principal/
         ├── analises/
         ├── documentos_processo/
         └── pecas/
     ```
4. **Renomeação de Arquivos Estranhos:**
   - Padronizar nomes genéricos (`New Text Document.txt`, `rad5CCBF.html`, `jdsjs.pdf`) para nomes jurídicos descritivos (ex: `Ata_Audiencia_Instrucao.txt`, `Peca_Defensiva_HC.pdf`).

---

## 🛠️ Como Executar a Higienização

### 1. Execução em Modo Simulação (Dry-Run — Sem Apagar Nada)
Para auditar a pasta do cliente e visualizar tudo o que será limpo ou renomeado **sem realizar alterações físicas**:

```bash
python c:\Projetos\superJus\.agents\skills\organizar_pastas_clientes\scripts\organizer_engine.py "c:\Projetos\superJus\Clientes\Nome_Do_Cliente"
```

### 2. Execução Real (Limpeza e Padronização Efetiva)
Para aplicar a limpeza, remoção de duplicatas por hash e renomeação definitiva:

```bash
python c:\Projetos\superJus\.agents\skills\organizar_pastas_clientes\scripts\organizer_engine.py "c:\Projetos\superJus\Clientes\Nome_Do_Cliente" --execute
```

---

## 🔒 Regras de Segurança Anti-Perda de Dados
- **Hash Obligatório:** Nenhum arquivo é apagado por semelhança de nome; a duplicidade é verificada estritamente pelo hash SHA256 do conteúdo.
- **Preservação de Documentos Únicos:** Documentos escaneados com nomes aleatórios (`hrhe.pdf`, `motoboy.pdf`, `radED68D.html`) NUNCA são excluídos caso sejam únicos; eles são apenas organizados ou sugeridos para renomeação com base no seu conteúdo.
- **Relatório de Auditoria:** O script emite um relatório detalhado de cada arquivo movido, mantido ou renomeado.
