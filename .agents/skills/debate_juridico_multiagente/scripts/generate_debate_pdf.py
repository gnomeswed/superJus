# -*- coding: utf-8 -*-
"""
SUPERJUS — GERADOR DE PDF DO DEBATE MULTIAGENTE JURÍDICO
Design institucional moderno com Playwright Chromium (sem erros de acentuação, 2 páginas executivas).
"""

import sys, os
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def generate_pdf(client_name: str = "Júlio Pereira Marcos"):
    client_dir = Path(f"c:/Projetos/superJus/Clientes/{client_name.replace(' ', '_')}")
    md_file = client_dir / "07_RELATORIOS_ESTRATEGICOS_E_ANALISES" / "Relatorio_Debate_Estrategico_Multiagente.md"
    pdf_file = client_dir / "07_RELATORIOS_ESTRATEGICOS_E_ANALISES" / "Relatorio_Debate_Estrategico_Multiagente.pdf"

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
    
    @page {{
        size: A4;
        margin: 14mm 14mm 14mm 14mm;
    }}
    
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}
    
    body {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1e293b;
        background-color: #ffffff;
        font-size: 8.8pt;
        line-height: 1.45;
    }}

    .header {{
        border-bottom: 2px solid #0f172a;
        padding-bottom: 8px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }}
    
    .logo-area h1 {{
        font-family: 'Cinzel', serif;
        font-size: 14pt;
        letter-spacing: 1.5px;
        color: #0f172a;
        font-weight: 700;
    }}
    
    .logo-area p {{
        font-size: 7.5pt;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #64748b;
        font-weight: 600;
    }}
    
    .badge {{
        background: #0f172a;
        color: #f8fafc;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 7.5pt;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .title-banner {{
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
        padding: 10px 14px;
        border-radius: 6px;
        margin-bottom: 12px;
    }}
    
    .title-banner h2 {{
        font-size: 11pt;
        font-weight: 700;
        margin-bottom: 4px;
        letter-spacing: 0.3px;
    }}
    
    .title-banner .meta {{
        display: flex;
        gap: 16px;
        font-size: 7.8pt;
        color: #cbd5e1;
    }}
    
    .persona-card {{
        border: 1px solid #e2e8f0;
        border-left: 4px solid #0f172a;
        border-radius: 4px;
        padding: 8px 10px;
        margin-bottom: 8px;
        background: #f8fafc;
    }}
    
    .persona-card.p1 {{ border-left-color: #dc2626; }}
    .persona-card.p2 {{ border-left-color: #2563eb; }}
    .persona-card.p3 {{ border-left-color: #059669; }}
    .persona-card.p4 {{ border-left-color: #d97706; }}
    
    .persona-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 4px;
    }}
    
    .persona-title {{
        font-weight: 700;
        font-size: 8.8pt;
        color: #0f172a;
    }}
    
    .persona-tag {{
        font-size: 7pt;
        font-weight: 600;
        padding: 2px 6px;
        border-radius: 3px;
        background: #e2e8f0;
        color: #334155;
    }}
    
    .persona-body {{
        font-size: 8.2pt;
        color: #334155;
        text-align: justify;
        line-height: 1.4;
    }}

    .consensus-box {{
        background: #f0fdf4;
        border: 1.5px solid #86efac;
        border-radius: 6px;
        padding: 10px 12px;
        margin-top: 10px;
    }}
    
    .consensus-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }}
    
    .consensus-header h3 {{
        color: #166534;
        font-size: 9.5pt;
        font-weight: 700;
    }}
    
    .consensus-prob {{
        background: #166534;
        color: #ffffff;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 7.5pt;
        font-weight: 700;
    }}

    .action-list {{
        list-style: none;
        padding: 0;
        margin-top: 4px;
    }}
    
    .action-list li {{
        position: relative;
        padding-left: 14px;
        font-size: 8pt;
        color: #14532d;
        margin-bottom: 3px;
        font-weight: 500;
    }}
    
    .action-list li::before {{
        content: "▶";
        position: absolute;
        left: 0;
        font-size: 6.5pt;
        color: #16a34a;
        top: 2px;
    }}
    
    .footer {{
        margin-top: 10px;
        border-top: 1px solid #e2e8f0;
        padding-top: 6px;
        display: flex;
        justify-content: space-between;
        font-size: 7pt;
        color: #94a3b8;
    }}
</style>
</head>
<body>

<div class="header">
    <div class="logo-area">
        <h1>SUPERJUS</h1>
        <p>Inteligência Jurídica Estratégica & Análise Multiagente</p>
    </div>
    <div class="badge">Mesa Redonda de Subagentes</div>
</div>

<div class="title-banner">
    <h2>PARECER DO COMITÊ JURÍDICO ESTRATÉGICO</h2>
    <div class="meta">
        <span><strong>Cliente:</strong> {client_name}</span>
        <span><strong>Caso STJ:</strong> HC 1.116.750/RJ (6ª Turma)</span>
        <span><strong>Data:</strong> 29/08/2026</span>
    </div>
</div>

<!-- PERSONA 1 -->
<div class="persona-card p1">
    <div class="persona-header">
        <span class="persona-title">🏛️ O MAGISTRADO SIMULADOR (MINISTRO CÉTICO)</span>
        <span class="persona-tag">Filtro de Admissibilidade & Barreiras</span>
    </div>
    <div class="persona-body">
        "O MPF alegou suposta fuga e periculosidade. Contudo, o paciente impetrou HC preventivo antes do cumprimento e o mandado não constava regularmente no BNMP. Além disso, a segregação cautelar ultrapassa <strong>90 dias sem realização da AIJ no feito desmembrado (Art. 400, CPP)</strong>. Se a defesa focar no <strong>excesso de prazo e na isonomia do Art. 580 do CPP</strong> com o corréu Matheus, a concessão da ordem tem alta viabilidade."
    </div>
</div>

<!-- PERSONA 2 -->
<div class="persona-card p2">
    <div class="persona-header">
        <span class="persona-title">⚡ O ESTRATEGISTA DE CORTES SUPERIORES (STJ / STF)</span>
        <span class="persona-tag">Tese de Soltura & Art. 580 CPP</span>
    </div>
    <div class="persona-body">
        "Nossa melhor janela no STJ reside no <strong>Art. 580 do CPP</strong>: o corréu Matheus obteve revogação da preventiva pela ausência de contemporaneidade e apreensão direta. Júlio encontra-se em situação idêntica (zero drogas apreendidas). Incidência expressa da jurisprudência consolidada no <strong>STJ HC 568.211/SP</strong> e votos do Min. Sebastião Reis Júnior e Min. Og Fernandes."
    </div>
</div>

<!-- PERSONA 3 -->
<div class="persona-card p3">
    <div class="persona-header">
        <span class="persona-title">🛡️ O AUDITOR DE NULIDADES & CADEIA DE CUSTÓDIA</span>
        <span class="persona-tag">Nulidades Processuais (Art. 564 CPP)</span>
    </div>
    <div class="persona-body">
        "Três nulidades absolutas mapeadas: <strong>1. Ausência de Laudo de Confronto Vocálico (STJ HC 512.278/SP)</strong> nas interceptações; <strong>2. Descaracterização do Art. 35</strong> com confissão do próprio Delegado Dr. Nelson Esquiba em juízo de que Júlio não exercia gerência nem vínculo permanente; <strong>3. Quebra de cadeia de custódia (Art. 158-A, CPP)</strong> das mídias digitais."
    </div>
</div>

<!-- PERSONA 4 -->
<div class="persona-card p4">
    <div class="persona-header">
        <span class="persona-title">📊 O ESPECIALISTA EM DOSIMETRIA & EXECUÇÃO</span>
        <span class="persona-tag">Homogeneidade Cautelar & Detração</span>
    </div>
    <div class="persona-body">
        "Com a absolvição do Art. 35 e a aplicação do <strong>Tráfico Privilegiado (Art. 33, § 4º - redução de 2/3)</strong>, a pena final é projetada em <strong>1 ano e 8 meses em REGIME ABERTO com substituição por PRD</strong>. Manter a prisão preventiva viola o Princípio da Homogeneidade, pois a cautelar tornou-se infinitamente mais severa que o provimento condenatório final."
    </div>
</div>

<!-- CONSENSO & BOLETA -->
<div class="consensus-box">
    <div class="consensus-header">
        <h3>📋 CONSENSO DA BANCA & BOLETA DE AÇÃO PROCESSUAL</h3>
        <span class="consensus-prob">Probabilidade de Êxito: 75% a 85%</span>
    </div>
    <p style="font-size: 8.2pt; color: #15803d; font-weight: 600; margin-bottom: 4px;">
        Veredito: OFENSIVA IMEDIATA EM DUAS FRENTES (STJ & 1ª INSTÂNCIA)
    </p>
    <ul class="action-list">
        <li><strong>Frente 1 (STJ - HC 1.116.750):</strong> Despacho presencial/virtual de Memoriais Executivos de 2 páginas na assessoria do Relator Min. Og Fernandes priorizando o Art. 580 do CPP e o excesso de prazo.</li>
        <li><strong>Frente 2 (1ª Vara de Búzios):</strong> Protocolo de pedido de relaxamento de prisão preventiva por excesso de prazo injustificado na instrução criminal (Art. 400 do CPP c/c Art. 5º, LXXVIII da CF).</li>
        <li><strong>Frente 3 (Precedente Vinculante):</strong> Juntada de certidão de soltura do corréu Matheus para preclusão lógica do debate acusatório.</li>
    </ul>
</div>

<div class="footer">
    <span>SuperJus Intelligence — Sistema de Comitê Multiagente Estratégico</span>
    <span>Documento de Circulação Interna & Planejamento da Banca</span>
</div>

</body>
</html>"""

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html_content)
        pdf_file.parent.mkdir(parents=True, exist_ok=True)
        page.pdf(
            path=str(pdf_file),
            format="A4",
            print_background=True,
            margin={"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"}
        )
        browser.close()

    print(f"PDF Executivo gerado com sucesso em:\n{pdf_file}")

if __name__ == "__main__":
    generate_pdf()
