# -*- coding: utf-8 -*-
import os
import shutil
from pypdf import PdfReader

desktop_dir = r"C:\Users\Administrator\Desktop"
target_doc_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
target_txt_dir = os.path.join(target_doc_dir, "_textos_extraidos")

os.makedirs(target_doc_dir, exist_ok=True)
os.makedirs(target_txt_dir, exist_ok=True)

files_to_organize = [
    ("DENUNCIA.pdf", "Denuncia_MP_Operacao_Delivery.pdf"),
    ("MP pelo indef.pdf", "Parecer_MP_Indeferimento_Revogacao_Preventiva.pdf"),
    ("processo Júlio .pdf", "Andamento_Oficial_TJRJ_Buzios_23_07_2026.pdf"),
    ("Julio Pereira Marcos.pdf", "Documentos_Pessoais_e_Procedimento_Julio.pdf")
]

organized_summary = []

for src_name, new_name in files_to_organize:
    src_path = os.path.join(desktop_dir, src_name)
    if os.path.exists(src_path):
        dst_path = os.path.join(target_doc_dir, new_name)
        shutil.copy2(src_path, dst_path)
        print(f"Copiado: {src_name} -> {dst_path}")
        
        # Extrair texto
        try:
            reader = PdfReader(dst_path)
            extracted_text = []
            for i, page in enumerate(reader.pages, start=1):
                txt = page.extract_text()
                if txt:
                    extracted_text.append(f"--- PAGINA {i} ---\n{txt}")
            
            txt_content = "\n\n".join(extracted_text)
            txt_filename = os.path.splitext(new_name)[0] + ".txt"
            txt_path = os.path.join(target_txt_dir, txt_filename)
            
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(txt_content if txt_content else f"[PDF com imagens/scaneado: {len(reader.pages)} páginas]")
                
            organized_summary.append({
                "original": src_name,
                "salvo_como": new_name,
                "caminho_pdf": dst_path,
                "caminho_txt": txt_path,
                "paginas": len(reader.pages),
                "tamanho_bytes": os.path.getsize(dst_path)
            })
        except Exception as e:
            print(f"Erro ao extrair texto de {src_name}: {e}")

print("Organização concluída!")
