import os
import shutil

print("=== SEPARANDO DOCUMENTOS OFICIAIS DE GERAÇÕES DA IA ===")

base_dir = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal"
doc_processo_dir = os.path.join(base_dir, "documentos_processo")
ai_dir = os.path.join(base_dir, "analises_e_automacoes_ia")

os.makedirs(ai_dir, exist_ok=True)

# Pastas geradas por IA ou automações para mover para fora de documentos_processo
folders_to_move = [
    "Consultas_e_Logs_Automacoes",
    "_textos_extraidos",
    "paginas_renderizadas"
]

for folder in folders_to_move:
    src = os.path.join(doc_processo_dir, folder)
    dst = os.path.join(ai_dir, folder)
    
    if os.path.exists(src):
        try:
            shutil.move(src, dst)
            print(f"Movido com sucesso: {folder} -> {ai_dir}")
        except Exception as e:
            print(f"Erro ao mover {folder}: {e}")
    else:
        print(f"Aviso: {folder} não encontrada em documentos_processo.")

print("Separação concluída. A pasta 'documentos_processo' agora contém apenas arquivos oficiais.")
