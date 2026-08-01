import json

path = r'C:\Projetos\Super Analista Jurídico\Clientes\Processo_0011857-95.2024.8.19.0002\datajud_metadata.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Listando todas as partes encontradas no processo:")
for p in data.get('partes', []):
    nome = p.get('nome', '')
    doc = p.get('numeroDocumentoPrincipal', 'Não informado')
    tipo = p.get('tipoParticipacao', 'Não informado')
    print(f"Tipo: {tipo} | Nome Completo: {nome} | Documento: {doc}")
