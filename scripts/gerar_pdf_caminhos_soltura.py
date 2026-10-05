# -*- coding: utf-8 -*-
import asyncio
import os
import shutil
from playwright.async_api import async_playwright

html_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Plano Estratégico de Agilização da Soltura — Júlio Pereira Marcos</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

  @page {
    size: A4;
    margin: 14mm 14mm 16mm 14mm;
    @bottom-right {
      content: "Página " counter(page) " de " counter(pages);
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 8pt;
      color: #718096;
    }
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1a202c;
    background: #ffffff;
    font-size: 9.5pt;
    line-height: 1.55;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  /* Header Superior */
  .header-container {
    border-bottom: 2px solid #2b6cb0;
    padding-bottom: 10px;
    margin-bottom: 16px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }

  .brand-title {
    font-size: 14pt;
    font-weight: 800;
    color: #1a365d;
    letter-spacing: -0.5px;
    text-transform: uppercase;
  }

  .brand-subtitle {
    font-size: 8pt;
    color: #4a5568;
    font-weight: 600;
    margin-top: 2px;
  }

  .header-meta {
    text-align: right;
    font-size: 8pt;
    color: #4a5568;
  }

  .meta-tag {
    display: inline-block;
    background: #edf2f7;
    color: #2d3748;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 600;
    margin-top: 3px;
  }

  .meta-tag.urgent {
    background: #fed7d7;
    color: #9b2c2c;
  }

  /* Título Principal */
  .document-title-box {
    background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 100%);
    color: #ffffff;
    padding: 14px 18px;
    border-radius: 8px;
    margin-bottom: 16px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  }

  .document-title-box h1 {
    font-size: 13.5pt;
    font-weight: 700;
    margin-bottom: 4px;
  }

  .document-title-box p {
    font-size: 9pt;
    color: #e2e8f0;
    line-height: 1.4;
  }

  /* Introdução */
  .intro-text {
    font-size: 10pt;
    color: #2d3748;
    margin-bottom: 16px;
    line-height: 1.6;
    background: #f7fafc;
    border-left: 4px solid #3182ce;
    padding: 10px 14px;
    border-radius: 0 6px 6px 0;
  }

  /* Cards de Frente */
  .front-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 14px;
    page-break-inside: avoid;
  }

  .front-card.stj {
    border-left: 4px solid #dd6b20;
  }

  .front-card.tjrj {
    border-left: 4px solid #d69e2e;
  }

  .front-card.comarca {
    border-left: 4px solid #e53e3e;
  }

  .front-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    border-bottom: 1px solid #edf2f7;
    padding-bottom: 6px;
  }

  .front-header h2 {
    font-size: 11pt;
    font-weight: 700;
    color: #1a365d;
  }

  .front-desc {
    font-size: 9pt;
    color: #4a5568;
    margin-bottom: 10px;
    line-height: 1.45;
  }

  .action-list {
    list-style: none;
    padding-left: 0;
  }

  .action-item {
    margin-bottom: 8px;
    padding-left: 14px;
    position: relative;
    font-size: 9pt;
    color: #2d3748;
  }

  .action-item::before {
    content: "•";
    position: absolute;
    left: 2px;
    color: #2b6cb0;
    font-weight: bold;
  }

  .action-title {
    font-weight: 700;
    color: #2c5282;
  }

  .sub-bullet {
    margin-top: 4px;
    padding-left: 12px;
    font-size: 8.5pt;
    color: #4a5568;
    line-height: 1.45;
  }

  .quote-box {
    background: #fffaf0;
    border-left: 3px solid #dd6b20;
    padding: 6px 10px;
    margin: 4px 0 6px 0;
    font-style: italic;
    color: #7b341e;
    font-size: 8.5pt;
    border-radius: 0 4px 4px 0;
  }

  .badge-code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8pt;
    background: #edf2f7;
    color: #2b6cb0;
    padding: 1px 5px;
    border-radius: 3px;
    font-weight: 600;
  }

  /* Tabela de Plano de Ação */
  .table-section {
    margin-top: 14px;
    margin-bottom: 14px;
    page-break-inside: avoid;
  }

  .table-section-title {
    font-size: 10.5pt;
    font-weight: 700;
    color: #1a365d;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    border-radius: 6px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }

  th {
    background: #2b6cb0;
    color: #ffffff;
    font-weight: 700;
    padding: 7px 10px;
    text-align: left;
    text-transform: uppercase;
    font-size: 8pt;
    letter-spacing: 0.5px;
  }

  td {
    padding: 8px 10px;
    border-bottom: 1px solid #e2e8f0;
    vertical-align: top;
    color: #2d3748;
  }

  tr:nth-child(even) {
    background: #f7fafc;
  }

  tr:last-child td {
    border-bottom: 2px solid #cbd5e0;
  }

  .col-date {
    width: 25%;
    font-weight: 700;
    color: #1a365d;
  }

  .col-action {
    width: 45%;
    color: #2d3748;
  }

  .col-target {
    width: 30%;
    color: #2c5282;
    font-weight: 600;
  }

  /* Rodapé Final */
  .conclusion-box {
    background: #ebf8ff;
    border: 1px solid #bee3f8;
    border-radius: 6px;
    padding: 10px 14px;
    margin-top: 12px;
    font-size: 9pt;
    color: #2b6cb0;
    font-weight: 600;
    text-align: center;
    line-height: 1.45;
  }

  .signature-bar {
    margin-top: 16px;
    padding-top: 8px;
    border-top: 1px solid #e2e8f0;
    display: flex;
    justify-content: space-between;
    font-size: 7.5pt;
    color: #718096;
  }
</style>
</head>
<body>

  <!-- Topo Institucional -->
  <div class="header-container">
    <div>
      <div class="brand-title">SuperJus Intelligence</div>
      <div class="brand-subtitle">Núcleo de Inteligência Criminal & Estratégia em Tribunais Superiores</div>
    </div>
    <div class="header-meta">
      <div><strong>Cliente:</strong> Júlio Pereira Marcos</div>
      <div><strong>Ação Originária:</strong> <span class="badge-code">0023013-51.2021.8.19.0078</span></div>
      <div><span class="meta-tag urgent">Réu Preso: 116 Dias</span> <span class="meta-tag">Data: 04/09/2026</span></div>
    </div>
  </div>

  <!-- Box de Título -->
  <div class="document-title-box">
    <h1>PLANO TÁTICO DE ACELERAÇÃO PROCESSUAL</h1>
    <p>Caminhos práticos, imediatos e articulados para antecipação da soltura sem dependência do recesso forense</p>
  </div>

  <!-- Introdução -->
  <div class="intro-text">
    Para agilizar a soltura de <strong>Júlio Pereira Marcos</strong> e encurtar o tempo de espera, a estratégia mais eficaz no processo penal de alta performance é a <strong>ofensiva simultânea em 3 frentes (Triangulação Processual)</strong>.
  </div>

  <!-- FRENTE 1 -->
  <div class="front-card stj">
    <div class="front-header">
      <h2>🚀 1. No STJ (Brasília — O Caminho Mais Rápido de Soltura)</h2>
    </div>
    <div class="front-desc">
      O processo (<span class="badge-code">HC 1.116.750/RJ</span>) já está <strong>concluso dentro do gabinete</strong> do Relator, <strong>Ministro Og Fernandes</strong>. Para fazê-lo sair da fila comum e ser julgado imediatamente:
    </div>

    <ul class="action-list">
      <li class="action-item">
        <span class="action-title">A. Despacho Direto com a Assessoria do Ministro (Agendado para Terça-feira):</span>
        <div class="sub-bullet">• O advogado deve despachar (presencialmente em Brasília ou via Balcão Virtual) diretamente com o assessor responsável pela minuta de votos da 6ª Turma.</div>
        <div class="sub-bullet">• O foco do despacho verbal deve ser cirúrgico:</div>
        <div class="quote-box">
          "Ministro, temos um réu preso há 116 dias sem audiência de instrução, enquanto todos os outros 5 corréus estão soltos há 4 anos pelo mesmo motivo. É caso manifesto de aplicação do Art. 580 do CPP."
        </div>
      </li>

      <li class="action-item">
        <span class="action-title">B. Entrega de "Memoriais Executivos de 2 Páginas" (One-Pager):</span>
        <div class="sub-bullet">• Gabinetes de Tribunais Superiores não leem petições longas com urgência. A entrega de um memorial visual de apenas <strong>duas páginas</strong>, com tabela comparativa destacando a soltura dos corréus e os 116 dias de prisão sem AIJ, tem efeito catalisador imediato.</div>
      </li>

      <li class="action-item">
        <span class="action-title">C. Petição de "Fato Novo / Pedido de Apreciação Urgente de Liminar":</span>
        <div class="sub-bullet">• Protocolar nos autos eletrônicos do STJ uma petição sucinta informando o marco atualizado de <strong>116 dias de prisão ininterrupta sem designação da AIJ</strong>, juntando a certidão atualizada de Búzios. No sistema do STJ, petições de urgência sinalizam alerta na tela do chefe de gabinete.</div>
      </li>
    </ul>
  </div>

  <!-- FRENTE 2 -->
  <div class="front-card tjrj">
    <div class="front-header">
      <h2>⚡ 2. No TJRJ (Rio de Janeiro — Destravar o Novo HC)</h2>
    </div>
    <div class="front-desc">
      O novo HC impetrado no Rio é uma rota de fuga rápida, mas está preso no gargalo da distribuição eletrônica:
    </div>

    <ul class="action-list">
      <li class="action-item">
        <span class="action-title">A. Contato com a Divisão de Protocolo e Distribuição (DIPRO / Suporte do Novo Sistema):</span>
        <div class="sub-bullet">• Na segunda-feira de manhã, o advogado ou seu assistente deve acionar a central de atendimento/DIPRO do TJRJ para solicitar a <strong>distribuição manual e forçada</strong> da petição que travou no sistema novo.</div>
      </li>

      <li class="action-item">
        <span class="action-title">B. Pedido de Liminar em 48 Horas:</span>
        <div class="sub-bullet">• Assim que o sistema sortear a Câmara Criminal e o Desembargador Relator, o advogado deve ligar no mesmo instante para o gabinete do Desembargador no Rio solicitando a apreciação urgente da liminar. O TJRJ costuma apreciar liminares de réu preso em até 72 horas.</div>
      </li>
    </ul>
  </div>

  <!-- FRENTE 3 -->
  <div class="front-card comarca">
    <div class="front-header">
      <h2>🎯 3. Na 1ª Instância (1ª Vara de Búzios — Ação Penal 0023013-51.2021.8.19.0078)</h2>
    </div>
    <div class="front-desc">
      A comarca de origem não pode ficar inerte:
    </div>

    <ul class="action-list">
      <li class="action-item">
        <span class="action-title">A. Petição de Relaxamento de Prisão por Excesso de Prazo Consumado (Art. 5º, LXV, da CF):</span>
        <div class="sub-bullet">• Protocolar na 1ª Vara de Búzios um pedido direto de relaxamento, lembrando ao magistrado que a própria comarca reconheceu em 2022 o excesso de prazo do Estado e soltou os corréus, sendo ilegal manter Júlio preso há 116 dias sem AIJ.</div>
      </li>

      <li class="action-item">
        <span class="action-title">B. Requerimento Subsidiário de Tornozeleira Eletrônica (Art. 319 do CPP):</span>
        <div class="sub-bullet">• Muitos juízes hesitam em dar liberdade plena de imediato. Quando a defesa inclui o pedido subsidiário de <strong>prisão com monitoramento eletrônico (tornozeleira) ou comparecimento mensal em juízo</strong>, a barreira psicológica do julgador cai drasticamente e a soltura é viabilizada muito mais rápido.</div>
      </li>
    </ul>
  </div>

  <!-- TABELA -->
  <div class="table-section">
    <div class="table-section-title">📊 Resumo do Plano de Ação para a Próxima Semana</div>
    <table>
      <thead>
        <tr>
          <th>Dia / Momento</th>
          <th>Ação Estratégica</th>
          <th>Objetivo Concreto</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="col-date">Segunda-feira (07/09)</td>
          <td class="col-action">Acionar o suporte/distribuição do TJRJ (DIPRO)</td>
          <td class="col-target">Destravar a distribuição do novo HC e obter relator imediato</td>
        </tr>
        <tr>
          <td class="col-date">Terça-feira (08/09)</td>
          <td class="col-action">Despacho com a assessoria do Min. Og Fernandes (STJ)</td>
          <td class="col-target">Forçar a decisão monocrática de soltura em Brasília</td>
        </tr>
        <tr>
          <td class="col-date">Quarta-feira (09/09)</td>
          <td class="col-action">Protocolar memoriais curtos no STJ e pedido em Búzios</td>
          <td class="col-target">Fechar o cerco processual com oferta de medidas do Art. 319 (tornozeleira)</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- Caixa de Conclusão -->
  <div class="conclusion-box">
    "Adotando essa postura incisiva de despacho e memoriais enxutos, a decisão de soltura pode ser antecipada em semanas, sem depender do final do ano."
  </div>

  <!-- Barra de Assinatura -->
  <div class="signature-bar">
    <div>SuperJus Intelligence — Planejamento Tático e Defensivo | Pair Programming Jurídico</div>
    <div>Documento Estruturado para Alinhamento com a Banca de Advocacia</div>
  </div>

</body>
</html>
"""

async def generate_pdf():
    output_dirs = [
        r"c:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\07_RELATORIOS_ESTRATEGICOS_E_ANALISES",
        r"C:\Users\Administrator\Desktop",
        r"C:\Users\Administrator\.gemini\antigravity\brain\2187cd0c-a701-4a55-bea5-ce9e775530e8"
    ]
    for d in output_dirs:
        os.makedirs(d, exist_ok=True)
        
    main_pdf_path = os.path.join(output_dirs[0], "Plano_Estrategico_Agilizacao_Soltura_Julio.pdf")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_content(html_template, wait_until="networkidle")
        await page.pdf(
            path=main_pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "10mm", "bottom": "12mm", "left": "10mm", "right": "10mm"}
        )
        await browser.close()
        
    print(f"[OK] PDF gerado em: {main_pdf_path}")
    
    for dest_dir in output_dirs[1:]:
        dest_file = os.path.join(dest_dir, "Plano_Estrategico_Agilizacao_Soltura_Julio.pdf")
        shutil.copy2(main_pdf_path, dest_file)
        print(f"[OK] Copia sincronizada em: {dest_file}")

if __name__ == "__main__":
    asyncio.run(generate_pdf())
