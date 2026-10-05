# -*- coding: utf-8 -*-
import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

target_dir = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\Diarios_Oficiais"
os.makedirs(target_dir, exist_ok=True)

docs_src = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\Andamentos_Oficiais_PDF"

print("=== COMPILANDO DIÁRIOS OFICIAIS DE JÚLIO PEREIRA MARCOS ===")

# Copiar PDFs das publicações oficiais da pasta de andamentos para a pasta Diarios_Oficiais
orig_files = [
    ("DJERJ_29_07_2026_Publicacao.pdf", "01_DJERJ_29_07_2026_Publicacao_Oficial.pdf"),
    ("DJERJ_29_07_2026_Caderno5_Editais.pdf", "02_DJERJ_29_07_2026_Caderno5_Editais.pdf"),
    ("DESPACHO MINISTRO STJ.pdf", "03_DJEN_STJ_31_07_2026_Despacho_Ministro_Og_Fernandes.pdf"),
    ("OFÍCIO TJRJ AO STJ.pdf", "04_TJRJ_Oficio_SEI_2026_06236234_Resposta_STJ.pdf")
]

copied = []
for src_name, dst_name in orig_files:
    sf = os.path.join(docs_src, src_name)
    df = os.path.join(target_dir, dst_name)
    if os.path.exists(sf):
        shutil.copy2(sf, df)
        copied.append(dst_name)
        print(f"✅ Copiado com sucesso: {dst_name}")

md_out = os.path.join(target_dir, "Compilado_Diarios_Oficiais_Julio_Pereira_Marcos.md")

content = """# COMPILADO DE DIÁRIOS OFICIAIS E PUBLICAÇÕES — JÚLIO PEREIRA MARCOS
**Cliente:** Júlio Pereira Marcos  
**Processo Originário:** 0023013-51.2021.8.19.0078 (2ª Vara de Búzios)  
**HC TJRJ:** 0029845-67.2026.8.19.0000 (7ª Câmara Criminal)  
**RHC STJ:** HC 1.116.750 / RJ (2026/0311210-7 - 6ª Turma)  

---

## 📄 1. DJEN — Diário da Justiça Eletrônico Nacional (STJ)
* **Data da Publicação:** 31/07/2026
* **Processo:** HC nº 1.116.750 / RJ (2026/0311210-7)
* **Órgão Julgador:** Superior Tribunal de Justiça — Sexta Turma
* **Relator:** Ministro Og Fernandes
* **Arquivo PDF:** [`03_DJEN_STJ_31_07_2026_Despacho_Ministro_Og_Fernandes.pdf`](03_DJEN_STJ_31_07_2026_Despacho_Ministro_Og_Fernandes.pdf)
* **Teor do Despacho:** Indeferimento sumário da liminar, requisição de informações de urgência ao TJRJ e vista ao MPF.
* **Documento Vinculado:** [`04_TJRJ_Oficio_SEI_2026_06236234_Resposta_STJ.pdf`](04_TJRJ_Oficio_SEI_2026_06236234_Resposta_STJ.pdf) (Ofício prestado pela 2ª Vice-Presidência do TJRJ em 31/07/2026 às 12:11h).

---

## 📄 2. DJERJ — Diário da Justiça Eletrônico (2ª Vara de Búzios)
* **Data da Publicação:** 29/07/2026 (Caderno I - Judicial)
* **Processo:** Ação Penal nº 0023013-51.2021.8.19.0078
* **Órgão Julgador:** 2ª Vara Criminal de Armação dos Búzios
* **Juiz:** Dr. Danilo Marques Borges
* **Arquivo PDF:** [`01_DJERJ_29_07_2026_Publicacao_Oficial.pdf`](01_DJERJ_29_07_2026_Publicacao_Oficial.pdf)
* **Teor da Publicação:** Publicação oficial do indeferimento da revogação da prisão preventiva (fl. 1297).

---

## 📄 3. DJERJ — Caderno 5 Editais
* **Data da Publicação:** 29/07/2026
* **Arquivo PDF:** [`02_DJERJ_29_07_2026_Caderno5_Editais.pdf`](02_DJERJ_29_07_2026_Caderno5_Editais.pdf)
"""

with open(md_out, "w", encoding="utf-8") as f:
    f.write(content)

print(f"✨ Compilado de Diários salvo em: {md_out}")
