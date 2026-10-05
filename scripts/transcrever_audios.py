import os
import glob
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("ERRO: GOOGLE_API_KEY não encontrada no .env")
    exit(1)

genai.configure(api_key=api_key)

audio_dir = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\áudios advogado"
output_file = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\analises\Transcricao_Audios.md"

mp3_files = glob.glob(os.path.join(audio_dir, "*.mp3"))

if not mp3_files:
    print("Nenhum arquivo MP3 encontrado.")
    exit(0)

print(f"Encontrados {len(mp3_files)} áudios. Iniciando transcrição...")

with open(output_file, "w", encoding="utf-8") as f:
    f.write("# Transcrições dos Áudios do Cliente\n\n")

for mp3 in mp3_files:
    filename = os.path.basename(mp3)
    print(f"Processando {filename}...")
    try:
        audio_file = genai.upload_file(path=mp3)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([audio_file, "Ouça este áudio do WhatsApp (pode ser o advogado e o cliente conversando sobre o caso criminal do Júlio Pereira Marcos). Transcreva o áudio relatando os pontos cruciais e as instruções passadas."])
        
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"## Arquivo: {filename}\n")
            f.write(f"{response.text}\n\n")
            
        print(f"{filename} transcrito com sucesso!")
    except Exception as e:
        print(f"Erro no {filename}: {e}")
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"## Arquivo: {filename}\n")
            f.write(f"Erro ao transcrever: {e}\n\n")

print("Transcrições concluídas e salvas em analises/Transcricao_Audios.md")
