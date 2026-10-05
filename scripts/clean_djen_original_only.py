# -*- coding: utf-8 -*-
import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== SEPARANDO DOCUMENTOS ORIGINAIS DE CERTIDÕES GERADAS POR IA ===")

base_dir = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal"
diarios_dir = os.path.join(base_dir, "documentos_processo", "Diarios_Oficiais")
ai_cert_dir = os.path.join(base_dir, "analises_e_automacoes_ia", "Certidoes_Sinteticas_IA")

os.makedirs(ai_cert_dir, exist_ok=True)

# Lista de arquivos gerados/sintetizados pela IA para mover para fora de Diarios_Oficiais
generated_files = [
    "DJEN_ID_602661584_07_05_2026_Ata_Distribuicao.pdf",
    "DJEN_ID_602775138_07_05_2026_Decisao_Liminar.pdf",
    "DJEN_ID_626141945_02_06_2026_Pauta_Julgamento.pdf"
]

for fname in generated_files:
    src = os.path.join(diarios_dir, fname)
    dst = os.path.join(ai_cert_dir, fname)
    if os.path.exists(src):
        try:
            shutil.move(src, dst)
            print(f"✅ Movido para IA: {fname}")
        except Exception as e:
            print(f"Erro ao mover {fname}: {e}")

# Atualizar o arquivo markdown compilado para refletir estritamente os PDFs autênticos baixados
md_file = os.path.join(diarios_dir, "Compilado_Diarios_Oficiais_Julio_Pereira_Marcos.md")
content = """# REPOSITÓRIO OFICIAL DE DIÁRIOS E PUBLICAÇÕES (APENAS PDFs ORIGINAIS BAIXADOS)
**Cliente:** JÚLIO PEREIRA MARCOS  
**Auditoria de Autenticidade:** 05/08/2026  

> [!NOTE]
> Esta pasta contém **estritamente os arquivos PDFs originais e brutos** baixados diretamente dos portais do TJRJ, DJERJ e STJ (sem qualquer formatação ou edição por IA).

---

## 📄 1. PDFs Originais do STJ e TJRJ (DJEN / SEI)

1. **Despacho do Min. Og Fernandes no STJ (DJEN 31/07/2026):**
   * **Arquivo PDF Original:** [`03_DJEN_STJ_31_07_2026_Despacho_Ministro_Og_Fernandes.pdf`](03_DJEN_STJ_31_07_2026_Despacho_Ministro_Og_Fernandes.pdf)
   * **Chancela:** Assinado eletronicamente por Antônio Herman de Vasconcellos e Benjamin. Código: `c9dccefb-8409-48f8-a4f2-e5dea6c78a00`.

2. **Ofício SEI da 2ª Vice-Presidência do TJRJ ao STJ (31/07/2026):**
   * **Arquivo PDF Original:** [`04_TJRJ_Oficio_SEI_2026_06236234_Resposta_STJ.pdf`](04_TJRJ_Oficio_SEI_2026_06236234_Resposta_STJ.pdf)

---

## 📄 2. PDFs Originais do DJERJ (Tribunal de Justiça do Rio de Janeiro)

1. **DJERJ Edição de 29/07/2026 (Publicação Oficial):**
   * **Arquivo PDF Original:** [`01_DJERJ_29_07_2026_Publicacao_Oficial.pdf`](01_DJERJ_29_07_2026_Publicacao_Oficial.pdf)

2. **DJERJ Edição de 29/07/2026 (Caderno 5 Editais):**
   * **Arquivo PDF Original:** [`02_DJERJ_29_07_2026_Caderno5_Editais.pdf`](02_DJERJ_29_07_2026_Caderno5_Editais.pdf)
"""

with open(md_file, "w", encoding="utf-8") as f:
    f.write(content)

print(f"✨ Compilado atualizado em {md_file}")
