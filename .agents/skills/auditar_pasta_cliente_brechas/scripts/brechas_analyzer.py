# -*- coding: utf-8 -*-
import os
import re
import sys
import json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

LEGAL_CHECKPOINTS = [
    {
        "categoria": "Nulidade de Reconhecimento Pessoal (Art. 226 do CPP)",
        "padroes": [r"reconhec", r"fotogr", r"álbum de fotos", r"apresentad", r"imagem"],
        "fundamentacao": "Art. 226 do CPP e Jurisprudência Vinculante do STJ (HC 598.886/SP e Tema 1.184/STJ). O reconhecimento por foto em sede policial sem observância das formalidades legais não fundamenta condenação.",
        "nivel_risco": "ALTO"
    },
    {
        "categoria": "Quebra da Cadeia de Custódia (Arts. 158-A a 158-F do CPP)",
        "padroes": [r"lacre", r"sem lacre", r"apreens", r"auto de apreensão", r"perícia", r"hash", r"espelhament", r"celular"],
        "fundamentacao": "Arts. 158-A a 158-F do CPP. Ausência de documentação do fluxo de posse, violação ou descarte da evidência digital/física acarreta a inadmissibilidade da prova.",
        "nivel_risco": "ALTO"
    },
    {
        "categoria": "Inviolabilidade de Domicílio e Busca sem Mandado",
        "padroes": [r"busca domiciliar", r"ingresso", r"residência", r"denúncia anônima", r"fundada suspeita", r"consentimento"],
        "fundamentacao": "Art. 5º, XI da CF/88 e Tema 280 do STF. A busca em domicílio sem mandado judicial exige justa causa prévia e documentada, sob pena de ilicitude de todas as provas derivadas.",
        "nivel_risco": "CRÍTICO"
    },
    {
        "categoria": "Nulidade na Prova Telemática / WhatsApp sem Perícia Integral",
        "padroes": [r"whatsapp", r"print", r"mídia", r"degravação", r"conversas", r"extração"],
        "fundamentacao": "Tema 1.062 do STF e Julgados da 6ª Turma do STJ. Prints de WhatsApp ou extração sem preservação da cadeia de custódia e integridade do arquivo gerador ensejam nulidade.",
        "nivel_risco": "ALTO"
    },
    {
        "categoria": "Vício de Isonomia / Extensão do Benefício aos Corréus (Art. 580 do CPP)",
        "padroes": [r"corréu", r"desmembramen", r"liberdade provisória", r"extensão", r"relaxam", r"foragid"],
        "fundamentacao": "Art. 580 do CPP. A decisão judicial que beneficia um dos corréus fundada em motivos que não sejam de caráter exclusivamente pessoal aproveita aos demais.",
        "nivel_risco": "CRÍTICO"
    },
    {
        "categoria": "Inépcia da Acusação por Associação Genericamente Imputada",
        "padroes": [r"associação", r"art\. 35", r"estabilidade", r"permanência", r"vínculo", r"concurso"],
        "fundamentacao": "Art. 41 do CPP e Art. 35 da Lei 11.343/06. Imputação de associação sem demonstração cabal do vínculo estável e permanente configura inépcia e atipicidade.",
        "nivel_risco": "MÉDIO"
    },
    {
        "categoria": "Aplicação Indevida da Agravante da Calamidade/Pandemia (Art. 61, II, 'j' CP)",
        "padroes": [r"covid", r"pandemia", r"calamidade", r"inciso ii", r"alínea j"],
        "fundamentacao": "Art. 61, II, 'j' do CP. A incidência da agravante exige comprovação concreta de que o agente se aproveitou do estado de calamidade para a prática do crime.",
        "nivel_risco": "MÉDIO"
    }
]

def scan_client_directory(client_dir):
    print(f"=== AUDITORIA DE BRECHAS E NULIDADES — CLIENTE: {os.path.basename(client_dir)} ===")
    
    findings = []
    analyzed_files = 0
    
    for root, dirs, files in os.walk(client_dir):
        for f in files:
            if f.endswith(('.txt', '.md', '.json', '.html')):
                fp = os.path.join(root, f)
                analyzed_files += 1
                try:
                    content = open(fp, "r", encoding="utf-8", errors="ignore").read()
                    lines = content.splitlines()
                    
                    for chk in LEGAL_CHECKPOINTS:
                        for pattern in chk["padroes"]:
                            matches = [ (idx+1, line.strip()) for idx, line in enumerate(lines) if re.search(pattern, line, re.IGNORECASE) ]
                            if matches:
                                findings.append({
                                    "arquivo": os.path.relpath(fp, client_dir),
                                    "categoria": chk["categoria"],
                                    "fundamentacao": chk["fundamentacao"],
                                    "nivel_risco": chk["nivel_risco"],
                                    "termo": pattern,
                                    "ocorrencias_qtd": len(matches),
                                    "exemplo": matches[0][1][:180]
                                })
                                break
                except Exception as e:
                    pass

    return analyzed_files, findings

def generate_report(client_dir, analyzed_files, findings):
    report_path = os.path.join(client_dir, "Relatorio_Diagnostico_Brechas_Nulidades.md")
    
    lines = []
    lines.append(f"# RELATÓRIO DE DIAGNÓSTICO DE BRECHAS E NULIDADES PROCESSUAIS")
    lines.append(f"**Cliente:** {os.path.basename(client_dir)}")
    lines.append(f"**Data da Auditoria:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    lines.append(f"**Total de Arquivos Analisados:** {analyzed_files}")
    lines.append(f"**Vulnerabilidades / Brechas Identificadas:** {len(findings)}\n")
    lines.append("--- \n")
    
    if not findings:
        lines.append("ℹ️ Nenhum vício ou ponto cético critico detectado nos padrões mapeados.")
    else:
        # Agrupar por Categoria
        categories = {}
        for f in findings:
            cat = f["categoria"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(f)
            
        for cat, items in categories.items():
            lines.append(f"## 🚨 {cat}")
            lines.append(f"**Nível de Relevância/Risco:** `{items[0]['nivel_risco']}`")
            lines.append(f"**Fundamentação Jurídica / Precedentes:**\n> {items[0]['fundamentacao']}\n")
            lines.append("### Arquivos Envolvidos e Evidências:")
            for item in items:
                lines.append(f"* **Arquivo:** `{item['arquivo']}`")
                lines.append(f"  * *Trecho Capturado:* \"{item['exemplo']}\"\n")
            lines.append("---\n")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
    print(f"SUCESSO: Relatório gerado com {len(findings)} teses/brechas mapeadas!")
    print(f"Salvo em: {report_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python brechas_analyzer.py <caminho_da_pasta_do_cliente>")
        sys.exit(1)
        
    target_dir = sys.argv[1]
    cnt, fnds = scan_client_directory(target_dir)
    generate_report(target_dir, cnt, fnds)
