import whisper
import os
import glob
import warnings

# Silenciando warnings comuns do Whisper/PyTorch
warnings.filterwarnings("ignore")

def process_media(directory):
    print("[*] Carregando modelo de Inteligência Artificial Whisper (Local)...")
    print("[*] Isso pode demorar na primeira execução devido ao download do modelo.")
    
    try:
        # O modelo "base" é rápido e não exige placa de vídeo dedicada forte
        model = whisper.load_model("base")
    except Exception as e:
        print(f"[-] Erro ao carregar o Whisper: {e}")
        return
    
    # Suporta diversos formatos
    extensions = ("*.mp3", "*.mp4", "*.wav", "*.opus", "*.m4a", "*.ogg")
    media_files = []
    for ext in extensions:
        media_files.extend(glob.glob(os.path.join(directory, ext)))
        
    if not media_files:
        print("[-] Nenhuma mídia multimídia encontrada na pasta.")
        return
        
    print(f"[+] Encontrados {len(media_files)} arquivos. Iniciando transcrição forense...")
    
    for file_path in media_files:
        filename = os.path.basename(file_path)
        print(f"    -> Lendo áudio/vídeo: {filename}")
        
        try:
            result = model.transcribe(file_path)
            transcript_text = result["text"].strip()
            
            output_path = f"{file_path}_transcricao.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"--- TRANSCRIÇÃO DE {filename} ---\n\n")
                f.write(transcript_text)
                
            print(f"    [+] Sucesso! Texto salvo em: {os.path.basename(output_path)}")
        except Exception as e:
            print(f"    [-] Erro ao transcrever {filename}: {e}")

if __name__ == "__main__":
    target_dir = r"c:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\áudios advogado"
    
    if os.path.exists(target_dir):
        process_media(target_dir)
    else:
        print("Pasta de áudios não encontrada. Crie a pasta e coloque os arquivos.")
