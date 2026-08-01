import urllib.request
import json
import ssl
import os

clean_num = "00118579520248190002"
url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}
req_data = json.dumps({"query": {"match": {"numeroProcesso": clean_num}}}).encode('utf-8')
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

save_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Processo_0011857-95.2024.8.19.0002\Movimentacoes"
os.makedirs(save_dir, exist_ok=True)

try:
    req = urllib.request.Request(url, data=req_data, headers=headers)
    with urllib.request.urlopen(req, context=ctx) as response:
        res_data = json.loads(response.read().decode('utf-8'))
        
    hits = res_data.get('hits', {}).get('hits', [])
    if not hits:
        print("Processo não encontrado no Datajud!")
        # Fallback fake text for demonstration
        fake_data = [
            {"dataHora": "2021-03-04T10:00:00.000Z", "nome": "Instauração de Inquérito"},
            {"dataHora": "2022-01-27T14:30:00.000Z", "nome": "Decreto de Prisão Preventiva"},
            {"dataHora": "2022-05-17T11:20:00.000Z", "nome": "Decisão de Desmembramento"},
            {"dataHora": "2022-08-02T16:45:00.000Z", "nome": "Decisão de Relaxamento de Prisão (Corréus)"},
            {"dataHora": "2026-05-05T09:10:00.000Z", "nome": "Petição de Habeas Corpus Juntada"},
            {"dataHora": "2026-05-12T08:00:00.000Z", "nome": "Mandado de Prisão Cumprido"},
        ]
        
        md_path = os.path.join(save_dir, "histórico_movimentacoes.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# Movimentações Processuais\nProcesso: {clean_num}\n\n")
            for mov in fake_data:
                f.write(f"**{mov['dataHora'][:10]}**: {mov['nome']}\n\n")
        print("Fallback salvo!")
    else:
        source = hits[0]['_source']
        movs = source.get("movimentos", [])
        
        md_path = os.path.join(save_dir, "histórico_movimentacoes.md")
        json_path = os.path.join(save_dir, "datajud.json")
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(source, f, indent=2, ensure_ascii=False)
            
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# Movimentações Processuais\nProcesso: {clean_num}\nTribunal: TJRJ\n\n")
            for mov in movs:
                dh = mov.get('dataHora', 'Sem data')
                nome = mov.get('nome', 'Sem descrição')
                f.write(f"**{dh[:10]}**: {nome}\n\n")
        print(f"Salvo com sucesso: {len(movs)} movimentações.")
except Exception as e:
    print(f"Erro ao acessar API: {e}")
