from fpdf import FPDF
import os
import glob
import datetime

class DossierPDF(FPDF):
    """Gerador de Dossiê em PDF profissional para entrega ao Magistrado."""
    
    def __init__(self, client_name, office_name="Escritório de Advocacia Criminal"):
        super().__init__()
        self.client_name = client_name
        self.office_name = office_name
        self.set_auto_page_break(auto=True, margin=25)
    
    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(113, 113, 122)  # zinc-500
        self.cell(0, 8, self.office_name, align="L")
        self.cell(0, 8, f"Cliente: {self.client_name}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(228, 228, 231)  # zinc-200
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(161, 161, 170)  # zinc-400
        self.cell(0, 10, f"Super Analista Jurídico | Página {self.page_no()}/{{nb}}", align="C")
    
    def add_cover(self):
        """Capa profissional."""
        self.add_page()
        self.ln(60)
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(9, 9, 11)  # zinc-950
        self.cell(0, 15, "DOSSIÊ DE DEFESA", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(5)
        self.set_font("Helvetica", "", 16)
        self.set_text_color(113, 113, 122)
        self.cell(0, 10, self.client_name, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(20)
        self.set_draw_color(37, 99, 235)  # accent blue
        self.set_line_width(0.8)
        self.line(70, self.get_y(), 140, self.get_y())
        self.ln(20)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(161, 161, 170)
        today = datetime.datetime.now().strftime("%d/%m/%Y")
        self.cell(0, 8, f"Gerado automaticamente em {today}", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 8, "pelo Super Analista Jurídico (Motor DeepSeek)", align="C", new_x="LMARGIN", new_y="NEXT")
    
    def add_section(self, title, content):
        """Adiciona uma seção formatada."""
        self.add_page()
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(9, 9, 11)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(37, 99, 235)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 60, self.get_y())
        self.ln(8)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(39, 39, 42)  # zinc-800
        # Limpa caracteres que o FPDF não suporta
        clean = content.encode("latin-1", errors="replace").decode("latin-1")
        self.multi_cell(0, 5.5, clean)

def generate_dossier(client_name, client_base_path, output_path=None):
    """Compila todos os documentos de análise em um PDF profissional."""
    pdf = DossierPDF(client_name)
    pdf.alias_nb_pages()
    pdf.add_cover()
    
    # Varre todos os .md e .txt da pasta de análises
    analises_dir = os.path.join(client_base_path, "analises")
    pecas_dir = os.path.join(client_base_path, "pecas")
    
    for search_dir, section_prefix in [(analises_dir, "Análise"), (pecas_dir, "Peça")]:
        if os.path.exists(search_dir):
            for filepath in sorted(glob.glob(os.path.join(search_dir, "*.md"))):
                filename = os.path.basename(filepath).replace(".md", "").replace("_", " ")
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    pdf.add_section(f"{section_prefix}: {filename}", content)
                except:
                    continue
            for filepath in sorted(glob.glob(os.path.join(search_dir, "*.txt"))):
                filename = os.path.basename(filepath).replace(".txt", "").replace("_", " ")
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    pdf.add_section(f"{section_prefix}: {filename}", content)
                except:
                    continue
    
    if output_path is None:
        output_path = os.path.join(client_base_path, f"Dossie_{client_name.replace(' ', '_')}.pdf")
    
    pdf.output(output_path)
    return output_path
