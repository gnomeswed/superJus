# -*- coding: utf-8 -*-
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Projetos\superJus\Clientes\Lucas_Dias_Oliveira\03_Documentos_do_Processo"
target_dir = os.path.join(base_dir, "PDFs_Documentos_Publicos")
os.makedirs(target_dir, exist_ok=True)

print("=== COMPILANDO TODOS OS DOCUMENTOS PÚBLICOS DE LUCAS TAXISTA EM PDF ===")

pje_docs = [
    {
        "id": "281122579",
        "title": "Decisão - Ratificação do Recebimento da Denúncia e AIJ",
        "date": "11/05/2026",
        "type": "Decisão Judicial (Dra. Juliana Grillo El Jaick)",
        "file_txt": "Doc_PJe_01_id281122579.txt"
    },
    {
        "id": "280659639",
        "title": "Despacho - Retificação do Rito Processual",
        "date": "08/05/2026",
        "type": "Despacho Judicial",
        "file_txt": "Doc_PJe_02_id280659639.txt"
    },
    {
        "id": "278145702",
        "title": "Decisão - Recebimento da Denúncia e Indeferimento da Liberdade",
        "date": "27/04/2026",
        "type": "Decisão Judicial",
        "file_txt": "Doc_PJe_03_id278145702.txt"
    },
    {
        "id": "277050897",
        "title": "Decisão - Indeferimento da Restituição do Veículo Fiat Siena",
        "date": "20/04/2026",
        "type": "Decisão Judicial",
        "file_txt": "Doc_PJe_04_id277050897.txt"
    },
    {
        "id": "275104905",
        "title": "Decisão - Indeferimento da Liberdade Provisória",
        "date": "10/04/2026",
        "type": "Decisão Judicial",
        "file_txt": "Doc_PJe_05_id275104905.txt"
    },
    {
        "id": "274550507",
        "title": "Autuação e Deferimento da Quebra de Sigilo de Dados Telemáticos",
        "date": "08/04/2026",
        "type": "Decisão / Autuação",
        "file_txt": "Doc_PJe_06_id274550507.txt"
    },
    {
        "id": "273106393",
        "title": "Ata da Audiência de Custódia (Parte 1)",
        "date": "31/03/2026",
        "type": "Ata de Audiência",
        "file_txt": "Doc_PJe_07_id273106393.txt"
    },
    {
        "id": "273145859",
        "title": "Ata da Audiência de Custódia (Parte 2)",
        "date": "31/03/2026",
        "type": "Ata de Audiência",
        "file_txt": "Doc_PJe_08_id273145859.txt"
    }
]

def clean_text_for_doc(txt_content):
    # Extract only lines that are actual decision text
    lines = txt_content.split('\n')
    clean_lines = []
    capture = False
    for line in lines:
        if "Poder Judici" in line or "DECIS" in line or "Processo:" in line:
            capture = True
        if capture:
            if "Content-Type" in line or "MultipartBoundary" in line or "font-awesome" in line:
                break
            clean_lines.append(line)
    return "\n".join(clean_lines[:150]) if clean_lines else txt_content[:1500]

def make_html(doc_info, content):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
    body {{ font-family: Arial, sans-serif; margin: 35px; color: #222; line-height: 1.5; }}
    .header {{ text-align: center; border-bottom: 2px solid #1a365d; padding-bottom: 12px; margin-bottom: 20px; }}
    .header h2 {{ margin: 4px 0; font-size: 16px; color: #1a365d; text-transform: uppercase; }}
    .header h4 {{ margin: 2px 0; font-size: 13px; font-weight: normal; color: #555; }}
    .info-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 12px; }}
    .info-table td {{ padding: 6px 10px; border: 1px solid #cbd5e0; }}
    .info-table td.label {{ background: #edf2f7; font-weight: bold; width: 25%; color: #2d3748; }}
    .content-box {{ border: 1px solid #e2e8f0; padding: 18px; border-radius: 4px; background: #fff; white-space: pre-wrap; font-size: 13px; font-family: 'Courier New', monospace; }}
    .footer {{ font-size: 10px; color: #718096; text-align: center; border-top: 1px solid #e2e8f0; padding-top: 10px; margin-top: 30px; }}
</style>
</head>
<body>

<div class="header">
    <h2>PODER JUDICIÁRIO DO ESTADO DO RIO DE JANEIRO</h2>
    <h4>4ª VARA CRIMINAL DA COMARCA DE NITERÓI</h4>
    <h4>PROCESSO Nº 0808595-36.2026.8.19.0002</h4>
</div>

<table class="info-table">
    <tr>
        <td class="label">DOCUMENTO:</td>
        <td><strong>{doc_info['title']}</strong></td>
    </tr>
    <tr>
        <td class="label">ID DOCUMENTO PJe:</td>
        <td>{doc_info['id']}</td>
    </tr>
    <tr>
        <td class="label">DATA DO ATO:</td>
        <td>{doc_info['date']}</td>
    </tr>
    <tr>
        <td class="label">NOME DO RÉU:</td>
        <td><strong>LUCAS DIAS OLIVEIRA (LUCAS TAXISTA)</strong></td>
    </tr>
    <tr>
        <td class="label">NATUREZA:</td>
        <td>{doc_info['type']}</td>
    </tr>
</table>

<div class="content-box">
{content}
</div>

<div class="footer">
    <p>Documento Público Extraído do Processo Eletrônico (PJe TJRJ) — Repositório SuperJus Lucas Dias Oliveira</p>
</div>

</body>
</html>"""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for item in pje_docs:
        txt_path = os.path.join(base_dir, item["file_txt"])
        if os.path.exists(txt_path):
            with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
                raw_txt = f.read()
            body_txt = clean_text_for_doc(raw_txt)
            html = make_html(item, body_txt)
            pdf_fname = f"Doc_PJe_ID_{item['id']}_{item['date'].replace('/', '_')}.pdf"
            pdf_path = os.path.join(target_dir, pdf_fname)
            page.set_content(html)
            page.pdf(path=pdf_path, format="A4", print_background=True)
            print(f"✅ PDF Público Gerado: {pdf_fname}")
        else:
            print(f"⚠️ TXT não encontrado para ID {item['id']}")

    browser.close()

print(f"\n✨ Todos os 8 documentos públicos foram compilados em PDF na pasta:\n   {target_dir}")
