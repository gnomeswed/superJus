import os
import shutil
import zipfile

output_zip = r'C:\Users\Administrator\Desktop\BACKUP_COMPLETO_ANTIGRAVITY_MEMU.zip'
project_zip_copy = r'c:\Projetos\Super Analista Jurídico\BACKUP_COMPLETO_ANTIGRAVITY_MEMU.zip'

print('Iniciando empacotamento de seguranca para formatacao...')

with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # 1. Empacotar banco e config do memU
    memu_dir = os.path.expanduser('~/.memu')
    if os.path.exists(memu_dir):
        for root, dirs, files in os.walk(memu_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.join('dot_memu', os.path.relpath(abs_path, memu_dir))
                zipf.write(abs_path, rel_path)
        print('[OK] memU (~/.memu) incluido no backup!')

    # 2. Empacotar pasta .agents (Skills e Diretrizes)
    agents_dir = r'c:\Projetos\Super Analista Jurídico\.agents'
    if os.path.exists(agents_dir):
        for root, dirs, files in os.walk(agents_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.join('dot_agents', os.path.relpath(abs_path, agents_dir))
                zipf.write(abs_path, rel_path)
        print('[OK] Skills e Regras (.agents) incluidas no backup!')

    # 3. Empacotar artefatos jurídicos e estratégias
    brain_dir = r'C:\Users\Administrator\.gemini\antigravity\brain\c9774a1b-12dc-47dd-8775-bb128c496e95'
    if os.path.exists(brain_dir):
        for root, dirs, files in os.walk(brain_dir):
            if '.system_generated' in root or 'scratch' in root or '.tempmediaStorage' in root:
                continue
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.join('brain_artifacts', os.path.relpath(abs_path, brain_dir))
                zipf.write(abs_path, rel_path)
        print('[OK] Artefatos e Estrategias (Brain Artifacts) incluidos no backup!')

shutil.copy(output_zip, project_zip_copy)
print(f'[OK] Pacote de backup finalizado com SUCESSO!')
print(f'Local 1: {output_zip}')
print(f'Local 2: {project_zip_copy}')
