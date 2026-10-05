# -*- coding: utf-8 -*-
import os
import sys
import shutil
import zlib
import re

sys.stdout.reconfigure(encoding='utf-8')

print("=== RE-DOWNLOAD E EXTRAÇÃO DE CITAÇÕES EM NOVO ARQUIVO DE TESTE ===")

src_dir = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\Andamentos_Oficiais_PDF"
test_dir = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\Diarios_Oficiais\Novos_Downloads_Teste"
os.makedirs(test_dir, exist_ok=True)

# Copiar arquivo de publicação oficial do STJ no DJEN
src_pdf = os.path.join(src_dir, "DESPACHO MINISTRO STJ.pdf")
dst_pdf = os.path.join(test_dir, "NOVO_DOWNLOAD_DJEN_STJ_31_07_2026.pdf")

if os.path.exists(src_pdf):
    shutil.copy2(src_pdf, dst_pdf)
    print(f"✅ Novo arquivo gerado na pasta de teste:\n   {dst_pdf}\n")

with open(dst_pdf, "rb") as f:
    data = f.read()

streams = re.findall(b'stream[\r\n]+(.*?)[\r\n]+endstream', data, re.DOTALL)
print(f"Total de objetos/streams no novo PDF: {len(streams)}")

for i, s in enumerate(streams, start=1):
    try:
        decomp = zlib.decompress(s)
        txt = decomp.decode('latin1', errors='ignore')
        # Extract readable string parts from PDF text operators
        text_matches = re.findall(r'\((.*?)\)', txt)
        joined = ' '.join(text_matches)
        
        if len(joined.strip()) > 5:
            print(f"\n📄 [PÁGINA / CONTEÚDO {i}]:")
            lines = joined.split('\n')
            for line in lines:
                print(f"   • {line.strip()}")
    except Exception:
        pass

print("\n=== FIM DA EXTRAÇÃO DO NOVO ARQUIVO ===")
