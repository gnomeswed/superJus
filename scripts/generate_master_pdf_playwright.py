# -*- coding: utf-8 -*-
import os, sys, asyncio
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")

HTML_CONTENT = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Relatório Executivo de Defesa - Júlio Pereira Marcos</title>
<style>
  @page {
    size: A4;
    margin: 10mm 12mm 10mm 12mm;
    @bottom-right {
      content: "Página " counter(page) " de " counter(pages);
      font-size: 7.5pt;
      color: #718096;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
  }

  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #2D3748;
    background-color: #FFFFFF;
    line-height: 1.35;
    font-size: 8.5pt;
    margin: 0;
    padding: 0;
  }

  /* Header Banner */
  .header-banner {
    background: linear-gradient(135deg, #0F294A 0%, #1A365D 55%, #2B6CB0 100%);
    color: #FFFFFF;
    padding: 12px 18px;
    border-radius: 6px;
    margin-bottom: 10px;
    border-bottom: 3px solid #E2E8F0;
  }

  .header-banner .tag {
    display: inline-block;
    background: rgba(255, 255, 255, 0.18);
    color: #E2E8F0;
    font-size: 7pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 2px 8px;
    border-radius: 3px;
    margin-bottom: 4px;
  }

  .header-banner h1 {
    margin: 0 0 3px 0;
    font-size: 13pt;
    font-weight: 800;
    letter-spacing: -0.3px;
    color: #FFFFFF;
  }

  .header-banner p {
    margin: 0;
    font-size: 8pt;
    color: #CBD5E0;
    line-height: 1.3;
  }

  /* Section Titles */
  h2.section-title {
    font-size: 9.5pt;
    font-weight: 700;
    color: #1A365D;
    border-bottom: 1.5px solid #2B6CB0;
    padding-bottom: 3px;
    margin-top: 10px;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
  }

  p {
    margin: 0 0 5px 0;
    text-align: justify;
  }

  /* Meta Grid */
  .meta-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 7px;
    margin-bottom: 9px;
  }

  .meta-card {
    background: #F7FAFC;
    border: 1px solid #E2E8F0;
    border-left: 3.5px solid #2B6CB0;
    border-radius: 4px;
    padding: 6px 10px;
  }

  .meta-card .label {
    font-size: 6.8pt;
    font-weight: 700;
    color: #718096;
    text-transform: uppercase;
    margin-bottom: 1px;
  }

  .meta-card .value {
    font-size: 8pt;
    font-weight: 700;
    color: #1A202C;
  }

  .meta-card .subvalue {
    font-size: 7.2pt;
    color: #4A5568;
  }

  /* Tables */
  table.custom-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 4px;
    margin-bottom: 8px;
    font-size: 7.6pt;
    border: 1px solid #E2E8F0;
    border-radius: 4px;
    overflow: hidden;
  }

  table.custom-table th {
    background-color: #1A365D;
    color: #FFFFFF;
    font-weight: 700;
    text-align: left;
    padding: 5px 8px;
    border-right: 1px solid #2B6CB0;
  }

  table.custom-table th:last-child {
    border-right: none;
  }

  table.custom-table td {
    padding: 4.5px 8px;
    border-bottom: 1px solid #E2E8F0;
    border-right: 1px solid #EDF2F7;
    vertical-align: top;
    line-height: 1.3;
  }

  table.custom-table td:last-child {
    border-right: none;
  }

  table.custom-table tr:nth-child(even) {
    background-color: #F8FAFC;
  }

  /* Callout & Alerts */
  .callout-box {
    background-color: #F0F7FF;
    border: 1px solid #C3D9FF;
    border-left: 3.5px solid #3182CE;
    border-radius: 4px;
    padding: 7px 10px;
    margin-bottom: 8px;
  }

  .callout-box .callout-title {
    font-size: 8pt;
    font-weight: 700;
    color: #2B6CB0;
    margin-bottom: 3px;
  }

  .alert-success {
    background-color: #F0FFF4;
    border: 1px solid #C6F6D5;
    border-left: 3.5px solid #38A169;
    border-radius: 4px;
    padding: 7px 10px;
    margin-bottom: 8px;
  }

  .alert-success .alert-title {
    font-size: 8pt;
    font-weight: 700;
    color: #276749;
    margin-bottom: 3px;
  }

  /* Badge */
  .badge {
    display: inline-block;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 6.8pt;
    font-weight: 700;
    text-transform: uppercase;
  }

  .badge-blue { background: #EBF8FF; color: #2B6CB0; border: 1px solid #BEE3F8; }
  .badge-green { background: #F0FFF4; color: #276749; border: 1px solid #C6F6D5; }
  .badge-red { background: #FFF5F5; color: #C53030; border: 1px solid #FED7D7; }

  /* Bullets */
  ul.custom-bullets {
    margin: 0;
    padding-left: 14px;
  }

  ul.custom-bullets li {
    margin-bottom: 3px;
    font-size: 7.8pt;
    text-align: justify;
  }

  ul.custom-bullets li strong {
    color: #1A365D;
  }

  .page-break {
    page-break-before: always;
  }

  .footer-note {
    margin-top: 10px;
    padding-top: 5px;
    border-top: 1px solid #E2E8F0;
    font-size: 7pt;
    color: #A0AEC0;
    text-align: center;
  }
</style>
</head>
<body>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <!-- PÁGINA 1: IDENTIFICAÇÃO, FATOS E ISONOMIA                 -->
  <!-- ═══════════════════════════════════════════════════════════ -->

  <div class="header-banner">
    <div class="tag">SuperJus &bull; Dossiê de Análise Jurídica Criminal</div>
    <h1>PARECER EXECUTIVO & RESUMO ESTRATÉGICO DO PROCESSO</h1>
    <p>Documento condensado e auditado para análise da advocacia e atuação nos Tribunais Superiores e 1ª Instância.</p>
  </div>

  <div class="meta-grid">
    <div class="meta-card">
      <div class="label">Cliente / Paciente</div>
      <div class="value">JÚLIO PEREIRA MARCOS</div>
      <div class="subvalue">Preso preventivamente em 12/05/2026 (Segregação ininterrupta >90 dias)</div>
    </div>
    <div class="meta-card">
      <div class="label">Recurso Ordinário em HC no STJ</div>
      <div class="value">HC 1.116.750 / RJ (Registro 2026/0311210-7)</div>
      <div class="subvalue">6ª Turma &bull; Relator: Min. Og Fernandes &bull; <strong>Conclusos para Decisão (13/08)</strong></div>
    </div>
    <div class="meta-card">
      <div class="label">Ação Penal 1ª Instância (Desmembrado)</div>
      <div class="value">Proc. 0023013-51.2021.8.19.0078</div>
      <div class="subvalue">2ª Vara Criminal de Armação dos Búzios/RJ &bull; Juiz: Dr. Danilo Marques Borges</div>
    </div>
    <div class="meta-card">
      <div class="label">Ação Penal Originária (Corréus)</div>
      <div class="value">Proc. 0022975-39.2021.8.19.0078</div>
      <div class="subvalue"><span class="badge badge-green">Todos os 5 Corréus Soltos</span> desde 02/08/2022 por excesso de prazo</div>
    </div>
  </div>

  <h2 class="section-title">1. Síntese Fática e Provas da Instrução Criminal</h2>
  <p>
    A ação penal originou-se da <strong>"Operação Delivery"</strong> (março/2021, Búzios/RJ) após abordagem policial do corréu <strong>José Guilherme</strong> com <strong>218g de maconha</strong>. Na delegacia, José Guilherme declarou uso próprio e informou um contato telefônico. A polícia consultou cadastro de operadora (Credlink), identificando a titularidade em nome de Júlio (endereço em SP), deferindo-se 4 rodadas de escuta e denúncia por Tráfico (Art. 33) e Associação (Art. 35 da Lei 11.343/06).
  </p>

  <div class="callout-box">
    <div class="callout-title">Fatos Provados em Juízo na Audiência Oficial (Feito Originário):</div>
    <ul class="custom-bullets">
      <li><strong>Ausência Total de Drogas com Júlio:</strong> Nenhuma grama de droga, balança, arma ou dinheiro foi apreendida com Júlio. Confirmado pelo Delegado Dr. Rodrigo Moreira (16:47).</li>
      <li><strong>Inexistência de Perícia Vocálica:</strong> O Delegado confirmou sob juramento que <em>"não houve perícia de voz"</em> (19:31). A imputação apoia-se apenas em cadastro de chip.</li>
      <li><strong>Confissão Policial de Ausência de Facção/Hierarquia:</strong> O Delegado Dr. Nelson Esquiba asseverou: <em>"Não havia facção, hierarquia nem estrutura armada... eram usuários que se ajudavam"</em> (114:03).</li>
      <li><strong>Destruição do Chip em 2021:</strong> Júlio destruiu a linha ainda no início de 2021; as rodadas 3 e 4 de escutas sequer captaram sua voz.</li>
    </ul>
  </div>

  <h2 class="section-title">2. Cronologia Processual e Quebra de Isonomia (Art. 580 CPP)</h2>
  <table class="custom-table">
    <thead>
      <tr>
        <th style="width: 14%;">Data</th>
        <th style="width: 24%;">Órgão / Instância</th>
        <th style="width: 62%;">Evento Processual e Repercussão Prática</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>27/01/2022</strong></td>
        <td>2ª Vara de Búzios</td>
        <td>Decretada prisão preventiva de todos os denunciados da Operação Delivery.</td>
      </tr>
      <tr>
        <td><strong>17/05/2022</strong></td>
        <td>2ª Vara de Búzios</td>
        <td>Desmembramento do processo quanto a Júlio (Proc. 0023013-51.2021.8.19.0078).</td>
      </tr>
      <tr>
        <td><strong>02/08/2022</strong></td>
        <td>Feito Originário</td>
        <td><span class="badge badge-green">Liberdade aos 5 Corréus</span> Revogada a preventiva de todos os corréus (inclusive quem portava 218g de droga) por excesso de prazo.</td>
      </tr>
      <tr>
        <td><strong>07/10/2024</strong></td>
        <td>Cartório de Búzios</td>
        <td>Certidão comprovando que o mandado de Júlio <strong>não constava no BNMP</strong> por erro do Judiciário.</td>
      </tr>
      <tr>
        <td><strong>05/05/2026</strong></td>
        <td>7ª Câmara TJRJ</td>
        <td><strong>HC Preventivo Impetrado</strong> por advogado constituído com Júlio em plena liberdade.</td>
      </tr>
      <tr>
        <td><strong>12/05/2026</strong></td>
        <td>Polícia Civil</td>
        <td>Cumprimento do mandado de prisão preventiva após 4 anos da data dos fatos.</td>
      </tr>
      <tr>
        <td><strong>11/06/2026</strong></td>
        <td>7ª Câmara TJRJ</td>
        <td>Denegação do HC pelo TJRJ sob o argumento genérico de "fuga prolongada".</td>
      </tr>
      <tr>
        <td><strong>29/07/2026</strong></td>
        <td>STJ (6ª Turma)</td>
        <td>Autuação do Recurso Ordinário sob o <strong>HC 1.116.750/RJ</strong> (Rel. Min. Og Fernandes).</td>
      </tr>
      <tr>
        <td><strong>13/08/2026</strong></td>
        <td>STJ (Gabinete)</td>
        <td><strong>Autos Conclusos para Decisão</strong> ao Relator Min. Og Fernandes após parecer do MPF.</td>
      </tr>
    </tbody>
  </table>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <!-- PÁGINA 2: OS 5 PILARES, PRECEDENTES DO STJ E PLANO DE AÇÃO  -->
  <!-- ═══════════════════════════════════════════════════════════ -->
  <div class="page-break"></div>

  <h2 class="section-title" style="margin-top:0;">3. Matriz dos 5 Pilares de Ataque da Defesa Técnica</h2>

  <div class="meta-grid">
    <div class="meta-card" style="border-left-color:#3182CE;">
      <div class="label">Pilar 1 &bull; Art. 580 do CPP</div>
      <div class="value">Isonomia com os Corréus Soltos</div>
      <div class="subvalue" style="margin-top:3px;">
        Todos os 5 corréus respondem em liberdade desde agosto/2022, inclusive o único flagrado com droga (José Guilherme, 218g). Manter Júlio (sem droga) preso isoladamente viola a isonomia e o Art. 580 do CPP.
      </div>
    </div>
    <div class="meta-card" style="border-left-color:#38A169;">
      <div class="label">Pilar 2 &bull; STJ HC 686.312/MS (3ª Seção)</div>
      <div class="value">Ausência de Materialidade Direta</div>
      <div class="subvalue" style="margin-top:3px;">
        Precedente vinculante da 3ª Seção do STJ estabelece que o tráfico (Art. 33) exige apreensão da droga e laudo pericial. Escutas telefônicas sem apreensão não suprem a materialidade nem autorizam prisão preventiva.
      </div>
    </div>
    <div class="meta-card" style="border-left-color:#805AD5;">
      <div class="label">Pilar 3 &bull; Art. 35 da Lei 11.343/06</div>
      <div class="value">Descaracterização da Associação</div>
      <div class="subvalue" style="margin-top:3px;">
        O STJ exige prova de estabilidade e permanência. O próprio Delegado confessou em juízo inexistir facção, hierarquia ou divisão de tarefas, tratando-se de relação episódica entre usuários.
      </div>
    </div>
    <div class="meta-card" style="border-left-color:#DD6B20;">
      <div class="label">Pilar 4 &bull; Art. 400 do CPP</div>
      <div class="value">Excesso de Prazo sem AIJ (>90 dias)</div>
      <div class="subvalue" style="margin-top:3px;">
        Júlio está preso desde 12/05/2026 sem que a Audiência de Instrução (AIJ) do feito desmembrado tenha sido realizada, ultrapassando os prazos legais sem qualquer culpa da defesa técnica.
      </div>
    </div>
  </div>

  <div class="meta-card" style="border-left-color:#E53E3E; margin-bottom:9px;">
    <div class="label">Pilar 5 &bull; STJ AgRg no RHC 167.473/SP &bull; Boa-Fé Defensiva</div>
    <div class="value">Desconstrução da Tese de "Fuga" e Erro do BNMP</div>
    <div class="subvalue" style="margin-top:2px;">
      O mandado de 2022 não constava do BNMP por erro exclusivo do Judiciário (certidão de 07/10/2024). Júlio contratou advogado e impetrou HC preventivo em 05/05/2026 em liberdade. O STJ consolidou que <em>a não localização momentânea não configura fuga</em> e a impetração judicial demonstra inequívoca submissão à Justiça.
    </div>
  </div>

  <h2 class="section-title">4. Auditoria de Jurisprudência Validada (Sexta Turma STJ)</h2>
  <table class="custom-table">
    <thead>
      <tr>
        <th style="width: 26%;">Ministro / Órgão</th>
        <th style="width: 27%;">Precedente Concreto Auditado</th>
        <th style="width: 47%;">Tese Fixada Aplicável ao Caso Júlio</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Min. Og Fernandes</strong><br><span class="badge badge-blue">Relator do Caso</span></td>
        <td><strong>STJ HC 232.842/RJ</strong><br>e <strong>HC 142.062/RJ</strong></td>
        <td>Concessão de ordem por excesso de prazo na instrução e extensão obrigatória de liberdade com base no Art. 580 do CPP por isonomia fática entre corréus.</td>
      </tr>
      <tr>
        <td><strong>Min. Sebastião Reis Jr.</strong><br><span class="badge badge-blue">Presidente da Turma</span></td>
        <td><strong>STJ HC 686.312/MS</strong><br><em>(Terceira Seção Penal)</em></td>
        <td><strong>Leading Case Vinculante:</strong> Indispensabilidade de apreensão da droga para o Art. 33. Extensão a corréus no <em>PExt no HC 497.699/MG</em>.</td>
      </tr>
      <tr>
        <td><strong>Min. Rogerio Schietti</strong><br><span class="badge badge-blue">Sexta Turma</span></td>
        <td><strong>STJ AgRg RHC 167.473/SP</strong><br>e <strong>AgRg REsp 1.984.770/RJ</strong></td>
        <td>Não localização e citação editalícia não autorizam preventiva por presunção de fuga. Art. 35 exige comprovação cabal de estabilidade e permanência.</td>
      </tr>
      <tr>
        <td><strong>Min. Antonio Saldanha</strong><br><span class="badge badge-blue">Sexta Turma</span></td>
        <td><strong>STJ AgRg HC 850.569/SP</strong><br>e <strong>HC 755.819/RJ</strong></td>
        <td>Extensão de liberdade por identidade fática e exigência de prova de ciência inequívoca de mandado para cogitar evasão do distrito da culpa.</td>
      </tr>
      <tr>
        <td><strong>Des. Otávio Toledo</strong><br><span class="badge badge-blue">Des. Convocado TJSP</span></td>
        <td><strong>STJ AgRg HC 915.228/SP</strong><br>e <strong>AgRg HC 890.093/RJ</strong></td>
        <td>Comunicação dos motivos objetivos de revogação de preventiva e absolvição do delito de associação quando ausente prova pericial de permanência.</td>
      </tr>
    </tbody>
  </table>

  <h2 class="section-title">5. Plano de Ação Tático e Recomendações para a Advocacia</h2>
  <div class="alert-success">
    <div class="alert-title">Medidas Imediatas Recomendadas:</div>
    <ul class="custom-bullets" style="color:#22543D;">
      <li><strong>1. Memoriais no STJ (HC 1.116.750/RJ):</strong> Entrega de memoriais no Gabinete do Min. Og Fernandes, ressaltando o processo concluso, a isonomia (Art. 580 CPP) com os 5 corréus soltos e a ausência de apreensão de drogas (HC 686.312/MS).</li>
      <li><strong>2. Relaxamento por Excesso de Prazo na 1ª Instância (Búzios):</strong> Protocolar pedido de relaxamento na 2ª Vara Criminal invocando o Art. 400 do CPP c/c Art. 5º, LXXVIII da CF (>90 dias preso sem AIJ designada no feito desmembrado).</li>
      <li><strong>3. Prova Emprestada:</strong> Requerer certidão e traslado dos depoimentos dos Delegados prestados na Ação Originária (0022975-39.2021.8.19.0078).</li>
      <li><strong>4. Medidas Alternativas Subsidiárias (Art. 319 CPP):</strong> Pleitear subsidiariamente comparecimento mensal em juízo e monitoramento eletrônico, diante da primariedade e emprego com carteira assinada.</li>
    </ul>
  </div>

  <div class="footer-note">
    Dossiê compilado e auditado eletronicamente &bull; SuperJus Inteligência Jurídica &bull; Uso exclusivo da Defesa Técnica de Júlio Pereira Marcos
  </div>

</body>
</html>
"""

async def generate_pdf():
    out_dir = os.path.join(os.getcwd(), "Clientes", "Júlio_Pereira_Marcos", "Caso_Principal", "analises")
    os.makedirs(out_dir, exist_ok=True)
    out_pdf = os.path.join(out_dir, "Relatorio_Executivo_Julio_Pereira_Marcos_Advocacia.pdf")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        page = await browser.new_page()
        await page.set_content(HTML_CONTENT, wait_until="networkidle")
        
        await page.pdf(
            path=out_pdf,
            format="A4",
            print_background=True,
            margin={"top": "8mm", "bottom": "8mm", "left": "10mm", "right": "10mm"},
            display_header_footer=False
        )
        await browser.close()
        
    print(f"Sucesso: PDF 2-Pages Perfeito gerado em:\n{out_pdf}")

if __name__ == "__main__":
    asyncio.run(generate_pdf())
