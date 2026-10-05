import os
import shutil
import glob

print("=== ORGANIZANDO PASTA DOCUMENTOS_PROCESSO ===")

base_dir = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"

# Pastas de destino
folders = {
    "Andamentos_Oficiais_PDF": [
        "Andamento_*.pdf", 
        "DESPACHO MINISTRO STJ.pdf", 
        "OFÍCIO TJRJ AO STJ.pdf", 
        "DJERJ_*.pdf", 
        "Decisao_Fl_1297_*.jpg", 
        "Processo Nº*.pdf",
        "recebeu a DENUNCIA.pdf",
        "Portal de Serviços.pdf"
    ],
    "Pecas_e_Manifestacoes_PDF": [
        "DENUNCIA.pdf", 
        "HC COM PEDIDO DE LIMINAR*.pdf", 
        "HC julio.pdf", 
        "MP pelo indef.pdf"
    ],
    "Documentos_Defesa_PDF": [
        "Doc_*.pdf",
        "Prova_Trechos_Audiencia.pdf"
    ],
    "Consultas_e_Logs_Automacoes": [
        "*.txt", 
        "*.md",
        "*.lnk"
    ]
}

for folder, patterns in folders.items():
    folder_path = os.path.join(base_dir, folder)
    os.makedirs(folder_path, exist_ok=True)
    
    for pattern in patterns:
        search_path = os.path.join(base_dir, pattern)
        files = glob.glob(search_path)
        
        for file in files:
            if os.path.isfile(file):
                filename = os.path.basename(file)
                dst = os.path.join(folder_path, filename)
                try:
                    shutil.move(file, dst)
                    print(f"Movido: {filename} -> {folder}")
                except Exception as e:
                    print(f"Erro ao mover {filename}: {e}")

print("Organização concluída!")
