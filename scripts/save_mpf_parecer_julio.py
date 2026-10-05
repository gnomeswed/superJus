# -*- coding: utf-8 -*-
import os, sys, asyncio
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")

MD_CONTENT = """# MINISTÉRIO PÚBLICO FEDERAL
## PROCURADORIA-GERAL DA REPÚBLICA

### MANIFESTAÇÃO MINISTERIAL Nº 68200-2026 – MFL
**HABEAS CORPUS Nº 1116750/RJ – Processo Eletrônico**  
**STJ - Petição Eletrônica (ParMPF) 00816581/2026 recebida em 13/08/2026 às 17:05:52 (e-STJ Fls. 121-127)**  
**Documento Eletrônico e-Pet nº 11930679 com assinatura eletrônica**  
**Signatário:** MARIO FERREIRA LEITE (Subprocurador-Geral da República) - CPF: ***.523.248-**  
**Data da Assinatura:** 13/08/2026 17:01:00  

---

* **IMPETRANTE:** GABRIEL ALVES GUIMARAES
* **ADVOGADO:** GABRIEL ALVES GUIMARÃES - RJ203902
* **IMPETRADO:** TRIBUNAL DE JUSTIÇA DO ESTADO DO RIO DE JANEIRO
* **PACIENTE:** JULIO PEREIRA MARCOS (PRESO)
* **INTERES.:** MINISTÉRIO PÚBLICO DO ESTADO DO RIO DE JANEIRO
* **RELATOR:** MINISTRO OG FERNANDES – SEXTA TURMA

---

### EMENTA DO MPF:
> **HABEAS CORPUS IMPETRADO CONCOMITANTEMENTE AO RECURSO ORDINÁRIO. INVIABILIDADE. PRISÃO PREVENTIVA. EXCESSO DE PRAZO NÃO CONFIGURADO. PACIENTE QUE PERMANECEU FORAGIDO POR MAIS DE QUATRO ANOS. INAPLICABILIDADE DO ART. 580 DO CPP. ESTADO DE FUGA QUE JUSTIFICA A CUSTÓDIA. CONDIÇÕES PESSOAIS FAVORÁVEIS IRRELEVANTES. PONTOS NÃO APRECIADOS NA ORIGEM. SUPRESSÃO DE INSTÂNCIAS. INEXISTÊNCIA DE CONSTRANGIMENTO ILEGAL. NÃO CONHECIMENTO DO WRIT.**

---

### ÍNTEGRA DA MANIFESTAÇÃO:

Trata-se de *habeas corpus* impetrado por GABRIEL ALVES GUIMARÃES em favor de JÚLIO PEREIRA MARCOS, contra acórdão proferido pela Sétima Câmara Criminal do TRIBUNAL DE JUSTIÇA DO ESTADO DO RIO DE JANEIRO, que denegou a ordem no HC nº 0029845-67.2026.8.19.0000.

Consta dos autos que o Paciente foi denunciado no âmbito da "Operação Delivery de Búzios" pela suposta prática dos crimes de tráfico de drogas e associação para o tráfico (arts. 33 e 35 da Lei nº 11.343/06). A prisão preventiva foi decretada em 20/01/2022 para garantia da ordem pública, diante da gravidade concreta dos fatos e da estrutura organizada do grupo criminoso, que utilizava sistema de "delivery" e aplicativos de mensagens para distribuição de entorpecentes em locais turísticos. O mandado de prisão foi cumprido apenas em 12/05/2026, tendo o paciente permanecido foragido por mais de quatro anos.

Irresignada, a defesa impetrou *habeas corpus* perante o Tribunal de Justiça do Estado do Rio de Janeiro, tendo a Segunda Câmara Criminal [sic], por unanimidade, denegado a ordem, conforme acórdão de fls. 15/25.

No presente *writ*, a defesa sustenta, em síntese:
a) constrangimento ilegal pela demora no processamento e remessa de Recurso Ordinário Constitucional interposto perante o Tribunal de origem em 19/06/2026;  
b) violação ao princípio da isonomia e ao art. 580 do CPP, uma vez que corréus do processo principal tiveram a prisão relaxada por excesso de prazo em 02/08/2022;  
c) que o "estado de fuga" é ilegítimo, pois o mandado de prisão permaneceu mais de dois anos sem registro no Banco Nacional de Mandados de Prisão (BNMP);  
d) a existência de condições pessoais favoráveis, como primariedade e residência fixa, além de ser genitor de criança que demanda cuidados especiais; e  
e) indícios de erro na identificação do paciente. Ao final, requer a revogação da prisão ou substituição por prisão domiciliar.

É a síntese do necessário.

#### 1. Do Não Conhecimento do Writ (Unirrecorribilidade)
A impetração é manifestamente incabível.

Conforme os autos, a defesa interpôs Recurso Ordinário Constitucional em 19/06/2026 contra o mesmo acórdão ora combatido. Embora o *habeas corpus* possua natureza de ação autônoma, quando utilizado concomitantemente com o recurso cabível para alcançar a mesma finalidade, qual seja, a reforma da decisão denegatória e a liberdade do paciente, configura-se nítida violação ao sistema recursal e ao princípio da unirrecorribilidade.

Nesse sentido:
> *"A jurisprudência desta Corte não admite a tramitação concomitante de recursos legalmente previstos e habeas corpus manejados contra o mesmo ato ou que questionem as mesmas matérias, sob pena de violação do princípio da unirrecorribilidade. Precedentes. (AgRg no HC n. 981.785/RJ, relator Ministro Antonio Saldanha Palheiro, Sexta Turma, julgado em 1/4/2025, DJEN de 7/4/2025)."*

Não se vislumbra qualquer ilegalidade passível de correção de ofício.

#### 2. Da Alegação de Excesso de Prazo
Inicialmente, no que tange à alegada demora na remessa do Recurso Ordinário não configura, por ora, constrangimento ilegal, pois como sabido o prazo para a prática de atos processuais não é peremptório, devendo ser aferido sob a ótica da razoabilidade.

No caso, o feito é complexo, oriundo de desmembramento de processo com múltiplos réus, o que justifica maior dilação procedimental. Ademais, o Tribunal de origem já prestou informações à fl. 112 e impulsionou o feito recentemente, afastando a desídia estatal.

#### 3. Da Inaplicabilidade do Art. 580 do CPP (Isonomia)
Noutro vértice, como assentado no acórdão, não há identidade fático-processual entre o paciente e os corréus soltos. Enquanto os corréus tiveram a prisão relaxada em 02/08/2022 por excesso de prazo na instrução do processo principal, o paciente permaneceu foragido por mais de quatro anos.

Vale mencionar que, como já assentado em julgados desse e. STJ, o estado de fuga é condição de caráter exclusivamente pessoal que impede a extensão de benefícios, tratando-se de elemento diferenciador que justifica o tratamento distinto para assegurar a aplicação da lei penal.

Sobre o tema:
> *"AGRAVO REGIMENTAL NO PEDIDO DE EXTENSÃO NO HABEAS CORPUS. ESTELIONATO. EXTENSÃO DOS EFEITOS DA DECISÃO DE REVOGAÇÃO DA PRISÃO PREVENTIVA DA CORRÉ. APLICAÇÃO DO ART. 580 DO CPP. IMPOSSIBILIDADE. REQUERENTE. CONDIÇÃO RECENTE DE FORAGIDA. SITUAÇÃO FÁTICA E JURÍDICA DISTINTA DA BENEFICIADA. AGRAVO REGIMENTAL NÃO PROVIDO. (...) 2. Segundo a jurisprudência desta Corte, 'a fuga do distrito da culpa é fundamento válido à segregação cautelar, forte da asseguração da aplicação da lei penal' (AgRg no HC n. 568.658/SP, relator Ministro Nefi Cordeiro, Sexta Turma, julgado em 4/8/2020, DJe 13/8/2020). (...) (AgRg no PExt no HC n. 1.042.157/SP, relator Ministro Rogerio Schietti Cruz, Sexta Turma, julgado em 27/5/2026, DJEN de 1/6/2026)."*

Ademais, os estreitos limites do presente remédio heroico não se coadunam com a verificação aprofundada da situação fática de foragido, na medida em que o estado de fuga restou devidamente assentado pelas instâncias ordinárias, sendo inviável sua desconstituição na presente via, de cognição probatória limitada.

#### 4. Das Condições Pessoais e Prisão Domiciliar
Além disso, sabe-se que as condições pessoais favoráveis (primariedade, residência fixa e trabalho) não são suficientes, por si sós, para revogar a custódia quando presentes os requisitos do art. 312 do CPP.

Quanto ao pedido de prisão domiciliar, conclui-se que não restou demonstrada a imprescindibilidade dos cuidados maternos à filha [sic], tampouco a defesa demonstrou perante as instâncias ordinárias os requisitos necessários do art. 318 do CPP, configurando supressão de instância.

#### 5. Conclusão / Dispositivo
Ante o exposto, o Ministério Público Federal, como *custos iuris*, postula o **NÃO CONHECIMENTO DO WRIT**.

Brasília, 13 de agosto de 2026.

**MARIO FERREIRA LEITE**  
Subprocurador-Geral da República
"""

HTML_CONTENT = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Manifestação Ministerial 68200-2026 - MPF STJ HC 1116750/RJ</title>
<style>
  @page {
    size: A4;
    margin: 25mm 20mm 25mm 20mm;
    @top-left {
      content: "STJ-Petição Eletrônica (ParMPF) 00816581/2026 recebida em 13/08/2026 17:05:52";
      font-size: 8pt;
      font-family: Arial, sans-serif;
      color: #333;
    }
    @top-right {
      content: "(e-STJ Fl. " counter(page, decimal-leading-zero) ")";
      font-size: 8pt;
      font-family: Arial, sans-serif;
      color: #333;
      font-weight: bold;
    }
    @bottom-left {
      content: "Documento assinado via Token digitalmente por MARIO FERREIRA LEITE em 13/08/2026 17:01. Chave: 01668bef.7b73a4f7.ab78597f.6d162f8d";
      font-size: 6.5pt;
      font-family: Arial, sans-serif;
      color: #666;
    }
  }

  body {
    font-family: "Times New Roman", Times, serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #000;
    margin: 0;
    padding: 0;
  }

  .header {
    text-align: center;
    margin-bottom: 25px;
  }

  .brasao {
    width: 65px;
    height: auto;
    margin-bottom: 8px;
  }

  .header h2 {
    font-size: 11pt;
    font-weight: bold;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .header h3 {
    font-size: 10pt;
    font-weight: bold;
    margin: 2px 0 0 0;
    text-transform: uppercase;
  }

  .doc-title {
    font-weight: bold;
    margin-top: 15px;
    margin-bottom: 15px;
    font-size: 11pt;
  }

  .proc-table {
    width: 100%;
    margin-bottom: 20px;
    font-size: 10.5pt;
    font-weight: bold;
  }

  .proc-table td {
    padding: 1.5px 0;
    vertical-align: top;
  }

  .ementa {
    margin-left: 35%;
    text-align: justify;
    font-size: 9.5pt;
    font-weight: bold;
    line-height: 1.35;
    margin-bottom: 30px;
    text-transform: uppercase;
  }

  p {
    text-align: justify;
    text-indent: 2.5cm;
    margin: 0 0 14px 0;
  }

  p.no-indent {
    text-indent: 0;
  }

  blockquote {
    margin: 15px 0 15px 2cm;
    text-align: justify;
    font-size: 10pt;
    line-height: 1.35;
  }

  .signature {
    margin-top: 40px;
    text-align: center;
  }

  .signature .name {
    font-weight: bold;
    font-size: 11pt;
    text-transform: uppercase;
  }

  .signature .cargo {
    font-size: 10.5pt;
  }

  .page-break {
    page-break-before: always;
  }
</style>
</head>
<body>

  <div class="header">
    <div style="font-size: 26pt; margin-bottom: 4px;">⚖️</div>
    <h2>MINISTÉRIO PÚBLICO FEDERAL</h2>
    <h3>PROCURADORIA-GERAL DA REPÚBLICA</h3>
  </div>

  <div class="doc-title">
    MANIFESTAÇÃO MINISTERIAL Nº 68200-2026 – MFL
  </div>

  <table class="proc-table">
    <tr><td style="width: 25%;">HABEAS CORPUS</td><td>Nº 1116750/RJ – Processo Eletrônico</td></tr>
    <tr><td>IMPETRANTE:</td><td>GABRIEL ALVES GUIMARAES</td></tr>
    <tr><td>ADVOGADO:</td><td>GABRIEL ALVES GUIMARÃES - RJ203902</td></tr>
    <tr><td>IMPETRADO:</td><td>TRIBUNAL DE JUSTIÇA DO ESTADO DO RIO DE JANEIRO</td></tr>
    <tr><td>PACIENTE:</td><td>JULIO PEREIRA MARCOS (PRESO)</td></tr>
    <tr><td>INTERES.:</td><td>MINISTÉRIO PÚBLICO DO ESTADO DO RIO DE JANEIRO</td></tr>
    <tr><td>RELATOR:</td><td>MINISTRO OG FERNANDES – SEXTA TURMA</td></tr>
  </table>

  <div class="ementa">
    HABEAS CORPUS IMPETRADO CONCOMITANTEMENTE AO RECURSO ORDINÁRIO. INVIABILIDADE. PRISÃO PREVENTIVA. EXCESSO DE PRAZO NÃO CONFIGURADO. PACIENTE QUE PERMANECEU FORAGIDO POR MAIS DE QUATRO ANOS. INAPLICABILIDADE DO ART. 580 DO CPP. ESTADO DE FUGA QUE JUSTIFICA A CUSTÓDIA. CONDIÇÕES PESSOAIS FAVORÁVEIS IRRELEVANTES. PONTOS NÃO APRECIADOS NA ORIGEM. SUPRESSÃO DE INSTÂNCIAS. INEXISTÊNCIA DE CONSTRANGIMENTO ILEGAL. NÃO CONHECIMENTO DO WRIT.
  </div>

  <p>
    Trata-se de <em>habeas corpus</em> impetrado por GABRIEL ALVES GUIMARÃES em favor de JÚLIO PEREIRA MARCOS, contra acórdão proferido pela Sétima Câmara Criminal do TRIBUNAL DE JUSTIÇA DO ESTADO DO RIO DE JANEIRO, que denegou a ordem no HC nº 0029845-67.2026.8.19.0000.
  </p>

  <p>
    Consta dos autos que o Paciente foi denunciado no âmbito da "Operação Delivery de Búzios" pela suposta prática dos crimes de tráfico de drogas e associação para o tráfico (arts. 33 e 35 da Lei nº 11.343/06). A prisão preventiva foi decretada em 20/01/2022 para garantia da ordem pública, diante da gravidade concreta dos fatos e da estrutura organizada do grupo criminoso, que utilizava sistema de "delivery" e aplicativos de mensagens para distribuição de entorpecentes em locais turísticos. O mandado de prisão foi cumprido apenas em 12/05/2026, tendo o paciente permanecido foragido por mais de quatro anos.
  </p>

  <p>
    Irresignada, a defesa impetrou <em>habeas corpus</em> perante o Tribunal de Justiça do Estado do Rio de Janeiro, tendo a Segunda Câmara Criminal, por unanimidade, denegou a ordem, conforme acórdão de fls. 15/25.
  </p>

  <p>
    No presente <em>writ</em>, a defesa sustenta, em síntese: a) constrangimento ilegal pela demora no processamento e remessa de Recurso Ordinário Constitucional interposto perante o Tribunal de origem em 19/06/2026; b) violação ao princípio da isonomia e ao art. 580 do CPP, uma vez que corréus do processo principal tiveram a prisão relaxada por excesso de prazo em 02/08/2022; c) que o "estado de fuga" é ilegítimo, pois o mandado de prisão permaneceu mais de dois anos sem registro no Banco Nacional de Mandados de Prisão (BNMP); d) a existência de condições pessoais favoráveis, como primariedade e residência fixa, além de ser genitor de criança que demanda cuidados especiais; e e) indícios de erro na identificação do paciente. Ao final, requer a revogação da prisão ou substituição por prisão domiciliar.
  </p>

  <p>
    É a síntese do necessário.
  </p>

  <p>
    A impetração é manifestamente incabível.
  </p>

  <p>
    Conforme os autos, a defesa interpôs Recurso Ordinário Constitucional em 19/06/2026 contra o mesmo acórdão ora combatido. Embora o <em>habeas corpus</em> possua natureza de ação autônoma, quando utilizado concomitantemente com o recurso cabível para alcançar a mesma finalidade, quais seja, a reforma da decisão denegatória e a liberdade do paciente, configura-se nítida violação ao sistema recursal e ao princípio da unirrecorribilidade.
  </p>

  <p class="no-indent">
    Nesse sentido:
  </p>

  <blockquote>
    A jurisprudência desta Corte não admite a tramitação concomitante de recursos legalmente previstos e habeas corpus manejados contra o mesmo ato ou que questionem as mesmas matérias, sob pena de violação do princípio da unirrecorribilidade. Precedentes. (AgRg no HC n. 981.785/RJ, relator Ministro Antonio Saldanha Palheiro, Sexta Turma, julgado em 1/4/2025, DJEN de 7/4/2025).
  </blockquote>

  <p>
    Não se vislumbra qualquer ilegalidade passível de correção de ofício.
  </p>

  <p>
    Inicialmente, no que tange à alegada demora na remessa do Recurso Ordinário não configura, por ora, constrangimento ilegal, pois como sabido o prazo para a prática de atos processuais não é peremptório, devendo ser aferido sob a ótica da razoabilidade.
  </p>

  <p>
    No caso, o feito é complexo, oriundo de desmembramento de processo com múltiplos réus, o que justifica maior dilação procedimental. Ademais, o Tribunal de origem já prestou informações à fl. 112 e impulsionou o feito recentemente, afastando a desídia estatal.
  </p>

  <p>
    Noutro vértice, como assentado no acórdão, não há identidade fático-processual entre o paciente e os corréus soltos. Enquanto os corréus tiveram a prisão relaxada em 02/08/2022 por excesso de prazo na instrução do processo principal, o paciente permaneceu foragido por mais de quatro anos.
  </p>

  <p>
    Vale mencionar que, como já assentado em julgados desse e. STJ, o estado de fuga é condição de caráter exclusivamente pessoal que impede a extensão de benefícios, tratando-se de elemento diferenciador que justifica o tratamento distinto para assegurar a aplicação da lei penal.
  </p>

  <p class="no-indent">
    Sobre o tema:
  </p>

  <blockquote>
    AGRAVO REGIMENTAL NO PEDIDO DE EXTENSÃO NO HABEAS CORPUS. ESTELIONATO. EXTENSÃO DOS EFEITOS DA DECISÃO DE REVOGAÇÃO DA PRISÃO PREVENTIVA DA CORRÉ. APLICAÇÃO DO ART. 580 DO CPP. IMPOSSIBILIDADE. REQUERENTE. CONDIÇÃO RECENTE DE FORAGIDA. SITUAÇÃO FÁTICA E JURÍDICA DISTINTA DA BENEFICIADA. AGRAVO REGIMENTAL NÃO PROVIDO.<br>
    1. O art. 580 do Código de Processo Penal prevê: "No caso de concurso de agentes (Código Penal, art. 25), a decisão do recurso interposto por um dos réus, se fundado em motivos que não sejam de caráter exclusivamente pessoal, aproveitará aos outros".<br>
    2. Segundo a jurisprudência desta Corte, "a fuga do distrito da culpa é fundamento válido à segregação cautelar, forte da asseguração da aplicação da lei penal" (AgRg no HC n. 568.658/SP, relator Ministro Nefi Cordeiro, Sexta Turma, julgado em 4/8/2020, DJe 13/8/2020).<br>
    3. No caso, os fundamentos que ensejaram a substituição da prisão preventiva da ré Maria Eduarda de Oliveira Santos pela medidas cautelares previstas no art. 319, I, III e IV, do CPP não aproveitam à ora agravante, nos termos do art. 580 do CPP. Isso porque ela esteve foragida até 30/1/2026, o que a coloca em situação fática e jurídica distinta da corré, a qual ficou presa por mais de dois anos.<br>
    4. Agravo regimental não provido.<br>
    (AgRg no PExt no HC n. 1.042.157/SP, relator Ministro Rogerio Schietti Cruz, Sexta Turma, julgado em 27/5/2026, DJEN de 1/6/2026.)
  </blockquote>

  <p>
    Ademais, os estreitos limites do presente remédio heroico não se coadunam com a verificação aprofundada da situação fática de foragido, na medida em que o estado de fuga restou devidamente assentado pelas instâncias ordinárias, sendo inviável sua desconstituição na presente via, como dito, de cognição probatória limitada.
  </p>

  <p>
    Além disso, sabe-se que as condições pessoais favoráveis (primariedade, residência fixa e trabalho) não são suficientes, por si sós, para revogar a custódia quando presentes os requisitos do art. 312 do CPP. Da mesma forma, medidas cautelares diversas do cárcere se revelam inadequadas tanto em decorrência da gravidade da conduta quanto pelo risco de fuga.
  </p>

  <p>
    Por fim, o pleito pelo cumprimento da segregação em domicílio não foi enfrentado pela Corte de origem na forma como alegada, não tendo sido examinados seus requisitos essenciais. Tampouco a defesa demonstrou, perante as instâncias ordinárias, a imprescindibilidade dos cuidados maternos exclusivos ou a impossibilidade de assistência por outros familiares, requisitos necessários para a incidência do art. 318, IV, do CPP. A análise inaugural da matéria, nesses termos, incorreria em indevida supressão de instância.
  </p>

  <p>
    Assim, não se verifica a existência de constrangimento ilegal.
  </p>

  <p>
    Ante o exposto, o Ministério Público Federal, como <em>custos iuris</em>, postula o <strong>não conhecimento do <em>writ</em></strong>.
  </p>

  <div class="signature">
    Brasília, 13 de agosto de 2026.<br><br>
    <div class="name">MARIO FERREIRA LEITE</div>
    <div class="cargo">Subprocurador-Geral da República</div>
  </div>

</body>
</html>
"""

async def main():
    # 1. Salvar Markdown na pasta oficial 04_RECURSOS_SUPERIORES_STJ/03_Peticoes_e_Pareceres
    dir1 = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\04_RECURSOS_SUPERIORES_STJ\03_Peticoes_e_Pareceres"
    os.makedirs(dir1, exist_ok=True)
    md_file1 = os.path.join(dir1, "2026-08-13_Manifestacao_Ministerial_68200_2026_MPF_STJ_HC_1116750.md")
    pdf_file1 = os.path.join(dir1, "2026-08-13_Manifestacao_Ministerial_68200_2026_MPF_STJ_HC_1116750.pdf")

    with open(md_file1, "w", encoding="utf-8") as f:
        f.write(MD_CONTENT)
    print(f"MD salvo em: {md_file1}")

    # 2. Renderizar PDF idêntico com Playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        page = await browser.new_page()
        await page.set_content(HTML_CONTENT, wait_until="networkidle")
        await page.pdf(
            path=pdf_file1,
            format="A4",
            print_background=True,
            display_header_footer=False
        )
        await browser.close()
    print(f"PDF salvo em: {pdf_file1}")

    # 3. Espelhar na pasta Caso_Principal/documentos_processo
    dir2 = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
    os.makedirs(dir2, exist_ok=True)
    md_file2 = os.path.join(dir2, "2026-08-13_Manifestacao_Ministerial_68200_2026_MPF_STJ_HC_1116750.md")
    pdf_file2 = os.path.join(dir2, "2026-08-13_Manifestacao_Ministerial_68200_2026_MPF_STJ_HC_1116750.pdf")
    
    with open(md_file2, "w", encoding="utf-8") as f:
        f.write(MD_CONTENT)
    import shutil
    shutil.copy(pdf_file1, pdf_file2)
    print(f"Arquivos espelhados em: {dir2}")

if __name__ == "__main__":
    asyncio.run(main())
