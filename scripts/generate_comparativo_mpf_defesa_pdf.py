# -*- coding: utf-8 -*-
import os, sys, asyncio
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")

HTML_CONTENT = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Confronto Analítico: Parecer do MPF vs. Petição da Defesa - STJ HC 1.116.750/RJ</title>
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
    line-height: 1.38;
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
    padding: 5px 8px;
    border-bottom: 1px solid #E2E8F0;
    border-right: 1px solid #EDF2F7;
    vertical-align: top;
    line-height: 1.32;
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

  .alert-danger {
    background-color: #FFF5F5;
    border: 1px solid #FED7D7;
    border-left: 3.5px solid #E53E3E;
    border-radius: 4px;
    padding: 7px 10px;
    margin-bottom: 8px;
  }

  .alert-danger .alert-title {
    font-size: 8pt;
    font-weight: 700;
    color: #C53030;
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

  /* Badges */
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
  .badge-amber { background: #FFFAF0; color: #C05621; border: 1px solid #FEEBC8; }

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
  <!-- PÁGINA 1: CABEÇALHO, METADADOS E TABELA COMPARATIVA         -->
  <!-- ═══════════════════════════════════════════════════════════ -->

  <div class="header-banner">
    <div class="tag">SuperJus &bull; Confronto Analítico & Parecer Estratégico</div>
    <h1>CONFRONTO ANALÍTICO: PARECER DO MPF vs. PETIÇÃO DA DEFESA</h1>
    <p>Dissecção crítica da Manifestação Ministerial nº 68200-2026 frente às teses do RHC perante o Superior Tribunal de Justiça.</p>
  </div>

  <div class="meta-grid">
    <div class="meta-card">
      <div class="label">Processo Superior (STJ)</div>
      <div class="value">HC 1.116.750 / RJ (Registro 2026/0311210-7)</div>
      <div class="subvalue">6ª Turma &bull; Relator: Min. Og Fernandes &bull; <strong>Conclusos para Decisão</strong></div>
    </div>
    <div class="meta-card">
      <div class="label">Paciente / Réu</div>
      <div class="value">JÚLIO PEREIRA MARCOS</div>
      <div class="subvalue">Ação Penal 0023013-51.2021.8.19.0078 (2ª Vara Criminal de Búzios)</div>
    </div>
    <div class="meta-card">
      <div class="label">Peça da Acusação Federal (MPF)</div>
      <div class="value">Manifestação Ministerial nº 68200-2026 – MFL</div>
      <div class="subvalue">Subprocurador-Geral da República Dr. Mário Ferreira Leite (13/08/2026)</div>
    </div>
    <div class="meta-card">
      <div class="label">Patrono da Defesa Técnica</div>
      <div class="value">Dr. Gabriel Alves Guimarães (OAB/RJ 203.902)</div>
      <div class="subvalue">Petição de Habeas Corpus & Recurso Ordinário Constitucional</div>
    </div>
  </div>

  <h2 class="section-title">1. Quadro Comparativo Ponto a Ponto (Acusação vs. Defesa)</h2>

  <table class="custom-table">
    <thead>
      <tr>
        <th style="width: 18%;">Eixo Jurídico</th>
        <th style="width: 28%;">🏛️ O que a DEFESA Sustenta</th>
        <th style="width: 27%;">⚖️ O que o MPF Argumenta</th>
        <th style="width: 27%;">🔍 Avaliação Técnica (STJ)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>1. Admissibilidade do Recurso</strong></td>
        <td>O HC no STJ é indispensável para sanar <strong>constrangimento ilegal imediato</strong> decorrente da mora do TJRJ em remeter o Recurso Ordinário.</td>
        <td>Alega <strong>violação da unirrecorribilidade</strong>: a defesa não poderia usar HC e RHC simultaneamente contra o mesmo ato (cita <em>AgRg no HC 981.785/RJ</em>).</td>
        <td><span class="badge badge-green">Vantagem Defesa</span> O STJ pacificou que, mesmo não conhecendo do writ, <strong>concede a ordem de ofício</strong> se houver ilegalidade manifesta na prisão.</td>
      </tr>
      <tr>
        <td><strong>2. Isonomia com Corréus (Art. 580 CPP)</strong></td>
        <td><strong>Todos os 5 corréus do feito originário foram soltos em 02/08/2022</strong>, inclusive quem portava 218g de droga. Manter Júlio preso viola a isonomia.</td>
        <td>Sustenta que <strong>não cabe extensão do Art. 580</strong>: a "condição de foragido por 4 anos" seria motivo pessoal impeditivo (cita <em>AgRg no PExt HC 1.042.157/SP</em>).</td>
        <td><span class="badge badge-blue">Ponto Central</span> A soltura dos corréus decorreu de <strong>motivo objetivo</strong> (demora e fragilidade cautelar). A 6ª Turma aplica o Art. 580 em casos objetivos.</td>
      </tr>
      <tr>
        <td><strong>3. A Tese de "Fuga" do Acusado</strong></td>
        <td><strong>Não houve fuga deliberada:</strong> O mandado de 2022 <strong>não constava no BNMP</strong> por erro judicial (certidão de 07/10/2024). Impetrou <strong>HC preventivo em 05/05/2026</strong> em liberdade.</td>
        <td>Afirma que permaneceu 4 anos sem se apresentar, restando caracterizado o <strong>estado de foragido</strong> que justifica a preventiva para aplicação da lei penal.</td>
        <td><span class="badge badge-green">Vantagem Defesa</span> O precedente <em>AgRg no RHC 167.473/SP</em> firma que a não localização por falha estatal não se confunde com fuga deliberada.</td>
      </tr>
      <tr>
        <td><strong>4. Materialidade do Tráfico e Provas</strong></td>
        <td><strong>Zero droga apreendida com Júlio:</strong> Delegado confessou em juízo inexistir droga com ele (<em>HC 686.312/MS</em>) e ausência de perícia de voz. Negou facção/hierarquia (Art. 35).</td>
        <td>Utiliza <strong>narrativa genérica</strong>: cita gravidade do esquema "delivery" por mensagens em Búzios, sem enfrentar a falta de apreensão física com o paciente.</td>
        <td><span class="badge badge-green">Vantagem Defesa</span> Precedente vinculante da 3ª Seção (<em>HC 686.312/MS</em>): tráfico exige apreensão da droga e laudo pericial definitivo.</td>
      </tr>
      <tr>
        <td><strong>5. Condições Pessoais e Domiciliar</strong></td>
        <td>Júlio é primário, com residência fixa, carteira assinada e genitor de criança com necessidades especiais, cabendo medidas do Art. 319 do CPP.</td>
        <td>Alega que condições favoráveis não impedem a preventiva e que a prisão domiciliar não foi apreciada na origem (supressão de instância).</td>
        <td><span class="badge badge-amber">Equilíbrio</span> Condições pessoais somadas à falta de contemporaneidade e excesso de prazo (>90 dias sem AIJ) justificam cautelares alternativas.</td>
      </tr>
    </tbody>
  </table>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <!-- PÁGINA 2: FRAGILIDADES DO MPF, JURISPRUDÊNCIA E CONCLUSÃO  -->
  <!-- ═══════════════════════════════════════════════════════════ -->
  <div class="page-break"></div>

  <h2 class="section-title" style="margin-top:0;">2. As 3 Fragilidades Críticas do Parecer do Ministério Público Federal</h2>

  <div class="alert-danger">
    <div class="alert-title">1. Uso de Modelo Padrão sem Aderência aos Fatos Reais de Búzios:</div>
    <p>
      O parecer ministerial menciona genericamente a suposta operação de <em>"laboratórios clandestinos de droga e esquema de lavagem de capitais"</em> (e-STJ fl. 125). Tais fatos <strong>nunca existiram na Operação Delivery de Búzios</strong> (que tratou de venda episódica de maconha sem armas). Isso demonstra que a acusação se valeu de fundamentação genérica/copia-e-cola sem confrontar a prova dos autos.
    </p>
  </div>

  <div class="callout-box">
    <div class="callout-title">2. Omissão Deliberada Quanto à Falha no BNMP e Boa-Fé do Paciente:</div>
    <p>
      O MPF repete a pecha de "foragido por mais de 4 anos", mas <strong>silencia totalmente sobre a Certidão Cartorária de 07/10/2024</strong> (que atesta que o mandado nunca constou do Banco Nacional de Mandados de Prisão por falha do Judiciário) e sobre a <strong>impetração de HC preventivo em 05/05/2026</strong>, quando Júlio estava em plena liberdade, demonstrando voluntária submissão à jurisdição.
    </p>
  </div>

  <div class="callout-box" style="border-left-color:#DD6B20; background-color:#FFFAF0; border-color:#FEEBC8;">
    <div class="callout-title" style="color:#C05621;">3. Silêncio Inexplicável Sobre a Soltura do Único Réu Flagrado com a Droga:</div>
    <p style="color:#7B341E;">
      O MPF não oferece nenhuma justificativa para o fato de o corréu <strong>José Guilherme</strong> (o único indivíduo encontrado com 218g de maconha) estar em liberdade desde 02/08/2022, enquanto Júlio (com quem a polícia apreendeu zero grama de entorpecente) permanece encarcerado isoladamente, violando frontalmente o Art. 580 do CPP.
    </p>
  </div>

  <h2 class="section-title">3. Matriz de Confronto: Tese do MPF vs. Jurisprudência do STJ</h2>

  <table class="custom-table">
    <thead>
      <tr>
        <th style="width: 30%;">Tese Levantada pelo MPF</th>
        <th style="width: 35%;">Jurisprudência Auditada da 6ª Turma STJ</th>
        <th style="width: 35%;">Impacto Real no Julgamento</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><em>"Não conhecimento do HC por unirrecorribilidade"</em></td>
        <td><strong>Precedente Min. Og Fernandes / 6ª Turma:</strong> Concessão de ordem <em>ex officio</em> quando evidenciada ilegalidade na prisão (<em>HC 232.842/RJ</em>).</td>
        <td>Superação do óbice formal para apreciar a ilegalidade da prisão.</td>
      </tr>
      <tr>
        <td><em>"Fuga de 4 anos impede extensão do Art. 580 CPP"</em></td>
        <td><strong>Precedente Min. Rogerio Schietti:</strong> Não localização por erro do BNMP não equivale a fuga deliberada (<em>AgRg no RHC 167.473/SP</em>).</td>
        <td>Afastamento da tese de fuga; aplicação da isonomia processual.</td>
      </tr>
      <tr>
        <td><em>"Gravidade abstrata justifica a prisão preventiva"</em></td>
        <td><strong>Leading Case 3ª Seção (Min. Sebastião Reis):</strong> Tráfico exige apreensão de droga e laudo (<em>HC 686.312/MS</em>).</td>
        <td>Desproporcionalidade manifesta da custódia cautelar sem droga.</td>
      </tr>
      <tr>
        <td><em>"Inexistência de excesso de prazo na instrução"</em></td>
        <td><strong>Precedente Min. Og Fernandes:</strong> Prisão cautelar >90 dias sem realização da AIJ constitui constrangimento ilegal (<em>HC 193.308/BA</em>).</td>
        <td>Relaxamento da prisão ou substituição por cautelares diversas (Art. 319).</td>
      </tr>
    </tbody>
  </table>

  <h2 class="section-title">4. Conclusão e Próximos Passos para a Advocacia</h2>
  <div class="alert-success">
    <div class="alert-title">Direcionamento Estratégico Final:</div>
    <ul class="custom-bullets" style="color:#22543D;">
      <li>O parecer do MPF representa a postura defensiva padrão da acusação (buscando o não conhecimento formal), mas <strong>é substancialmente vulnerável</strong> nos pontos de mérito.</li>
      <li><strong>Ação Imediata Recomendada:</strong> Apresentar memoriais sucintos diretamente no Gabinete do <strong>Min. Og Fernandes</strong>, desmascarando a menção a "laboratórios clandestinos", comprovando a certidão do BNMP e ressaltando que todos os 5 corréus estão soltos desde 2022.</li>
    </ul>
  </div>

  <div class="footer-note">
    SuperJus Inteligência Jurídica &bull; Dossiê de Confronto Analítico &bull; Uso Exclusivo da Defesa Técnica de Júlio Pereira Marcos
  </div>

</body>
</html>
"""

async def generate_pdf():
    # 1. Diretórios de saída
    dir_stj = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\04_RECURSOS_SUPERIORES_STJ\03_Peticoes_e_Pareceres"
    dir_analises = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\analises"
    os.makedirs(dir_stj, exist_ok=True)
    os.makedirs(dir_analises, exist_ok=True)

    pdf_out1 = os.path.join(dir_stj, "Relatorio_Comparativo_Parecer_MPF_vs_Defesa_STJ.pdf")
    pdf_out2 = os.path.join(dir_analises, "Relatorio_Comparativo_Parecer_MPF_vs_Defesa_STJ.pdf")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        page = await browser.new_page()
        await page.set_content(HTML_CONTENT, wait_until="networkidle")
        
        await page.pdf(
            path=pdf_out1,
            format="A4",
            print_background=True,
            margin={"top": "8mm", "bottom": "8mm", "left": "10mm", "right": "10mm"},
            display_header_footer=False
        )
        await browser.close()
        
    import shutil
    shutil.copy(pdf_out1, pdf_out2)
    print(f"Sucesso: PDF Comparativo gerado em:\n{pdf_out1}\ne espelhado em:\n{pdf_out2}")

if __name__ == "__main__":
    asyncio.run(generate_pdf())
