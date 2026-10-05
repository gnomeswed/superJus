import sys
import os
import re
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setStrokeColor(colors.HexColor('#2B6CB0'))
        self.setLineWidth(0.8)
        self.line(36, 806, 559, 806)
        self.setFont('Helvetica-Bold', 8)
        self.setFillColor(colors.HexColor('#1A365D'))
        self.drawString(36, 812, 'SUPER ANALISTA JURIDICO - RELATORIO EXECUTIVO')
        self.setStrokeColor(colors.HexColor('#CBD5E0'))
        self.setLineWidth(0.5)
        self.line(36, 36, 559, 36)
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#718096'))
        self.drawString(36, 24, 'Documento de Acompanhamento Cautelar e Estrategico - Confidencial')
        page_str = f'Pagina {self._pageNumber} de {page_count}'
        self.drawRightString(559, 24, page_str)
        self.restoreState()

def clean_md_inline(text_str):
    # Emojis para remover
    emojis = ['⚖️', '📌', '📂', '🚨', '🛡️', '📊', '👥', '🔍', '🎯', '📋', '💬', '💡', '⚠️', '🏛️', '🛤️', '📜', '⚖']
    for e in emojis:
        text_str = text_str.replace(e, '')
    
    # Remover símbolos hash residuais do início se houver
    text_str = re.sub(r'^\#+\s*', '', text_str)
    
    # Escape '&' if not part of valid entity
    text_str = re.sub(r'&(?!(?:amp|lt|gt|quot|apos);)', '&amp;', text_str)
    
    # Trata codigo/crases soltas: `texto` -> font azul sem crase
    text_str = re.sub(r'`(.*?)`', r'<b><font color="#2B6CB0">\1</font></b>', text_str)
    
    # Processar **negrito** de forma limpa
    parts = text_str.split('**')
    res = ''
    for idx, part in enumerate(parts):
        if idx % 2 == 1:
            res += f'<b>{part}</b>'
        else:
            res += part

    # Processar *itálico* de forma limpa
    parts_i = res.split('*')
    res_i = ''
    for idx, part in enumerate(parts_i):
        if idx % 2 == 1 and len(part) > 0:
            res_i += f'<i>{part}</i>'
        else:
            res_i += part

    return res_i.strip()

def generate_perfect_pdf(md_file_path, output_pdf_path):
    if not os.path.exists(md_file_path):
        print(f'Erro: Arquivo {md_file_path} nao encontrado.')
        sys.exit(1)
        
    with open(md_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        raw_text = f.read()

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=14, leading=17,
        textColor=colors.HexColor('#1A365D'), alignment=TA_CENTER, spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'DocH1', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11, leading=14,
        textColor=colors.HexColor('#1A365D'), spaceBefore=10, spaceAfter=4
    )

    h2_style = ParagraphStyle(
        'DocH2', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=12.5,
        textColor=colors.HexColor('#2B6CB0'), spaceBefore=8, spaceAfter=3
    )

    body_style = ParagraphStyle(
        'DocBody', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13,
        textColor=colors.HexColor('#2D3748'), spaceAfter=4, alignment=TA_JUSTIFY
    )

    bullet_style = ParagraphStyle(
        'DocBullet', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13,
        textColor=colors.HexColor('#2D3748'), leftIndent=12, spaceAfter=3
    )

    th_style = ParagraphStyle(
        'TH', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=10,
        textColor=colors.white, alignment=TA_CENTER
    )

    td_style = ParagraphStyle(
        'TD', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.5, leading=9.5,
        textColor=colors.HexColor('#1A202C')
    )

    quote_style = ParagraphStyle(
        'DocQuote', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=8.5, leading=12,
        textColor=colors.HexColor('#2D3748'), leftIndent=16, rightIndent=12, spaceAfter=4, alignment=TA_JUSTIFY
    )

    story = []
    lines = raw_text.splitlines()
    in_table = False
    table_data = []

    def flush_table():
        nonlocal in_table, table_data
        if in_table and len(table_data) > 0:
            num_cols = len(table_data[0])
            total_w = 523
            if num_cols == 2:
                col_widths = [140, 383]
            elif num_cols == 3:
                col_widths = [110, 140, 273]
            elif num_cols == 4:
                col_widths = [95, 105, 110, 213]
            else:
                col_widths = [total_w / num_cols] * num_cols
            t = Table(table_data, colWidths=col_widths)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2B6CB0')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F7FAFC')]),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('TOPPADDING', (0,0), (-1,-1), 4),
            ]))
            story.append(t)
            story.append(Spacer(1, 6))
            in_table = False
            table_data = []

    for line in lines:
        l = line.strip()
        
        # Ignorar sintaxe de gráficos Mermaid e cercas de código
        if not l or l == '---' or l.startswith('```') or 'graph ' in l or '--> ' in l or 'subgraph ' in l:
            continue

        if '|' in l:
            if '---' in l:
                continue
            cells = [c.strip() for c in l.split('|')[1:-1]]
            if len(cells) >= 2:
                if not in_table:
                    in_table = True
                    table_data = []
                if len(table_data) == 0:
                    p_cells = [Paragraph(clean_md_inline(c), th_style) for c in cells]
                else:
                    p_cells = [Paragraph(clean_md_inline(c), td_style) for c in cells]
                table_data.append(p_cells)
                continue

        # Descarregar tabela pendente se mudou de bloco
        flush_table()

        # Título Principal (H1)
        if l.startswith('# '):
            clean_t = clean_md_inline(l[2:].strip())
            story.append(Paragraph(clean_t, title_style))
            story.append(HRFlowable(width='100%', thickness=1.5, color=colors.HexColor('#2B6CB0'), spaceBefore=2, spaceAfter=8))
            continue

        # Seções de Nível 2 (H2)
        if l.startswith('## '):
            clean_h = clean_md_inline(l[3:].strip())
            story.append(Paragraph(clean_h, h1_style))
            story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#CBD5E0'), spaceBefore=2, spaceAfter=4))
            continue

        # Sub-seções de Nível 3 (H3 - Ex: ### A. Excesso de Prazo...)
        if l.startswith('### '):
            clean_h3 = clean_md_inline(l[4:].strip())
            story.append(Paragraph(clean_h3, h2_style))
            continue

        # Citações em bloco (Blockquotes)
        if l.startswith('>'):
            clean_q = re.sub(r'^>\s*', '', l)
            fmt = clean_md_inline(clean_q)
            if fmt:
                story.append(Paragraph(fmt, quote_style))
            continue

        # Tópicos com marcadores (bullets)
        if l.startswith('* ') or l.startswith('- ') or re.match(r'^\d+\.\s', l):
            clean_b = re.sub(r'^\*\s+|^\-\s+|^\d+\.\s+', '', l)
            fmt = clean_md_inline(clean_b)
            story.append(Paragraph(f'• {fmt}', bullet_style))
            continue

        # Parágrafo comum
        fmt = clean_md_inline(l)
        story.append(Paragraph(fmt, body_style))

    # Finalizar tabela caso o arquivo termine em tabela
    flush_table()

    doc = SimpleDocTemplate(output_pdf_path, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=48, bottomMargin=48)
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f'PDF PERFEITAMENTE FORMATADO GERADO EM: {output_pdf_path}')

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        md_in = sys.argv[1]
        pdf_out = sys.argv[2]
        generate_perfect_pdf(md_in, pdf_out)
    elif len(sys.argv) == 2:
        md_in = sys.argv[1]
        pdf_out = os.path.splitext(md_in)[0] + '.pdf'
        generate_perfect_pdf(md_in, pdf_out)
    else:
        print("Uso: python gerar_pdf_profissional.py <arquivo.md> [arquivo.pdf]")
        sys.exit(1)
