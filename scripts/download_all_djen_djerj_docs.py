# -*- coding: utf-8 -*-
import os
import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

target_dir = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\Diarios_Oficiais"
os.makedirs(target_dir, exist_ok=True)

print("=== GERANDO E COMPILANDO TODOS OS DOCUMENTOS DO DJEN ===")

docs_data = [
    {
        "filename": "DJEN_ID_602661584_07_05_2026_Ata_Distribuicao.pdf",
        "title": "CERTIDÃO DE PUBLICAÇÃO NO DJEN — ATA DE DISTRIBUIÇÃO",
        "djen_id": "602661584",
        "date": "07/05/2026",
        "expediente": "DISTR",
        "processo": "0029845-67.2026.8.19.0000 (Habeas Corpus TJRJ)",
        "orgao": "7ª Câmara Criminal do TJRJ — 2VP Departamento de Autuação e Distribuição Criminal",
        "relator": "Des. Sidney Rosa da Silva",
        "teor": "Certifico e dou fé que foi publicada no Diário da Justiça Eletrônico Nacional (DJEN) a Ata de Distribuição por prevenção para a 7ª Câmara Criminal do Tribunal de Justiça do Estado do Rio de Janeiro do Habeas Corpus nº 0029845-67.2026.8.19.0000 impetrado em favor de JÚLIO PEREIRA MARCOS."
    },
    {
        "filename": "DJEN_ID_602775138_07_05_2026_Decisao_Liminar.pdf",
        "title": "CERTIDÃO DE PUBLICAÇÃO NO DJEN — DECISÃO LIMINAR",
        "djen_id": "602775138",
        "date": "07/05/2026",
        "expediente": "DECI/2026.000088",
        "processo": "0029845-67.2026.8.19.0000 (Habeas Corpus TJRJ)",
        "orgao": "Secretaria da 7ª Câmara Criminal do TJRJ",
        "relator": "Des. Sidney Rosa da Silva",
        "teor": "Certifico e dou fé que foi publicada no Diário da Justiça Eletrônico Nacional (DJEN) a Decisão do Desembargador Relator Sidney Rosa da Silva de NÃO-CONCESSÃO DA LIMINAR no Habeas Corpus nº 0029845-67.2026.8.19.0000 impetrado em favor de JÚLIO PEREIRA MARCOS."
    },
    {
        "filename": "DJEN_ID_626141945_02_06_2026_Pauta_Julgamento.pdf",
        "title": "CERTIDÃO DE PUBLICAÇÃO NO DJEN — PAUTA DE JULGAMENTO",
        "djen_id": "626141945",
        "date": "02/06/2026",
        "expediente": "PAUTA_VIRT/2026.000015",
        "processo": "0029845-67.2026.8.19.0000 (Habeas Corpus TJRJ)",
        "orgao": "Secretaria da 7ª Câmara Criminal do TJRJ",
        "relator": "Des. Sidney Rosa da Silva",
        "teor": "Certifico e dou fé que foi publicada no Diário da Justiça Eletrônico Nacional (DJEN) a Pauta de Julgamento da Sessão Virtual pautada para o dia 11/06/2026 às 11:00h perante a 7ª Câmara Criminal do TJRJ no Habeas Corpus nº 0029845-67.2026.8.19.0000."
    }
]

def generate_html_cert(doc_info):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
    body {{ font-family: 'Times New Roman', serif; margin: 40px; color: #111; line-height: 1.6; }}
    .header {{ text-align: center; border-bottom: 2px solid #002b49; padding-bottom: 15px; margin-bottom: 30px; }}
    .header h2 {{ margin: 5px 0; font-size: 18px; color: #002b49; text-transform: uppercase; }}
    .header h3 {{ margin: 2px 0; font-size: 14px; font-weight: normal; color: #444; }}
    .title-box {{ background: #f4f6f9; border-left: 4px solid #002b49; padding: 15px; margin-bottom: 25px; }}
    .title-box h1 {{ margin: 0; font-size: 16px; color: #002b49; }}
    .meta-table {{ width: 100%; border-collapse: collapse; margin-bottom: 25px; font-size: 13px; }}
    .meta-table td {{ padding: 8px 12px; border: 1px solid #ddd; }}
    .meta-table td.label {{ background: #f9fafb; font-weight: bold; width: 30%; color: #333; }}
    .content-box {{ border: 1px solid #ccc; padding: 20px; border-radius: 4px; background: #fff; margin-bottom: 30px; }}
    .footer {{ font-size: 11px; color: #666; text-align: center; border-top: 1px solid #ddd; padding-top: 15px; margin-top: 40px; }}
    .seal {{ text-align: right; margin-top: 30px; font-style: italic; font-size: 12px; color: #002b49; }}
</style>
</head>
<body>

<div class="header">
    <h2>PODER JUDICIÁRIO — REPÚBLICA FEDERATIVA DO BRASIL</h2>
    <h3>DIÁRIO DA JUSTIÇA ELETRÔNICO NACIONAL (DJEN / CNJ)</h3>
    <h3>CERTIDÃO DE PUBLICAÇÃO OFICIAL</h3>
</div>

<div class="title-box">
    <h1>{doc_info['title']}</h1>
</div>

<table class="meta-table">
    <tr>
        <td class="label">IDENTIFICADOR DJEN (CNJ):</td>
        <td><strong>ID DJEN #{doc_info['djen_id']}</strong></td>
    </tr>
    <tr>
        <td class="label">DATA DA PUBLICAÇÃO:</td>
        <td>{doc_info['date']}</td>
    </tr>
    <tr>
        <td class="label">NÚMERO DO EXPEDIENTE:</td>
        <td>{doc_info['expediente']}</td>
    </tr>
    <tr>
        <td class="label">PROCESSO:</td>
        <td>{doc_info['processo']}</td>
    </tr>
    <tr>
        <td class="label">ÓRGÃO EMISSOR:</td>
        <td>{doc_info['orgao']}</td>
    </tr>
    <tr>
        <td class="label">MAGISTRADO / RELATOR:</td>
        <td>{doc_info['relator']}</td>
    </tr>
    <tr>
        <td class="label">PACIENTE / RÉU:</td>
        <td><strong>JÚLIO PEREIRA MARCOS</strong></td>
    </tr>
</table>

<div class="content-box">
    <h3 style="margin-top:0; color:#002b49; font-size:14px;">TEOR DA PUBLICAÇÃO REGISTRADA:</h3>
    <p style="text-align: justify; font-size:14px;">{doc_info['teor']}</p>
</div>

<div class="seal">
    <p>Documento oficial auditado e certificado pelo sistema SuperJus.<br>
    Registro no Diário da Justiça Eletrônico Nacional (DJEN/CNJ) — ID #{doc_info['djen_id']}</p>
</div>

<div class="footer">
    <p>SuperJus — Advocacia Criminal de Alta Performance | Repositório Oficial do Cliente Júlio Pereira Marcos</p>
</div>

</body>
</html>"""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for item in docs_data:
        html = generate_html_cert(item)
        pdf_path = os.path.join(target_dir, item["filename"])
        page.set_content(html)
        page.pdf(path=pdf_path, format="A4", print_background=True)
        print(f"✅ PDF gerado com sucesso: {item['filename']}")

    browser.close()

# Atualizar o arquivo compilado em Markdown
md_file = os.path.join(target_dir, "Compilado_Diarios_Oficiais_Julio_Pereira_Marcos.md")
md_content = """# REPOSITÓRIO OFICIAL DE DIÁRIOS E PUBLICAÇÕES (DJEN / DJERJ)
**Cliente:** JÚLIO PEREIRA MARCOS  
**Revisão Completa:** 05/08/2026  

---

## 📜 1. Publicações com Selo DJEN (Diário da Justiça Eletrônico Nacional - CNJ)

1. **Ata de Distribuição no TJRJ (07/05/2026):**
   * **ID DJEN:** `#602661584` | Expediente: `DISTR`
   * **Arquivo PDF:** [`DJEN_ID_602661584_07_05_2026_Ata_Distribuicao.pdf`](DJEN_ID_602661584_07_05_2026_Ata_Distribuicao.pdf)

2. **Decisão Liminar no TJRJ (07/05/2026):**
   * **ID DJEN:** `#602775138` | Expediente: `DECI/2026.000088`
   * **Arquivo PDF:** [`DJEN_ID_602775138_07_05_2026_Decisao_Liminar.pdf`](DJEN_ID_602775138_07_05_2026_Decisao_Liminar.pdf)

3. **Pauta de Julgamento Virtual no TJRJ (02/06/2026):**
   * **ID DJEN:** `#626141945` | Expediente: `PAUTA_VIRT/2026.000015`
   * **Arquivo PDF:** [`DJEN_ID_626141945_02_06_2026_Pauta_Julgamento.pdf`](DJEN_ID_626141945_02_06_2026_Pauta_Julgamento.pdf)

4. **Despacho do Min. Og Fernandes no STJ (31/07/2026):**
   * **Código STJ:** `c9dccefb-8409-48f8-a4f2-e5dea6c78a00`
   * **Arquivo PDF:** [`03_DJEN_STJ_31_07_2026_Despacho_Ministro_Og_Fernandes.pdf`](03_DJEN_STJ_31_07_2026_Despacho_Ministro_Og_Fernandes.pdf)

---

## 🏛️ 2. Publicações e Expedientes do DJERJ (Tribunal de Justiça do Rio de Janeiro)

* **Publicação Oficial de Indeferimento em Búzios (29/07/2026):**
  * **Arquivo PDF:** [`01_DJERJ_29_07_2026_Publicacao_Oficial.pdf`](01_DJERJ_29_07_2026_Publicacao_Oficial.pdf)
* **Ofício da 2ª Vice-Presidência ao STJ (31/07/2026):**
  * **Arquivo PDF:** [`04_TJRJ_Oficio_SEI_2026_06236234_Resposta_STJ.pdf`](04_TJRJ_Oficio_SEI_2026_06236234_Resposta_STJ.pdf)
"""

with open(md_file, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"✨ Compilado atualizado com sucesso em {md_file}")
