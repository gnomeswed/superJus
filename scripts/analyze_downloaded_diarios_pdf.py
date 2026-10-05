# -*- coding: utf-8 -*-
import os
import re

pdf_dir = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\Diarios_Oficiais"

keywords = [
    "0023013", "0029845", "0022975", "0001140", "1.116.750",
    "julio", "júlio", "vitor vale", "gabriel alves", "og fernandes",
    "sidney rosa", "06236234", "búzios", "buzios"
]

results = []
results.append("=== ANÁLISE DETALHADA DOS DIÁRIOS BAIXADOS — CITAÇÕES DO PROCESSO DE JÚLIO ===")

for f in sorted(os.listdir(pdf_dir)):
    if f.endswith(".pdf"):
        fp = os.path.join(pdf_dir, f)
        results.append(f"\n============================================================")
        results.append(f"📄 ANALISANDO ARQUIVO PDF: {f}")
        results.append(f"============================================================")
        
        try:
            raw_bytes = open(fp, 'rb').read()
            # Extract printable ascii and utf-8 text chunks
            strings = re.findall(b'[\x20-\x7E\xA0-\xFF]{4,}', raw_bytes)
            full_text = ' '.join([s.decode('utf-8', errors='ignore') for s in strings])
            
            lines = full_text.splitlines()

            matched_lines = []
            for i, line in enumerate(lines):
                for kw in keywords:
                    if kw in line.lower():
                        matched_lines.append((kw, line.strip()))
            
            if matched_lines:
                results.append(f"✅ Ocorrências encontradas ({len(matched_lines)} trechos):")
                for kw, line in matched_lines[:15]:
                    results.append(f"  • [Termo '{kw}']: {line[:220]}")
            else:
                results.append("ℹ️ Nenhuma ocorrência direta de texto puro no fluxo stream do PDF (pode ser imagem escaneada ou formato gráfico).")
                
        except Exception as e:
            results.append(f"Erro ao ler PDF {f}: {e}")

res_txt = "\n".join(results)
target_path = r"c:\Projetos\superJus\analise_diarios_pdf_result.txt"
with open(target_path, "w", encoding="utf-8") as f:
    f.write(res_txt)

print("SUCESSO: Análise dos Diários em PDF concluída e salva em " + target_path)
