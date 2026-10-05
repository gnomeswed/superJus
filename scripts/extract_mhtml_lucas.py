#!/usr/bin/env python3
"""Extract text content from MHTML files for Lucas taxista process"""
import os, re, html

MHTML_DIR = "C:/Projetos/superJus/Clientes/Lucas_Dias_Oliveira/processo taxista"
OUT_DIR = "C:/Projetos/superJus/Clientes/Lucas_Dias_Oliveira/03_Documentos_do_Processo"
os.makedirs(OUT_DIR, exist_ok=True)

def extract_mhtml_text(filepath):
    """Extract readable text from MHTML file"""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Find the HTML part
    html_match = re.search(r'<!DOCTYPE[^>]*>(.*)', content, re.DOTALL)
    if not html_match:
        html_match = re.search(r'<html[^>]*>(.*)', content, re.DOTALL)
    
    if not html_match:
        return "Could not extract HTML"
    
    html_content = html_match.group(0)
    
    # Remove style and script blocks
    text = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove HTML comments
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    
    # Replace block elements with newlines
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</(?:p|div|h[1-6]|li|tr)>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<(?:td|th)[^>]*>', ' | ', text, flags=re.IGNORECASE)
    
    # Remove remaining tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Decode HTML entities
    text = html.unescape(text)
    
    # Clean up whitespace
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if line:
            lines.append(line)
    
    return '\n'.join(lines)

files = sorted([f for f in os.listdir(MHTML_DIR) if f.endswith('.mhtml')])
print(f"Processing {len(files)} MHTML files...\n")

all_docs = []

for i, fname in enumerate(files):
    fpath = os.path.join(MHTML_DIR, fname)
    print(f"[{i+1}/{len(files)}] {fname}")
    
    text = extract_mhtml_text(fpath)
    
    # Find doc ID
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        raw = f.read()
    id_match = re.search(r'idProcessoDoc=(\d+)', raw)
    doc_id = id_match.group(1) if id_match else "unknown"
    
    # Find title/subject from the document
    title_match = re.search(r'<title[^>]*>([^<]+)</title>', raw, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else "Sem título"
    
    # Try to find document type/name from the content
    tipo_match = re.search(r'Tipo do Documento[:\s]*([^<\n]+)', text)
    tipo = tipo_match.group(1).strip() if tipo_match else "Não identificado"
    
    data_match = re.search(r'Data[:\s]*(\d{2}/\d{2}/\d{4})', text)
    data = data_match.group(1) if data_match else "Não identificada"
    
    # Save extracted text
    out_fname = f"Doc_PJe_{i+1:02d}_id{doc_id}.txt"
    out_path = os.path.join(OUT_DIR, out_fname)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f"Arquivo original: {fname}\n")
        f.write(f"ID Documento PJe: {doc_id}\n")
        f.write(f"Título: {title}\n")
        f.write(f"Tipo: {tipo}\n")
        f.write(f"Data: {data}\n")
        f.write(f"{'='*60}\n\n")
        f.write(text)
    
    print(f"  Doc ID: {doc_id}")
    print(f"  Tipo: {tipo}")
    print(f"  Data: {data}")
    print(f"  Texto extraído: {len(text)} chars → {out_fname}")
    
    all_docs.append({
        "arquivo_original": fname,
        "doc_id": doc_id,
        "tipo": tipo,
        "data": data,
        "tamanho_texto": len(text),
        "arquivo_saida": out_fname
    })
    print()

# Save index
import json
index_path = os.path.join(OUT_DIR, "indice_documentos_pje.json")
with open(index_path, 'w', encoding='utf-8') as f:
    json.dump({
        "processo": "0808595-36.2026.8.19.0002",
        "cliente": "Lucas Dias Oliveira (Taxista)",
        "data_extracao": "2026-08-16",
        "total_documentos": len(all_docs),
        "documentos": all_docs
    }, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"EXTRAÇÃO CONCLUÍDA!")
print(f"Total de documentos: {len(all_docs)}")
print(f"Arquivos salvos em: {OUT_DIR}")
print(f"Índice: {index_path}")
