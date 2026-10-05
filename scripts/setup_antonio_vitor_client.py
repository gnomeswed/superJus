# -*- coding: utf-8 -*-
import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== CRIANDO PASTA DE CLIENTE — ANTÔNIO VITOR ===")

client_dir = r"c:\Projetos\superJus\Clientes\Antonio_Vitor"
subdirs = [
    "01_Dados_do_Cliente",
    "02_Movimentacoes",
    "03_Documentos_do_Processo",
    "04_Analises_e_Estrategias"
]

for sd in subdirs:
    os.makedirs(os.path.join(client_dir, sd), exist_ok=True)

# 1. Ficha Cadastral do Cliente
ficha_file = os.path.join(client_dir, "01_Dados_do_Cliente", "Ficha_Cadastral_Antonio_Vitor.md")
ficha_content = """# 📋 FICHA CADASTRAL DO CLIENTE — ANTÔNIO VITOR

- **Nome do Cliente:** Antônio Vitor
- **Processo Principal:** `0175803-86.2023.8.19.0001`
- **Vara de Origem:** 1ª Vara Criminal da Comarca de Petrópolis / RJ
- **Classe Processual:** Ação Penal de Competência do Tribunal do Júri
- **Fase Processual Atual:** Decisão de Pronúncia Mantida pelo TJRJ (RSE Não-Provido) — Fase de Preparação do Plenário do Júri (Art. 422, CPP)
- **Relator no TJRJ (RSE):** Des. Geraldo da Silva Batista Júnior
"""

with open(ficha_file, "w", encoding="utf-8") as f:
    f.write(ficha_content)

# 2. Resumo Processual
resumo_file = os.path.join(client_dir, "04_Analises_e_Estrategias", "Resumo_Processual_Antonio_Vitor.md")
resumo_content = """# ⚖️ DOSSIÊ PROCESSUAL — ANTÔNIO VITOR

**Processo:** `0175803-86.2023.8.19.0001`  
**Órgão Julgador de Origem:** 1ª Vara Criminal da Comarca de Petrópolis/RJ  
**Classe:** Ação Penal de Competência do Tribunal do Júri  

---

## 📊 Linha do Tempo e Acórdão do TJRJ

1. **Ação Penal Originária (1ª Vara Criminal de Petrópolis):**
   * Total de movimentações auditadas: **258 movimentações**.
   * Réu pronunciado ao Tribunal do Júri pela 1ª Vara Criminal de Petrópolis.

2. **Recurso em Sentido Estrito (TJRJ — 2ª Instância):**
   * **Relator:** Des. Geraldo da Silva Batista Júnior
   * **Inclusão em Pauta:** 04/05/2026
   * **Sessão de Julgamento (14/05/2026):** **NÃO-PROVIMENTO DO RECURSO (Cód. 239)**. O TJRJ manteve na íntegra a decisão de pronúncia.
   * **Juntada de Acórdão:** 29/05/2026
   * **Publicação do Acórdão no DJE:** 08/06/2026
   * **Movimentações Recentes:** Petições das partes protocoladas em 11/06/2026 e 23/06/2026.

---

## 🎯 Próximos Passos Defensivos
- Acompanhar a baixa dos autos à 1ª Vara Criminal de Petrópolis.
- Preparar a manifestação da fase do Art. 422 do CPP (Rol de testemunhas que deporão em Plenário e juntada de documentos/perícias).
- Elaborar o mapa de quesitação e tese defensiva para a Sessão Plenária do Júri.
"""

with open(resumo_file, "w", encoding="utf-8") as f:
    f.write(resumo_content)

print(f"✅ Estrutura criada com sucesso em: {client_dir}")
