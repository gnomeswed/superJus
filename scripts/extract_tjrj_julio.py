import sys, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
# -*- coding: utf-8 -*-
import json
import urllib.request
import os

clean_num = '00014922520168190046'
process_formatted = '0001492-25.2016.8.19.0046'
url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}
req_data = json.dumps({'query': {'match': {'numeroProcesso': clean_num}}}).encode('utf-8')
req = urllib.request.Request(url, data=req_data, headers=headers)

target_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_3\documentos_processo"
os.makedirs(target_dir, exist_ok=True)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        hits = res.get('hits', {}).get('hits', [])
        
        # Salvar JSON bruto completo
        raw_json_path = os.path.join(target_dir, "datajud_raw.json")
        with open(raw_json_path, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=2, ensure_ascii=False)
        print(f"Salvo JSON bruto em {raw_json_path}")
        
        md_lines = []
        md_lines.append(f"# PROCESSAMENTO DO PROCESSO: {process_formatted}")
        md_lines.append(f"**Tribunal:** TJRJ (Tribunal de Justiça do Estado do Rio de Janeiro)")
        md_lines.append(f"**Total de Instâncias/Instâncias Encontradas:** {len(hits)}\n")
        
        all_movs = []
        
        for idx, hit in enumerate(hits, start=1):
            src = hit['_source']
            classe = src.get('classe', {}).get('nome', 'N/I')
            orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
            dt_ajui = src.get('dataAjuizamento', 'N/I')
            assuntos = [a.get('nome') for a in src.get('assuntos', []) if a.get('nome')]
            
            md_lines.append(f"## Instância {idx}: {classe}")
            md_lines.append(f"- **Órgão Julgador:** {orgao}")
            md_lines.append(f"- **Data de Ajuizamento:** {dt_ajui}")
            md_lines.append(f"- **Assuntos:** {', '.join(assuntos) if assuntos else 'Não informado'}")
            
            movimentos = src.get('movimentos', [])
            md_lines.append(f"- **Quantidade de Movimentações:** {len(movimentos)}\n")
            md_lines.append("### Movimentações:")
            
            for m in movimentos:
                dt = m.get('dataHora', 'Sem data')
                nome = m.get('nome', 'Sem descrição')
                code = m.get('codigo', '')
                comps = m.get('complementosTabelados', [])
                comp_txt = ""
                if comps:
                    comp_txt = " | " + " - ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps])
                
                line_str = f"- **[{dt}]** {nome}{comp_txt} *(Código CNJ: {code})*"
                md_lines.append(line_str)
                all_movs.append((dt, nome, orgao, comp_txt))
            
            md_lines.append("\n" + "="*50 + "\n")
            
        md_path = os.path.join(target_dir, "movimentacoes_completas_datajud.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))
        print(f"Salvo Relatório de Movimentações em {md_path}")
        
        # Gerar resumo executivo
        resumo_lines = [
            f"# RESUMO DE ANDAMENTO PROCESSUAL - TJRJ",
            f"**Réu/Cliente:** Júlio Pereira Marcos",
            f"**Processo Nº:** {process_formatted}",
            f"**Origem:** TJRJ - Comarca de Rio Bonito / 3ª Câmara Criminal",
            f"**Crime/Assunto:** Tráfico de Drogas e Condutas Afins (Art. 33 da Lei 11.343/06)",
            f"\n## Síntese do Caso",
            f"Trata-se de processo antigo originado na Comarca de Rio Bonito (código de origem 0046), autuado em 2016.",
            f"O processo possui registros tanto na 1ª Instância quanto na 2ª Instância (3ª Câmara Criminal) em grau de Apelação Criminal.",
            f"\n## Últimas Movimentações Registradas",
        ]
        
        # Pegar as 10 movimentações mais recentes
        all_movs_sorted = sorted(all_movs, key=lambda x: x[0], reverse=True)
        for dt, nome, orgao, comp in all_movs_sorted[:10]:
            resumo_lines.append(f"- **{dt}** [{orgao}]: {nome}{comp}")
            
        resumo_path = os.path.join(target_dir, "resumo_processual.md")
        with open(resumo_path, "w", encoding="utf-8") as f:
            f.write("\n".join(resumo_lines))
        print(f"Salvo Resumo Processual em {resumo_path}")

except Exception as e:
    print("Erro durante extração:", e)
