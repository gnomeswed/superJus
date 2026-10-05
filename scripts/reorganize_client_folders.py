# -*- coding: utf-8 -*-
import os
import shutil

base_dir = r"c:\Projetos\superJus\Clientes"

def log(msg):
    print(f"[REORG] {msg}")

# 1. Mover conteúdo de Processo_0011857-95.2024.8.19.0002 para Lucas_Freitas\Caso_Principal\documentos_processo
src_lucas = os.path.join(base_dir, "Processo_0011857-95.2024.8.19.0002")
dst_lucas = os.path.join(base_dir, "Lucas_Freitas", "Caso_Principal", "documentos_processo")
os.makedirs(dst_lucas, exist_ok=True)

if os.path.exists(src_lucas):
    for root, dirs, files in os.walk(src_lucas):
        for f in files:
            src_fp = os.path.join(root, f)
            rel = os.path.relpath(src_fp, src_lucas)
            dst_fp = os.path.join(dst_lucas, rel)
            os.makedirs(os.path.dirname(dst_fp), exist_ok=True)
            if not os.path.exists(dst_fp):
                shutil.copy2(src_fp, dst_fp)
                log(f"Copiado para Lucas_Freitas: {rel}")
            else:
                log(f"Já existe em Lucas_Freitas: {rel}")
    shutil.rmtree(src_lucas)
    log("Removida pasta avulsa Processo_0011857-95.2024.8.19.0002")

# 2. Mover conteúdo de Processo_00230135120218190078 para Júlio_Pereira_Marcos\Caso_Principal
src_julio = os.path.join(base_dir, "Processo_00230135120218190078")
dst_julio = os.path.join(base_dir, "Júlio_Pereira_Marcos", "Caso_Principal")

if os.path.exists(src_julio):
    for f in os.listdir(src_julio):
        src_fp = os.path.join(src_julio, f)
        dst_fp = os.path.join(dst_julio, f)
        if not os.path.exists(dst_fp):
            shutil.copy2(src_fp, dst_fp)
            log(f"Copiado para Júlio_Pereira_Marcos: {f}")
    shutil.rmtree(src_julio)
    log("Removida pasta avulsa Processo_00230135120218190078")

# 3. Renomear pastas com inconsistências de nome
renames = [
    ("ecildo", "Ecildo_Victor"),
    ("Leandro mecânico", "Leandro_Mecanico"),
    ("Pastor Juneo", "Pastor_Juneo"),
    ("Taxista", "Lucas_Dias_Oliveira")
]

for old_name, new_name in renames:
    old_path = os.path.join(base_dir, old_name)
    new_path = os.path.join(base_dir, new_name)
    if os.path.exists(old_path) and not os.path.exists(new_path):
        os.rename(old_path, new_path)
        log(f"Renomeado: '{old_name}' -> '{new_name}'")

log("Reorganização de pastas dos clientes finalizada com SUCESSO!")
