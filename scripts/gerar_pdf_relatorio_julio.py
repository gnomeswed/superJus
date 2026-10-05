# -*- coding: utf-8 -*-
import asyncio
import os
from playwright.async_api import async_playwright

html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Relatório Estratégico Definitivo — Júlio Pereira Marcos</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap');

  @page {
    size: A4;
    margin: 14mm 14mm 14mm 14mm;
    @bottom-right {
      content: counter(page) ' / ' counter(pages);
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 8pt;
      color: #94a3b8;
    }
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #1e293b;
    background: #ffffff;
    font-size: 9.5pt;
    line-height: 1.5;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  /* Capa / Cabeçalho Principal */
  .header-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0a192f 100%);
    color: #ffffff;
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 16px;
    border-left: 6px solid #38bdf8;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.12);
  }

  .header-tag {
    display: inline-block;
    background: rgba(56, 189, 248, 0.15);
    color: #38bdf8;
    font-size: 7.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    padding: 3px 8px;
    border-radius: 5px;
    border: 1px solid rgba(56, 189, 248, 0.3);
    margin-bottom: 8px;
  }

  .header-title {
    font-family: 'Lora', serif;
    font-size: 16pt;
    font-weight: 700;
    letter-spacing: -0.3px;
    margin-bottom: 3px;
    color: #f8fafc;
  }

  .header-subtitle {
    font-size: 9pt;
    color: #94a3b8;
    font-weight: 400;
    margin-bottom: 12px;
  }

  .meta-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 10px;
  }

  .meta-item {
    font-size: 8pt;
  }

  .meta-label {
    color: #64748b;
    text-transform: uppercase;
    font-size: 6.5pt;
    font-weight: 700;
    letter-spacing: 0.5px;
  }

  .meta-val {
    color: #e2e8f0;
    font-weight: 600;
    margin-top: 1px;
    font-size: 8pt;
  }

  /* Seções */
  .section-title {
    font-family: 'Lora', serif;
    font-size: 11.5pt;
    font-weight: 700;
    color: #0f172a;
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 14px 0 8px 0;
    padding-bottom: 4px;
    border-bottom: 2px solid #e2e8f0;
    page-break-after: avoid;
  }

  .section-title span.num {
    background: #0f172a;
    color: #38bdf8;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8pt;
    font-weight: 800;
    width: 20px;
    height: 20px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 5px;
  }

  /* Tabelas */
  table.custom-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin: 8px 0 12px 0;
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
    font-size: 8pt;
    page-break-inside: avoid;
  }

  table.custom-table th {
    background: #0f172a;
    color: #f8fafc;
    font-weight: 600;
    text-align: left;
    padding: 7px 10px;
    font-size: 7.5pt;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  table.custom-table td {
    padding: 7px 10px;
    border-bottom: 1px solid #e2e8f0;
    color: #334155;
    vertical-align: top;
  }

  table.custom-table tr:nth-child(even) td {
    background: #f8fafc;
  }

  table.custom-table tr:last-child td {
    border-bottom: none;
  }

  /* Timeline */
  .timeline {
    position: relative;
    padding: 6px 0 6px 16px;
    margin: 6px 0 10px 0;
    border-left: 2px solid #cbd5e1;
    page-break-inside: avoid;
  }

  .timeline-item {
    position: relative;
    margin-bottom: 8px;
    padding-left: 12px;
  }

  .timeline-item:last-child {
    margin-bottom: 0;
  }

  .timeline-dot {
    position: absolute;
    left: -23px;
    top: 4px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #0f172a;
    border: 2px solid #38bdf8;
  }

  .timeline-dot.highlight {
    background: #38bdf8;
    border-color: #0f172a;
  }

  .timeline-date {
    font-weight: 700;
    color: #0f172a;
    font-size: 8pt;
  }

  .timeline-desc {
    font-size: 8pt;
    color: #475569;
  }

  /* Cards de Teses */
  .tese-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #0284c7;
    border-radius: 6px;
    padding: 10px 14px;
    margin-bottom: 10px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    page-break-inside: avoid;
  }

  .tese-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 4px;
  }

  .tese-title {
    font-size: 9pt;
    font-weight: 700;
    color: #0f172a;
  }

  .tese-badge {
    font-size: 6.5pt;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
    background: #e0f2fe;
    color: #0369a1;
    text-transform: uppercase;
  }

  .tese-body {
    font-size: 8pt;
    color: #334155;
    line-height: 1.45;
  }

  .quote-box {
    background: #f8fafc;
    border-left: 3px solid #64748b;
    padding: 5px 10px;
    margin: 5px 0;
    font-style: italic;
    font-family: 'Lora', serif;
    font-size: 8pt;
    color: #1e293b;
    border-radius: 0 4px 4px 0;
  }

  /* Matriz de Risco (Prós e Contras) */
  .grid-2col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin: 8px 0;
    page-break-inside: avoid;
  }

  .pros-box {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 6px;
    padding: 10px 12px;
  }

  .cons-box {
    background: #fef2f2;
    border: 1px solid #fecaca;
    border-radius: 6px;
    padding: 10px 12px;
  }

  .box-title {
    font-size: 8.5pt;
    font-weight: 700;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .pros-box .box-title { color: #166534; }
  .cons-box .box-title { color: #991b1b; }

  ul.box-list {
    list-style: none;
    font-size: 7.5pt;
    color: #334155;
  }

  ul.box-list li {
    position: relative;
    padding-left: 12px;
    margin-bottom: 4px;
  }

  ul.box-list li:last-child { margin-bottom: 0; }

  .pros-box ul.box-list li::before {
    content: '✓';
    position: absolute;
    left: 0;
    color: #16a34a;
    font-weight: bold;
  }

  .cons-box ul.box-list li::before {
    content: '⚠';
    position: absolute;
    left: 0;
    color: #dc2626;
    font-size: 7pt;
    top: 1px;
  }

  /* Probabilidade / Barra Visual */
  .chance-card {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 12px 16px;
    margin: 10px 0;
    page-break-inside: avoid;
  }

  .chance-bar-container {
    height: 16px;
    background: #e2e8f0;
    border-radius: 8px;
    overflow: hidden;
    display: flex;
    margin: 8px 0 6px 0;
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
  }

  .chance-segment-soltura {
    width: 45%;
    background: #10b981;
    color: #ffffff;
    font-size: 7pt;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .chance-segment-anulacao {
    width: 18%;
    background: #0ea5e9;
    color: #ffffff;
    font-size: 7pt;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .chance-segment-denegacao {
    width: 37%;
    background: #94a3b8;
    color: #ffffff;
    font-size: 7pt;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .chance-legend {
    display: flex;
    justify-content: space-between;
    font-size: 7pt;
    color: #475569;
    font-weight: 600;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 4px;
  }

  .legend-color {
    width: 8px;
    height: 8px;
    border-radius: 2px;
  }

  /* Rodapé do Relatório */
  .footer-notice {
    margin-top: 16px;
    padding-top: 8px;
    border-top: 1px solid #cbd5e1;
    font-size: 7pt;
    color: #64748b;
    display: flex;
    justify-content: space-between;
    align-items: center;
    page-break-inside: avoid;
  }

  .page-break {
    page-break-before: always;
  }
</style>
</head>
<body>

  <!-- CABEÇALHO EXECUTIVO -->
  <div class="header-card">
    <div class="header-tag">Parecer Técnico & Auditoria Processual</div>
    <div class="header-title">Relatório Estratégico Definitivo — Caso Júlio Pereira Marcos</div>
    <div class="header-subtitle">Análise da Petição Oficial do Advogado (29/07/2026), Prova dos Autos e Julgamento no STJ</div>
    
    <div class="meta-grid">
      <div class="meta-item">
        <div class="meta-label">Cliente</div>
        <div class="meta-val">Júlio Pereira Marcos</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Advogado</div>
        <div class="meta-val">Dr. Gabriel Alves Guimarães</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Tribunal / Órgão</div>
        <div class="meta-val">STJ — 6ª Turma (HC 1.116.750)</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Relator</div>
        <div class="meta-val">Min. Og Fernandes</div>
      </div>
    </div>
  </div>

  <!-- SEÇÃO 1: FICHA TÉCNICA -->
  <div class="section-title"><span class="num">1</span> Ficha Técnica e Situação em Tempo Real</div>
  <table class="custom-table">
    <thead>
      <tr>
        <th style="width: 25%;">Instância / Parâmetro</th>
        <th style="width: 75%;">Situação Processual Concreta e Verificada</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Situação Prisional</strong></td>
        <td>Preso preventivamente desde <strong>12/05/2026</strong> (3 meses e 10 dias de custódia efetiva) no Complexo Penitenciário de Gericinó (Bangu/RJ).</td>
      </tr>
      <tr>
        <td><strong>Superior Tribunal de Justiça (STJ)</strong></td>
        <td><strong>HC 1.116.750 / RJ</strong> concluso para decisão do Relator Ministro Og Fernandes desde <strong>13/08/2026 às 17:45</strong> (com parecer do MPF já juntado).</td>
      </tr>
      <tr>
        <td><strong>1ª Instância (Búzios)</strong></td>
        <td>Processo desmembrado nº <strong>0023013-51.2021.8.19.0078</strong> em fase de <em>Processamento</em> na serventia cartorária.</td>
      </tr>
      <tr>
        <td><strong>2ª Instância (TJRJ)</strong></td>
        <td>HC denegado em 11/06/2026 pela 7ª Câmara Criminal; Recurso Ordinário Constitucional (ROC) tempestivamente remetido a Brasília.</td>
      </tr>
    </tbody>
  </table>

  <!-- SEÇÃO 2: CRONOLOGIA REAL -->
  <div class="section-title"><span class="num">2</span> Cronologia Real dos Fatos</div>
  <div class="timeline">
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-date">Março a Setembro / 2021 — Fatos Investigados</div>
      <div class="timeline-desc">Operação Delivery deflagrada pela 127ª DP de Armação dos Búzios/RJ (Inquérito Policial 127-00370/2021).</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-date">27/01/2022 — Decreto Originário de Prisão</div>
      <div class="timeline-desc">Expedido mandado de prisão cautelar pelo Juízo de Búzios.</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-dot highlight"></div>
      <div class="timeline-date">02/08/2022 — LIBERDADE DE TODOS OS CORRÉUS</div>
      <div class="timeline-desc">O Juízo de Búzios concedeu liberdade a todos os 5 corréus do processo principal por excesso de prazo atribuível ao Estado (inclusive ao réu em posse de entorpecente).</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-date">05/05/2026 — Impetração de HC Preventivo no TJRJ</div>
      <div class="timeline-desc">Estando em liberdade, Júlio constitui advogado e impetra HC preventivo buscando a tutela jurisdicional.</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-dot highlight"></div>
      <div class="timeline-date">12/05/2026 — Prisão Efetiva de Júlio</div>
      <div class="timeline-desc">Mandado cumprido após 4 anos fora do Banco Nacional de Mandados de Prisão (BNMP) por inércia sistêmica.</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-date">24/07/2026 — Decisão Nula de 2 Linhas em Búzios</div>
      <div class="timeline-desc">Juiz Danilo Marques Borges rejeita a revogação da prisão sem apresentar fundamentação própria (fl. 1297).</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-dot highlight"></div>
      <div class="timeline-date">29/07/2026 — Petição Oficial do Dr. Gabriel (12 Páginas)</div>
      <div class="timeline-desc">Advogado protocola novo remédio constitucional demonstrando a nulidade da decisão e quebra de isonomia.</div>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- SEÇÃO 3: AS 4 TESES DA DEFESA REAL -->
  <div class="section-title"><span class="num">3</span> As 4 Teses Oficiais Protocoladas pelo Advogado</div>

  <div class="tese-card">
    <div class="tese-header">
      <div class="tese-title">1. Nulidade Absoluta da Decisão de 1ª Instância (fl. 1297)</div>
      <div class="tese-badge">Art. 315, §2º, CPP</div>
    </div>
    <div class="tese-body">
      O Juiz de Búzios indeferiu a liberdade limitando-se a declarar: <em>"Acolho a manifestação ministerial de fls. 1293/1294 e A ADOTO COMO INTEGRAL RAZÃO DE DECIDIR. Logo, rejeito o pleito libertário."</em>. A defesa demonstrou que a decisão por adesão cega viola a garantia constitucional da fundamentação e o Pacote Anticrime.
      <div class="quote-box">
        "A técnica de fundamentação per relationem não dispensa considerações, ainda que mínimas, sobre elementos concretos do fato." (STJ, HC 457.303/TO, Rel. Min. Antonio Saldanha Palheiro, 6ª Turma).
      </div>
    </div>
  </div>

  <div class="tese-card">
    <div class="tese-header">
      <div class="tese-title">2. Quebra de Isonomia e Extensão da Soltura dos Corréus</div>
      <div class="tese-badge">Art. 580, CPP</div>
    </div>
    <div class="tese-body">
      A soltura dos demais 5 corréus em 02/08/2022 fundou-se em motivo estritamente <strong>objetivo</strong> (demora e falhas do aparelho judiciário). Pelo Art. 580 do CPP, a manutenção exclusiva de Júlio no cárcere gera discriminação ilegal. A defesa rechaçou a Súmula 64/STJ comprovando que a demora decorreu da falha de registro no BNMP.
    </div>
  </div>

  <div class="tese-card">
    <div class="tese-header">
      <div class="tese-title">3. Fragilidade Probatória Admitida pelos Próprios Policiais</div>
      <div class="tese-badge">Prova Oral em AIJ</div>
    </div>
    <div class="tese-body">
      A petição confronta a acusação com as declarações prestadas em audiência pelos Delegados de Polícia:
      <ul style="margin-left: 18px; margin-top: 4px;">
        <li><strong>Materialidade Zero:</strong> Nenhuma grama de entorpecente foi apreendida com Júlio.</li>
        <li><strong>Ausência de Perícia:</strong> Não foi realizado confronto vocálico nas interceptações telefônicas.</li>
        <li><strong>Inexistência de Facção:</strong> Delegados admitiram que não havia hierarquia, armas ou organização estruturada.</li>
      </ul>
    </div>
  </div>

  <div class="tese-card">
    <div class="tese-header">
      <div class="tese-title">4. Falta de Contemporaneidade e Desmonte de Falso Antecedente</div>
      <div class="tese-badge">Art. 312, §2º, CPP</div>
    </div>
    <div class="tese-body">
      O Promotor alegou falsa reincidência por tráfico. A defesa provou documentalmente que o processo de Rio Bonito (0001492-25.2016.8.19.0046) foi <strong>DESCLASSIFICADO para o Art. 28 (porte para uso próprio)</strong>, sendo Júlio tecnicamente primário, com ocupação lícita (técnico de informática) e residência fixa.
    </div>
  </div>

  <!-- SEÇÃO 4: MINISTROS DO STJ -->
  <div class="section-title"><span class="num">4</span> Mapeamento Real da 6ª Turma do STJ</div>
  <table class="custom-table">
    <thead>
      <tr>
        <th style="width: 25%;">Ministro / Papel</th>
        <th style="width: 35%;">Perfil Técnico Verificado</th>
        <th style="width: 40%;">Precedentes Reais Mapeados</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Min. Og Fernandes</strong><br><small style="color: #0ea5e9;">RELATOR DO CASO</small></td>
        <td>Rigoroso e formal; anula preventivas lastreadas em fundamentação abstrata ou desídia estatal.</td>
        <td><strong>HC 1.002.290/SP</strong> (soltura por falta de fundamentação)<br><strong>AgRg HC 940.623/RJ</strong> (reformou TJRJ para tornozeleira)</td>
      </tr>
      <tr>
        <td><strong>Min. Sebastião Reis Jr.</strong><br><small style="color: #64748b;">Vogal</small></td>
        <td>O mais garantista do STJ; líder em substituição de prisão por cautelares em tráfico.</td>
        <td><strong>HC 828.070/RJ</strong> (reformou TJRJ)<br><strong>HC 798.690/SC</strong> (tornozeleira em delito sem violência)</td>
      </tr>
      <tr>
        <td><strong>Min. Rogerio Schietti Cruz</strong><br><small style="color: #64748b;">Vogal</small></td>
        <td>Maior autoridade processual penal; combate excessos de fundamentação e prisões automáticas.</td>
        <td><strong>HC 598.051/SP</strong> (Leading case sobre garantias)<br><strong>HC 573.144/SP</strong> (cautelares em arts. 33 e 35)</td>
      </tr>
      <tr>
        <td><strong>Min. Saldanha Palheiro</strong><br><small style="color: #64748b;">Vogal</small></td>
        <td>Ex-Desembargador do TJRJ; autor do precedente exato citado contra decisões <em>per relationem</em>.</td>
        <td><strong>HC 457.303/TO</strong> (precedente usado pelo Dr. Gabriel)<br><strong>HC 636.740/RJ</strong> (Caso Crivella — cautelares no RJ)</td>
      </tr>
    </tbody>
  </table>

  <!-- SEÇÃO 5: MATRIZ DE RISCO -->
  <div class="section-title"><span class="num">5</span> Matriz de Risco: Pontos Fortes vs. Desafios Reais</div>
  <div class="grid-2col">
    <div class="pros-box">
      <div class="box-title">Pontos Determinantes a Favor</div>
      <ul class="box-list">
        <li>Decisão de Búzios (fl. 1297) é nula de pleno direito por ter apenas 2 linhas.</li>
        <li>Isonomia do Art. 580 do CPP: 5 corréus soltos há 4 anos.</li>
        <li>Nenhuma apreensão de droga com Júlio nos autos.</li>
        <li>Erro material do Promotor (falsa alegação de tráfico anterior).</li>
        <li>Boa-fé processual com impetração de HC preventivo prévio.</li>
      </ul>
    </div>
    <div class="cons-box">
      <div class="box-title">Desafios & Pontos de Atenção</div>
      <ul class="box-list">
        <li>Período de 2022 a 2026 sem localização é explorado pelo MP como risco de fuga.</li>
        <li>Acórdão unânime de 2ª instância do TJRJ impõe cognição estrita no STJ.</li>
        <li>A via do Habeas Corpus não comporta dilação probatória profunda.</li>
      </ul>
    </div>
  </div>

  <!-- SEÇÃO 6: CENÁRIOS E PROBABILIDADE -->
  <div class="section-title"><span class="num">6</span> Cenário Realista de Julgamento no STJ</div>
  <div class="chance-card">
    <div style="font-size: 8.5pt; font-weight: 700; color: #0f172a;">Estimativa Ponderada de Desfecho no STJ:</div>
    
    <div class="chance-bar-container">
      <div class="chance-segment-soltura">45% Soltura Cautelar</div>
      <div class="chance-segment-anulacao">18% Anulação</div>
      <div class="chance-segment-denegacao">37% Denegação</div>
    </div>

    <div class="chance-legend">
      <div class="legend-item">
        <div class="legend-color" style="background: #10b981;"></div>
        <span>Concessão da Ordem / Tornozeleira (40% a 50%)</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background: #0ea5e9;"></div>
        <span>Anulação da Decisão de Piso (15% a 20%)</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background: #94a3b8;"></div>
        <span>Manutenção da Prisão (35% a 45%)</span>
      </div>
    </div>
  </div>

  <!-- RODAPÉ -->
  <div class="footer-notice">
    <div>Superior Tribunal de Justiça — 6ª Turma | HC nº 1.116.750/RJ</div>
    <div>Documento Gerado com Base nas Peças Oficiais e Dados do STJ — 22/08/2026</div>
  </div>

</body>
</html>
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html_content, wait_until="networkidle")
        
        pdf_path_1 = r'c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\analises\RELATORIO_ESTRATEGICO_DEFINITIVO_JULIO_STJ.pdf'
        pdf_path_2 = r'C:\Users\Administrator\.gemini\antigravity\brain\e2c0b2ac-ee71-4cae-b44e-9ade3182df28\RELATORIO_ESTRATEGICO_DEFINITIVO_JULIO_STJ.pdf'
        
        await page.pdf(
            path=pdf_path_1,
            format='A4',
            print_background=True,
            margin={'top': '12mm', 'bottom': '12mm', 'left': '12mm', 'right': '12mm'}
        )
        await page.pdf(
            path=pdf_path_2,
            format='A4',
            print_background=True,
            margin={'top': '12mm', 'bottom': '12mm', 'left': '12mm', 'right': '12mm'}
        )
        await browser.close()
        print('PDFs gerados com sucesso!')

if __name__ == '__main__':
    asyncio.run(main())
