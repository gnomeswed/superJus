# -*- coding: utf-8 -*-
"""
SUPERJUS — GERADOR DE PDF DO DEBATE MULTIAGENTE JURÍDICO REALISTA (LUCAS MOTOBOY)
Design institucional moderno com Playwright Chromium (sem erros de acentuação, 2 páginas executivas).
"""

import sys, os
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def generate_pdf_lucas():
    client_dir = Path("c:/Projetos/superJus/Clientes/Lucas_Freitas")
    pdf_file = client_dir / "04_Analises_e_Estrategias" / "Relatorio_Debate_Estrategico_Multiagente_Lucas.pdf"

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
    
    @page {{
        size: A4;
        margin: 10mm 12mm 10mm 12mm;
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
        font-size: 8.2pt;
        line-height: 1.38;
    }}

    .header {{
        border-bottom: 2px solid #0f172a;
        padding-bottom: 6px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }}
    
    .logo-area h1 {{
        font-family: 'Cinzel', serif;
        font-size: 13pt;
        letter-spacing: 1.5px;
        color: #0f172a;
        font-weight: 700;
    }}
    
    .logo-area p {{
        font-size: 6.8pt;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #64748b;
        font-weight: 600;
    }}
    
    .badge {{
        background: #b91c1c;
        color: #f8fafc;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 6.8pt;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .title-banner {{
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
        padding: 8px 12px;
        border-radius: 5px;
        margin-bottom: 8px;
    }}
    
    .title-banner h2 {{
        font-size: 10pt;
        font-weight: 700;
        margin-bottom: 2px;
        letter-spacing: 0.3px;
    }}
    
    .title-banner .meta {{
        display: flex;
        gap: 14px;
        font-size: 7.2pt;
        color: #cbd5e1;
    }}
    
    .persona-card {{
        border: 1px solid #e2e8f0;
        border-left: 4px solid #0f172a;
        border-radius: 4px;
        padding: 6px 9px;
        margin-bottom: 6px;
        background: #f8fafc;
    }}
    
    .persona-card.p1 {{ border-left-color: #dc2626; }}
    .persona-card.p2 {{ border-left-color: #991b1b; background: #fff5f5; }}
    .persona-card.p3 {{ border-left-color: #2563eb; }}
    .persona-card.p4 {{ border-left-color: #d97706; }}
    
    .persona-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2px;
    }}
    
    .persona-title {{
        font-weight: 700;
        font-size: 8.2pt;
        color: #0f172a;
    }}
    
    .persona-tag {{
        font-size: 6.5pt;
        font-weight: 600;
        padding: 2px 5px;
        border-radius: 3px;
        background: #e2e8f0;
        color: #334155;
    }}
    
    .persona-body {{
        font-size: 7.8pt;
        color: #334155;
        text-align: justify;
        line-height: 1.35;
    }}

    .grid-2 {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin-top: 6px;
    }}

    .box-bad {{
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 5px;
        padding: 7px 9px;
    }}
    
    .box-bad h4 {{
        color: #991b1b;
        font-size: 7.8pt;
        font-weight: 700;
        margin-bottom: 4px;
    }}

    .box-good {{
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 5px;
        padding: 7px 9px;
    }}
    
    .box-good h4 {{
        color: #166534;
        font-size: 7.8pt;
        font-weight: 700;
        margin-bottom: 4px;
    }}

    .family-box {{
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-radius: 5px;
        padding: 7px 9px;
        margin-top: 6px;
    }}

    .family-box h4 {{
        color: #92400e;
        font-size: 7.8pt;
        font-weight: 700;
        margin-bottom: 3px;
    }}

    .custom-list {{
        list-style: none;
        padding: 0;
    }}
    
    .custom-list li {{
        position: relative;
        padding-left: 12px;
        font-size: 7.3pt;
        margin-bottom: 2px;
        line-height: 1.3;
    }}
    
    .custom-list.bad li {{ color: #7f1d1d; }}
    .custom-list.bad li::before {{ content: "✕"; position: absolute; left: 0; color: #dc2626; font-size: 6.5pt; top: 1px; }}
    
    .custom-list.good li {{ color: #14532d; }}
    .custom-list.good li::before {{ content: "✓"; position: absolute; left: 0; color: #16a34a; font-weight: bold; font-size: 7pt; top: 0; }}

    .custom-list.fam li {{ color: #78350f; }}
    .custom-list.fam li::before {{ content: "•"; position: absolute; left: 0; color: #d97706; font-weight: bold; font-size: 9pt; top: -2px; }}
    
    .footer {{
        margin-top: 6px;
        border-top: 1px solid #e2e8f0;
        padding-top: 4px;
        display: flex;
        justify-content: space-between;
        font-size: 6.5pt;
        color: #94a3b8;
    }}
</style>
</head>
<body>

<div class="header">
    <div class="logo-area">
        <h1>SUPERJUS</h1>
        <p>Inteligência Jurídica Estratégica & Análise Realista de Casos</p>
    </div>
    <div class="badge">Protocolo Anti-Bajulação</div>
</div>

<div class="title-banner">
    <h2>DIAGNÓSTICO REALISTA — LUCAS DE SOUZA FREITAS ("MOTOBOY LUCAS")</h2>
    <div class="meta">
        <span><strong>Processo:</strong> 0011857-95.2024.8.19.0002</span>
        <span><strong>TJRJ:</strong> 2ª Câmara Criminal (Rel. Des. Flávio Itabaiana)</span>
        <span><strong>Pena da Sentença:</strong> 22 anos</span>
    </div>
</div>

<!-- PERSONA 1 -->
<div class="persona-card p1">
    <div class="persona-header">
        <span class="persona-title">⚖️ O MAGISTRADO INQUISIDOR (RELATOR CÉTICO - 2ª CÂMARA TJRJ)</span>
        <span class="persona-tag">Barreiras & Jurisprudência Defensiva</span>
    </div>
    <div class="persona-body">
        "Sejamos frios: a 2ª Câmara do TJRJ é rigorosamente punitivista e <strong>NÃO anulará o Júri de homicídio qualificado confesso</strong> por alegação de 'prova contrária' (Art. 593, III, 'd'). A soberania dos jurados prevalecerá. A <strong>ÚNICA</strong> brecha jurídica real é a <strong>DOSIMETRIA (Art. 593, III, 'c')</strong>: a Juíza de Niterói exorbitou na pena-base (+9 anos) e ignorou a súmula do STJ sobre confissão. Fora isso, o réu continuará condenado e preso em regime fechado."
    </div>
</div>

<!-- PERSONA 2 -->
<div class="persona-card p2">
    <div class="persona-header">
        <span class="persona-title">⚔️ O PROMOTOR ACUSADOR (O ADVOGADO DO DIABO)</span>
        <span class="persona-tag">Força Probatória da Acusação</span>
    </div>
    <div class="persona-body">
        "O crime chocou a sociedade: taxista atraído para emboscada, executado a tiros e ocultado. Lucas confessou e possui antecedentes. O Ministério Público sustentará a periculosidade social extrema e o parecer da Procuradoria de Justiça (com vista desde 13/08) será <strong>PELO DESPROVIMENTO TOTAL DA APELAÇÃO</strong>. A defesa não pode iludir o cliente: ele matou e confessou."
    </div>
</div>

<!-- PERSONA 3 -->
<div class="persona-card p3">
    <div class="persona-header">
        <span class="persona-title">🛡️ O ESTRATEGISTA PRAGMÁTICO DE CORTES SUPERIORES</span>
        <span class="persona-tag">Foco na Única Janela Real</span>
    </div>
    <div class="persona-body">
        "Chega de ilusões: brigar para anular o Júri é queimar cartucho e gerar falsas esperanças. Nosso alvo é 100% técnico na dosimetria: <strong>1. Tema Repetitivo 585 e Súmula 545 do STJ</strong> (compensação integral obrigatória entre confissão e reincidência); <strong>2. Fração de 1/6 na Pena-Base</strong>. O objetivo viável e real é reduzir a pena de 22 anos para <strong>17 a 19 anos</strong>."
    </div>
</div>

<!-- PERSONA 4 -->
<div class="persona-card p4">
    <div class="persona-header">
        <span class="persona-title">📊 O AUDITOR REALISTA DE EXECUÇÃO PENAL (A DURA REALIDADE DA CADEIA)</span>
        <span class="persona-tag">Cálculo Factual da VEP (Pacote Anticrime)</span>
    </div>
    <div class="persona-body">
        "Crime Hediondo com Resultado Morte exige <strong>50% a 70% de cumprimento de pena</strong> para progressão. Com 22 anos, ele cumpriria de 11 a 15 anos em regime fechado. Reduzindo para 18 anos, cumpre de 9 a 12 anos. <strong>A DURA VERDADE:</strong> A vitória na Apelação não soltará Lucas amanhã, mas evitará que ele passe a vida inteira trancado."
    </div>
</div>

<!-- MATRIZ DE REALIDADE -->
<div class="grid-2">
    <div class="box-bad">
        <h4>❌ O QUE NÃO VAI FUNCIONAR (FALSAS ESPERANÇAS)</h4>
        <ul class="custom-list bad">
            <li>Anular o veredito do Júri por prova contrária (Soberania dos jurados).</li>
            <li>Prometer liberdade provisória ou HC de soltura imediata.</li>
            <li>Tentar desclassificar o homicídio em sede de apelação.</li>
        </ul>
    </div>
    <div class="box-good">
        <h4>🎯 A ÚNICA JANELA TÉCNICA REAL (PROBABILIDADE 45% A 55%)</h4>
        <ul class="custom-list good">
            <li>Compensação Confissão x Reincidência (Tema 585 STJ).</li>
            <li>Redução da Pena-Base para a fração de 1/6 do STJ.</li>
            <li>Redução Factual da Pena de 22 anos para 17-19 anos (-3 a -5 anos).</li>
        </ul>
    </div>
</div>

<div class="family-box">
    <h4>🗣️ GUIA DE ALINHAMENTO COM A FAMÍLIA (COMO DIZER A VERDADE COM ÉTICA)</h4>
    <ul class="custom-list fam">
        <li><strong>Sem promessas mágicas:</strong> Deixar claro que o crime é hediondo e não há hipótese de soltura imediata.</li>
        <li><strong>Foco na vitória possível:</strong> Explicar que cortar 3 a 5 anos de pena é a maior vitória técnica possível, permitindo saída muito mais cedo no semiaberto.</li>
        <li><strong>Próximo passo real:</strong> Despacho de memoriais com o Des. Flávio Itabaiana após retorno do parecer do MP.</li>
    </ul>
</div>

<div class="footer">
    <span>SuperJus Intelligence — Análise Estratégica Realista & Anti-Bajulação</span>
    <span>Documento de Circulação Interna e Alinhamento Estratégico</span>
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
            margin={"top": "8mm", "bottom": "8mm", "left": "8mm", "right": "8mm"}
        )
        browser.close()

    print(f"PDF Executivo Realista gerado com sucesso em:\n{pdf_file}")

if __name__ == "__main__":
    generate_pdf_lucas()
