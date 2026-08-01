# -*- coding: utf-8 -*-
import os

target_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\analises"
os.makedirs(target_dir, exist_ok=True)

report_md = """# ⚖️ PARECER TÉCNICO DE DOSIMETRIA E ESTRATÉGIA RECURSAL
**Cliente / Réu:** Lucas de Souza Freitas ("Motoboy Lucas")  
**Processo:** `0011857-95.2024.8.19.0002`  
**Juízo:** 3ª Vara Criminal — Tribunal do Júri da Comarca de Niterói/RJ  
**Juíza Presidente:** Dra. Nearis dos S. Carvalho Arce  
**Data da Condenação:** 22/04/2026  
**Pena Aplicada:** 22 anos de reclusão em regime inicial FECHADO  

---

## 📌 1. RESUMO DA CONDENAÇÃO (22/04/2026)

| Delito | 1ª Fase (Pena-Base) | 2ª Fase (Agravantes / Atenuantes) | 3ª Fase / Pena Definitiva |
| :--- | :--- | :--- | :--- |
| **Homicídio Triplamente Qualificado** (Art. 121, § 2º, I, III e IV do CP) | **21 anos** *(mínimo 12 - aumento desproporcional de +9 anos)* | **21 anos** *(Magistrada negou compensação entre Confissão e Reincidência)* | **21 anos de reclusão** |
| **Ocultação de Cadáver** (Art. 211 do CP) | 1 ano + 10 dias-multa | 1 ano *(Compensada confissão com reincidência)* | **1 ano de reclusão** + 10 dias-multa |
| **PENA UNIFICADA (Art. 69 CP - Concurso Material)** | — | — | 🔴 **22 ANOS DE RECLUSÃO** (Regime Fechado) |

---

## 🚨 2. ERROS CRASSOS NA DOSIMETRIA (FUNDAMENTOS DA APELAÇÃO - ART. 593, III, 'c' DO CPP)

### A) Excesso Absurdo e Desproporcional na 1ª Fase (Pena-Base)
* **Falha da Sentença:** A magistrada fixou a pena-base em **21 anos de reclusão**, adicionando **9 anos** acima do mínimo legal (12 anos).
* **Entendimento Consolidado do STJ:** O STJ estabelece o critério fracionário de **1/6 (um sexto)** sobre a pena mínima para cada circunstância judicial desfavorável ou qualificadora excedente.
* **Cálculo Correto pelo Critério do STJ:**
  - Pena mínima do homicídio qualificado: 12 anos (144 meses).
  - Fração de 1/6 para cada vetor (2 qualificadoras excedentes + culpabilidade = 3 vetores): 3 x 24 meses = +6 anos.
  - **Pena-base devida:** No máximo **18 anos de reclusão** (em vez dos 21 anos aplicados).

### B) Negativa Ilegal de Compensação entre Confissão e Reincidência (2ª Fase)
* **Falha da Sentença:** A magistrada recusou a compensação integral sob a justificativa de "reincidência específica".
* **Violção à Súmula 545 e Tema Repetitivo 585 do STJ:** A 3ª Seção do STJ pacificou a tese de que a **Confissão Espontânea e a Reincidência (mesmo específica) são igualmente preponderantes** (Art. 67 do CP) e **DEVEM SER COMPENSADAS INTEGRALMENTE**.
* **Impacto:** A confissão de Lucas DEVE neutralizar a reincidência, não podendo haver aumento de pena nesta fase.

---

## 🎯 3. PERSPECTIVA DE REDUÇÃO DA PENA NO RECURSO DE APELAÇÃO

| Etapa | Pena Aplicada na Sentença | Pena Corrigida no STJ / TJRJ | Redução Obtida |
| :--- | :--- | :--- | :--- |
| **Homicídio Qualificado** | 21 anos | 16 a 18 anos | -3 a -5 anos |
| **Ocultação de Cadáver** | 1 ano | 1 ano | 0 |
| **PENA FINAL REVISADA** | 🔴 **22 anos** | 🟢 **17 a 19 anos** | **REDUÇÃO DE 3 A 5 ANOS DE PRISÃO** |

---

## 📋 4. TESES DE MÉRITO PARA ANULAÇÃO DO JÚRI (ART. 593, III, 'd' DO CPP)
- **Decisão Manifestamente Contrária à Prova dos Autos:** Avaliar contradições dos depoimentos e ausência de elementos conclusivos sobre o dolo do réu Lucas no homicídio.
"""

out_path = os.path.join(target_dir, "analise_dosimetria_e_recurso_lucas.md")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(report_md)

print(f"Relatório de análise do Motoboy Lucas salvo em {out_path}")
