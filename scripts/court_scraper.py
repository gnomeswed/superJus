import sys
import json
import urllib.request
import re

DATAJUD_API_KEY = __import__('os').getenv('DATAJUD_API_KEY','')

def get_tribunal_endpoint(process_number_clean):
    if len(process_number_clean) != 20:
        return "tjrj" # fallback
        
    j = process_number_clean[13]
    tr = process_number_clean[14:16]
    
    if j == '3':
        return "stj"
    elif j == '4':
        return f"trf{int(tr)}"
    elif j == '5':
        return f"trt{int(tr)}"
    elif j == '8':
        uf_map = {
            '01': 'ac', '02': 'al', '03': 'ap', '04': 'am', '05': 'ba', '06': 'ce',
            '07': 'dft', '08': 'es', '09': 'go', '10': 'ma', '11': 'mt', '12': 'ms',
            '13': 'mg', '14': 'pa', '15': 'pb', '16': 'pr', '17': 'pe', '18': 'pi',
            '19': 'rj', '20': 'rn', '21': 'rs', '22': 'ro', '23': 'rr', '24': 'sc',
            '25': 'se', '26': 'sp', '27': 'to'
        }
        return f"tj{uf_map.get(tr, 'rj')}"
    
    return "tjrj"

def scrape_tjrj_process(process_number):
    clean_number = re.sub(r'\D', '', process_number)
    tribunal_alias = get_tribunal_endpoint(clean_number)
    
    print(f"[*] Iniciando busca no Datajud (CNJ) para o processo: {process_number} (Tribunal: {tribunal_alias.upper()})")
    
    url = f'https://api-publica.datajud.cnj.jus.br/api_publica_{tribunal_alias}/_search'
    headers = {
        'Authorization': DATAJUD_API_KEY,
        'Content-Type': 'application/json'
    }
    
    data = json.dumps({
        "query": {
            "match": {
                "numeroProcesso": clean_number
            }
        }
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        print("[*] Acessando portal do Datajud (CNJ)...")
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            hits = result.get('hits', {}).get('hits', [])
            if not hits:
                print("[-] Nenhum processo encontrado na base pública (pode estar em segredo de justiça ou número incorreto).")
                return None
            
            processo_data = hits[0]['_source']
            movimentos = processo_data.get('movimentos', [])
            
            movimentos_ordenados = sorted(movimentos, key=lambda x: x.get('dataHora', ''), reverse=True)
            
            movimentos_formatados = []
            for mov in movimentos_ordenados[:5]:
                data_hora = mov.get('dataHora', '')
                if data_hora and len(data_hora) >= 10:
                    data_str = data_hora[:10].split('-')
                    data_str = f"{data_str[2]}/{data_str[1]}/{data_str[0]}"
                else:
                    data_str = "Data não informada"
                
                nome = mov.get('nome', 'Movimentação sem descrição')
                movimentos_formatados.append(f"{data_str} - {nome}")
            
            assuntos_lista = processo_data.get('assuntos', [])
            assunto_principal = assuntos_lista[0].get('nome', 'Não informado') if assuntos_lista else 'Não informado'
            
            resultado = {
                "processo": process_number,
                "tribunal": tribunal_alias.upper(),
                "status": "Encontrado no Datajud (Público)",
                "classe": processo_data.get('classe', {}).get('nome', 'Não informada'),
                "assunto": assunto_principal,
                "ultimas_movimentacoes": movimentos_formatados
            }
            
            print("[+] Dados extraídos com sucesso!")
            return resultado
            
    except urllib.error.HTTPError as e:
        print(f"[-] Erro HTTP ao acessar API ({tribunal_alias}): {e.code} - {e.reason}")
        return None
    except Exception as e:
        print(f"[-] Erro ao processar dados do Datajud: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        num = sys.argv[1]
    else:
        num = "0029845-67.2026.8.19.0000"
    
    dados = scrape_tjrj_process(num)
    if dados:
        print("\n--- RESULTADO DA CONSULTA ---")
        import pprint
        pprint.pprint(dados, sort_dicts=False)


