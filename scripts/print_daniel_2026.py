import json

with open(r"C:\Projetos\superJus\Clientes\Daniel_Ferreira_Lima\02_Movimentacoes\datajud_raw_2026-09-07_132404.json", "r", encoding="utf-8") as f:
    data = json.load(f)

g1 = [d for d in data if d.get("grau") == "G1"][0]
movs = g1.get("movimentos", [])
movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""))

print(f"Total movimentos: {len(movs_sorted)}")
for m in movs_sorted:
    dt = m.get("dataHora", "")[:19].replace("T", " ")
    cod = m.get("codigo")
    nome = m.get("nome")
    comps = m.get("complementosTabelados", [])
    comp_s = "; ".join([f"{c.get('nome')} ({c.get('descricao')})" for c in comps]) if comps else ""
    if any(k in dt for k in ["2026-04", "2026-05", "2026-06"]):
        print(f"{dt} | Cód {cod:<5} | {nome:<30} | {comp_s}")
