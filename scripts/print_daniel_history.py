import json

with open(r"C:\Projetos\superJus\Clientes\Daniel_Ferreira_Lima\02_Movimentacoes\datajud_raw_2026-09-07_132404.json", "r", encoding="utf-8") as f:
    data = json.load(f)

g1 = [d for d in data if d.get("grau") == "G1"][0]
movs = g1.get("movimentos", [])
movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""))

print("=== MARCOS HISTÓRICOS 2018 A 2025 ===")
for m in movs_sorted:
    dt = m.get("dataHora", "")[:10]
    cod = m.get("codigo")
    nome = m.get("nome")
    comps = m.get("complementosTabelados", [])
    comp_s = "; ".join([f"{c.get('nome')} ({c.get('descricao')})" for c in comps]) if comps else ""
    
    # Highlight specific events
    if cod in [26, 12066, 12068, 12146, 11025, 11026, 898, 282, 366]:
        print(f"{dt} | Cód {cod:<5} | {nome:<30} | {comp_s}")
    elif any(w in nome.lower() for w in ["prisão", "pronúncia", "suspensão", "mandado de prisão"]):
        print(f"{dt} | Cód {cod:<5} | {nome:<30} | {comp_s}")
