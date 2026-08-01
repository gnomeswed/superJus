import json
import os

json_path = r"C:\Projetos\Super Analista Jurídico\Clientes\Processo_0011857-95.2024.8.19.0002\datajud_metadata.json"
out_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Processo_0011857-95.2024.8.19.0002\Movimentacoes"
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "histórico_movimentacoes.md")

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

movs = data.get("movimentos", [])
with open(out_file, 'w', encoding='utf-8') as f:
    f.write("# Movimentações Processuais\nProcesso: 0011857-95.2024.8.19.0002\n\n")
    for mov in movs:
        dh = mov.get("dataHora", "Sem data")
        nome = mov.get("nome", "Sem descrição")
        f.write(f"**{dh[:10]}**: {nome}\n\n")

print(f"Salvas {len(movs)} movimentações.")
