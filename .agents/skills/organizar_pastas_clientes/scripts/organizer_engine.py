# -*- coding: utf-8 -*-
import os
import hashlib
import shutil
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def compute_hash(filepath):
    """Calcula o hash SHA256 do arquivo para comparação de conteúdo real."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return None

def sanitize_filename(filename):
    """Padroniza nomes estranhos removendo sufixos duplicados e caracteres ruidosos."""
    cleaned = re.sub(r'\s*\(\d+\)', '', filename)
    cleaned = re.sub(r' - Copy| - Cópia|_Duplicata', '', cleaned, flags=re.IGNORECASE)
    return cleaned.strip()

def is_junk_file(filename, filesize):
    """Identifica arquivos lixo, temporários ou vazios sem valor jurídico."""
    lower_name = filename.lower()
    if filesize == 0 and not lower_name.endswith('.gitkeep'):
        return True
    if lower_name.endswith(('.tmp', '.bak', '.swp', '.ds_store', 'thumbs.db')):
        return True
    if lower_name == 'desktop.ini':
        return True
    return False

def audit_and_clean_client_dir(client_dir, dry_run=True):
    """Audita a pasta do cliente, detectando duplicatas por hash, arquivos lixo e nomes fora de padrão."""
    print(f"=== AUDITORIA E HIGIENIZAÇÃO: {os.path.basename(client_dir)} ===")
    print(f"Modo: {'SIMULAÇÃO (Dry-Run)' if dry_run else 'EXECUÇÃO REAL'}\n")

    seen_hashes = {}
    duplicates = []
    junk_files = []
    rename_suggestions = []

    for root, dirs, files in os.walk(client_dir):
        for f in files:
            fp = os.path.join(root, f)
            try:
                size = os.path.getsize(fp)
                if is_junk_file(f, size):
                    junk_files.append((fp, f, size))
                    continue

                h = compute_hash(fp)
                if h:
                    if h in seen_hashes:
                        duplicates.append((fp, seen_hashes[h]))
                    else:
                        seen_hashes[h] = fp

                sanitized = sanitize_filename(f)
                if sanitized != f:
                    rename_suggestions.append((fp, os.path.join(root, sanitized)))

            except Exception as e:
                print(f"Erro ao analisar {f}: {e}")

    print(f"* Arquivos Irrelevantes / Lixo Encontrados: {len(junk_files)}")
    for fp, f, size in junk_files:
        print(f"  • [LIXO] {os.path.relpath(fp, client_dir)} ({size} bytes)")
        if not dry_run:
            os.remove(fp)

    print(f"\n* Arquivos Duplicados Identificados por Hash SHA256: {len(duplicates)}")
    for dup, original in duplicates:
        print(f"  • [DUPLICADO] {os.path.relpath(dup, client_dir)}")
        print(f"    Original em: {os.path.relpath(original, client_dir)}")
        if not dry_run:
            os.remove(dup)

    print(f"\n* Sugestões de Padronização de Nome: {len(rename_suggestions)}")
    for old_fp, new_fp in rename_suggestions:
        print(f"  • [RENOMEAR] {os.path.basename(old_fp)} ➔ {os.path.basename(new_fp)}")
        if not dry_run and not os.path.exists(new_fp):
            os.rename(old_fp, new_fp)

    print("\nAuditoria concluída com sucesso!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python organizer_engine.py <caminho_da_pasta_do_cliente> [--execute]")
        sys.exit(1)
    
    target_path = sys.argv[1]
    execute_mode = "--execute" in sys.argv
    audit_and_clean_client_dir(target_path, dry_run=not execute_mode)
