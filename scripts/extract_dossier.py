from pypdf import PdfReader
import os

pdf_path = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Dossie_Julio_Pereira_Marcos.pdf"
out_path = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Movimentacoes\todas_movimentacoes_tjrj.txt"

try:
    reader = PdfReader(pdf_path)
    txt = ''.join([page.extract_text() for page in reader.pages])
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("DADOS EXTRAÍDOS DO DOSSIÊ DO CLIENTE:\n\n")
        f.write(txt)
    print("Extraido com sucesso!")
except Exception as e:
    print(f"Erro: {e}")
