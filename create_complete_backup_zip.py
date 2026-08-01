import os
import shutil
import zipfile

output_zip = r'C:\Users\Administrator\Desktop\BACKUP_COMPLETO_ANTIGRAVITY_MEMU.zip'
project_zip_copy = r'c:\Projetos\Super Analista Jurídico\BACKUP_COMPLETO_ANTIGRAVITY_MEMU.zip'

print('Iniciando empacotamento INTEGRAL (com todos os documentos de processos)...')

with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # 1. Empacotar banco e config do memU
    memu_dir = os.path.expanduser('~/.memu')
    if os.path.exists(memu_dir):
        for root, dirs, files in os.walk(memu_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.join('dot_memu', os.path.relpath(abs_path, memu_dir))
                zipf.write(abs_path, rel_path)
        print('[OK] Banco e memorias memU incluidos!')

    # 2. Empacotar pasta .agents (Skills e Diretrizes)
    agents_dir = r'c:\Projetos\Super Analista Jurídico\.agents'
    if os.path.exists(agents_dir):
        for root, dirs, files in os.walk(agents_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.join('dot_agents', os.path.relpath(abs_path, agents_dir))
                zipf.write(abs_path, rel_path)
        print('[OK] Skills e Regras (.agents) incluidas!')

    # 3. Empacotar pasta Clientes completa (com todas as petições, movimentações, transcrições e PDFs)
    clientes_dir = r'c:\Projetos\Super Analista Jurídico\Clientes'
    if os.path.exists(clientes_dir):
        for root, dirs, files in os.walk(clientes_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                # Ignorar arquivos de vídeo pesados se houverem (> 100MB) para não explodir o zip, mantendo textos e PDFs
                if file.lower().endswith(('.mp4', '.mkv', '.avi')) and os.path.getsize(abs_path) > 100 * 1024 * 1024:
                    continue
                rel_path = os.path.join('Clientes', os.path.relpath(abs_path, clientes_dir))
                zipf.write(abs_path, rel_path)
        print('[OK] Pasta Clientes (Documentos, Movimentacoes e Pecas) incluida!')

    # 4. Empacotar PDFs de processos da Área de Trabalho
    desktop_dir = r'C:\Users\Administrator\Desktop'
    if os.path.exists(desktop_dir):
        for file in os.listdir(desktop_dir):
            if file.lower().endswith(('.pdf', '.txt', '.json')) and not file.startswith('BACKUP'):
                abs_path = os.path.join(desktop_dir, file)
                rel_path = os.path.join('Desktop_Documentos', file)
                zipf.write(abs_path, rel_path)
        print('[OK] Documentos e PDFs de processos da Area de Trabalho incluidos!')

    # 5. Empacotar artefatos jurídicos (Brain Artifacts)
    brain_dir = r'C:\Users\Administrator\.gemini\antigravity\brain\c9774a1b-12dc-47dd-8775-bb128c496e95'
    if os.path.exists(brain_dir):
        for root, dirs, files in os.walk(brain_dir):
            if '.system_generated' in root or 'scratch' in root or '.tempmediaStorage' in root:
                continue
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.join('brain_artifacts', os.path.relpath(abs_path, brain_dir))
                zipf.write(abs_path, rel_path)
        print('[OK] Artefatos e Estrategias (Brain Artifacts) incluidos!')

shutil.copy(output_zip, project_zip_copy)
print(f'[OK] PACOTE DE BACKUP INTEGRAL FINALIZADO COM SUCESSO!')
print(f'Tamanho do arquivo ZIP: {os.path.getsize(output_zip) / (1024*1024):.2f} MB')
