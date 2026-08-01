import sys
import os
import markdown
from fpdf import FPDF
from html.parser import HTMLParser

class ProfessionalPDF(FPDF):
    def header(self):
        # Logo / Nome do Escritório
        self.set_font("Arial", "B", 18)
        self.set_text_color(44, 62, 80)  # Dark Blue
        self.cell(0, 10, "SUPER ANALISTA JURÍDICO", border=False, ln=True, align="L")
        
        # Linha decorativa
        self.set_draw_color(52, 152, 219) # Light Blue
        self.set_line_width(0.8)
        self.line(15, 22, 195, 22)
        
        self.ln(10)

    def footer(self):
        self.set_y(-20)
        self.set_draw_color(189, 195, 199) # Light Gray
        self.set_line_width(0.5)
        self.line(15, 277, 195, 277)
        
        self.set_font("Arial", "I", 8)
        self.set_text_color(127, 140, 141) # Gray
        self.cell(0, 10, "Relatório Gerado por IA - Acompanhamento Estratégico", align="L")
        
        self.set_x(15)
        self.cell(0, 10, f"Página {self.page_no()}", align="R")

class HTMLtoPDF(HTMLParser):
    def __init__(self, pdf):
        super().__init__()
        self.pdf = pdf
        self.pdf.set_font("Arial", size=11)
        self.pdf.set_text_color(44, 62, 80)
        
        self.in_bold = False
        self.in_italic = False
        self.in_h1 = False
        self.in_h2 = False
        self.in_h3 = False
        self.in_li = False
        
    def set_normal_font(self):
        if self.in_bold:
            self.pdf.set_font("Arial", "B", 11)
        elif self.in_italic:
            self.pdf.set_font("Arial", "I", 11)
        else:
            self.pdf.set_font("Arial", "", 11)
        self.pdf.set_text_color(44, 62, 80) # Dark text

    def handle_starttag(self, tag, attrs):
        if tag in ['b', 'strong']:
            self.in_bold = True
            self.set_normal_font()
        elif tag in ['i', 'em']:
            self.in_italic = True
            self.set_normal_font()
        elif tag == 'h1':
            self.in_h1 = True
            self.pdf.ln(5)
            self.pdf.set_font("Arial", "B", 16)
            self.pdf.set_text_color(41, 128, 185) # Blue Title
        elif tag == 'h2':
            self.in_h2 = True
            self.pdf.ln(8)
            self.pdf.set_font("Arial", "B", 13)
            self.pdf.set_text_color(192, 57, 43) # Redish / Professional Wine for sections
            # Draw a subtle background or line
            self.pdf.set_fill_color(236, 240, 241) # Light gray bg
        elif tag == 'h3':
            self.in_h3 = True
            self.pdf.ln(5)
            self.pdf.set_font("Arial", "B", 11)
            self.pdf.set_text_color(39, 174, 96) # Green
        elif tag == 'li':
            self.in_li = True
            self.pdf.ln(2)
            self.set_normal_font()
            self.pdf.cell(6, 6, chr(149), align="R") # Bullet point
        elif tag == 'p':
            self.pdf.ln(5)
            self.set_normal_font()
        elif tag == 'hr':
            self.pdf.ln(5)
            y = self.pdf.get_y()
            self.pdf.set_draw_color(189, 195, 199)
            self.pdf.line(15, y, 195, y)
            self.pdf.ln(2)

    def handle_endtag(self, tag):
        if tag in ['b', 'strong']:
            self.in_bold = False
            self.set_normal_font()
        elif tag in ['i', 'em']:
            self.in_italic = False
            self.set_normal_font()
        elif tag == 'h1':
            self.in_h1 = False
            self.pdf.ln(8)
        elif tag == 'h2':
            self.in_h2 = False
            self.pdf.ln(6)
        elif tag == 'h3':
            self.in_h3 = False
            self.pdf.ln(4)
        elif tag == 'li':
            self.in_li = False
            self.pdf.ln(2)
        elif tag == 'p':
            self.pdf.ln(3)

    def handle_data(self, data):
        data = data.replace('\n', ' ').strip()
        if data:
            # Multi_cell handles word wrap. 
            # If we are inside H2, let's use background fill
            if self.in_h2:
                self.pdf.multi_cell(0, 8, data.encode('latin-1', 'replace').decode('latin-1'), fill=True)
            else:
                self.pdf.multi_cell(0, 6, data.encode('latin-1', 'replace').decode('latin-1'))

def generate_pdf(markdown_file, output_pdf):
    if not os.path.exists(markdown_file):
        print(f"Erro: Arquivo {markdown_file} não encontrado.")
        sys.exit(1)

    with open(markdown_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    html_text = markdown.markdown(md_text)

    pdf = ProfessionalPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    parser = HTMLtoPDF(pdf)
    parser.feed(html_text)

    pdf.output(output_pdf)
    print(f"PDF profissional gerado com sucesso em: {output_pdf}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python gerar_pdf.py <caminho_entrada_md> <caminho_saida_pdf>")
        sys.exit(1)
        
    input_md = sys.argv[1]
    output_file = sys.argv[2]
    generate_pdf(input_md, output_file)
