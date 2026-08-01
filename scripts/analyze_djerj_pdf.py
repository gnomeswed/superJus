# -*- coding: utf-8 -*-
import os
import shutil
import pypdf

desktop_pdf = r"C:\Users\Administrator\Desktop\20260729ADMDJETJRJ.pdf"
target_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
target_pdf = os.path.join(target_dir, "DJERJ_29_07_2026_Publicacao.pdf")

# 1. Copiar arquivo para pasta organizada do cliente
shutil.copy2(desktop_pdf, target_pdf)
print(f"Copiado de {desktop_pdf} para {target_pdf}")

# 2. Ler e extrair texto do PDF do DJERJ
reader = pypdf.PdfReader(target_pdf)
num_pages = len(reader.pages)
print(f"Total de páginas no PDF do DJERJ: {num_pages}")

terms = [
    "0023013-51.2021.8.19.0078",
    "0022975-39.2021.8.19.0078",
    "00230135120218190078",
    "Júlio Pereira Marcos",
    "Julio Pereira Marcos",
    "Vitor Vale Nogueira",
    "Gabriel Alves Guimarães",
    "Búzios",
    "Armação dos Búzios"
]

matches = []

for page_idx, page in enumerate(reader.pages, start=1):
    text = page.extract_text()
    for term in terms:
        if term.lower() in text.lower():
            matches.append((page_idx, term, text))

print(f"\n=== RESULTADOS ENCONTRADOS NO DJERJ (29/07/2026) ===")
print(f"Total de correspondências encontradas: {len(matches)}")

out_md = []
out_md.append("# RESULTADO DA ANÁLISE DO DJERJ (29/07/2026)")
out_md.append(f"**Arquivo:** `20260729ADMDJETJRJ.pdf` ({num_pages} páginas)")
out_md.append(f"**Cliente:** Júlio Pereira Marcos\n")

if matches:
    seen_pages = set()
    for p_num, term, full_txt in matches:
        if p_num not in seen_pages:
            seen_pages.add(p_num)
            out_md.append(f"## Páginas {p_num} (Termo correspondido: `{term}`)\n```text\n")
            out_md.append(full_txt)
            out_md.append("\n```\n")
            print(f"\n--- PÁGINA {p_num} (Encontrado termo '{term}') ---")
            print(full_txt[:2000])
else:
    out_md.append("*(Nenhuma menção direta ao processo de Júlio encontrada nas páginas do PDF fornecido)*")
    print("Nenhuma menção exata aos termos do Júlio na busca primária. Exibindo resumo do PDF...")
    for idx in range(min(5, num_pages)):
        txt = reader.pages[idx].extract_text()
        print(f"--- PÁGINA {idx+1} ---")
        print(txt[:1000])

out_txt_path = os.path.join(target_dir, "analise_djerj_29_07_2026.md")
with open(out_txt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(out_md))

print(f"\nAnálise completa salva em {out_txt_path}")
