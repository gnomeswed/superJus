# -*- coding: utf-8 -*-
import os
import shutil

desktop_dir = r"C:\Users\Administrator\Desktop"
target_doc_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"

os.makedirs(target_doc_dir, exist_ok=True)

mapping = [
    ("DENUNCIA.pdf", "Denuncia_MP_Operacao_Delivery.pdf"),
    ("MP pelo indef.pdf", "Parecer_MP_Indeferimento_Revogacao_Preventiva.pdf"),
    ("processo Júlio .pdf", "Andamento_Oficial_TJRJ_Buzios_23_07_2026.pdf"),
    ("Julio Pereira Marcos.pdf", "Dossie_Estrategico_Integral_Julio.pdf")
]

for src_name, new_name in mapping:
    src_path = os.path.join(desktop_dir, src_name)
    if os.path.exists(src_path):
        dst_path = os.path.join(target_doc_dir, new_name)
        shutil.copy2(src_path, dst_path)
        print(f"Copiado com sucesso: {src_name} -> {dst_path}")

print("Finalização da organização dos documentos concluída!")
