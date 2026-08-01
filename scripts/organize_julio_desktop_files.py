import os
import shutil
import fitz

desktop_dir = r'C:\Users\Administrator\Desktop'
julio_target_dir = r'c:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo'
os.makedirs(julio_target_dir, exist_ok=True)

print("Analisando documentos da Area de Trabalho para o cliente Julio Pereira Marcos...")

julio_keywords = ["júlio", "julio", "0023013", "0029845", "1116750", "saquarema", "og fernandes", "delivery", "gabriel alves"]

moved_count = 0
for file in os.listdir(desktop_dir):
    file_path = os.path.join(desktop_dir, file)
    if not os.path.isfile(file_path):
        continue
        
    is_julio_doc = False
    
    # 1. Checagem por nome do arquivo
    for kw in julio_keywords:
        if kw in file.lower():
            is_julio_doc = True
            break
            
    # 2. Se for PDF e ainda não identificado, inspecionar conteúdo
    if not is_julio_doc and file.lower().endswith('.pdf'):
        try:
            doc = fitz.open(file_path)
            full_text = ""
            for page in doc[:3]: # ler primeiras 3 páginas
                full_text += page.get_text().lower()
            doc.close()
            
            for kw in julio_keywords:
                if kw in full_text:
                    is_julio_doc = True
                    break
        except Exception as e:
            pass

    # 3. Se for arquivo do Júlio, copiar para a pasta oficial do Júlio
    if is_julio_doc:
        dest_path = os.path.join(julio_target_dir, file)
        shutil.copy2(file_path, dest_path)
        print(f"[OK] Copiado/Consolidado na pasta do Julio: {file}")
        moved_count += 1

print(f"\nConsolidacao concluida com SUCESSO! Total de {moved_count} documentos garantidos na pasta do Julio.")
