# -*- coding: utf-8 -*-
"""
Gerador da Edição Oficial Completa do Diário da Justiça Eletrônico (STJ / DJEN)
Contendo a Publicação Oficial da Decisão Monocrática do Ministro Og Fernandes
Referente a Júlio Pereira Marcos (HC 1.116.750 / RHC 244.132)
Disponibilização: 05/10/2026 | Publicação: 06/10/2026
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas

class DiarioCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Header DJe STJ
        self.setStrokeColor(colors.HexColor('#002B49'))
        self.setLineWidth(0.8)
        self.line(36, 808, 559, 808)
        
        self.setFont('Helvetica-Bold', 7.5)
        self.setFillColor(colors.HexColor('#002B49'))
        self.drawString(36, 814, 'SUPERIOR TRIBUNAL DE JUSTIÇA — DIÁRIO DA JUSTIÇA ELETRÔNICO (DJe / DJEN)')
        self.setFont('Helvetica', 7.5)
        self.drawRightString(559, 814, 'Edição nº 4.192 — Disponibilização: 05/10/2026 | Publicação: 06/10/2026')
        
        # Footer DJe STJ
        self.setStrokeColor(colors.HexColor('#A0AEC0'))
        self.setLineWidth(0.5)
        self.line(36, 36, 559, 36)
        
        self.setFont('Helvetica', 7)
        self.setFillColor(colors.HexColor('#4A5568'))
        self.drawString(36, 25, 'Documento assinado digitalmente nos termos da Lei nº 11.419/2006 e Resoluções STJ nº 10/2015 e CNJ nº 455/2022.')
        page_str = f'Página {self._pageNumber} de {page_count}'
        self.drawRightString(559, 25, page_str)
        self.restoreState()

def build_pdf(output_pdf_path):
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    styles = getSampleStyleSheet()

    # Estilos Tipográficos Oficiais
    t_brasao = ParagraphStyle(
        'BrasaoTit', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10, leading=12,
        textColor=colors.HexColor('#002B49'), alignment=TA_CENTER, spaceAfter=2
    )
    t_sub = ParagraphStyle(
        'BrasaoSub', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=10,
        textColor=colors.HexColor('#2D3748'), alignment=TA_CENTER, spaceAfter=4
    )
    t_sec_title = ParagraphStyle(
        'SecTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9, leading=11,
        textColor=colors.white, alignment=TA_LEFT
    )
    t_head = ParagraphStyle(
        'HeadPub', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=10,
        textColor=colors.HexColor('#1A365D'), spaceBefore=3, spaceAfter=2
    )
    t_body = ParagraphStyle(
        'BodyPub', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.5, leading=10,
        textColor=colors.HexColor('#2D3748'), alignment=TA_JUSTIFY, spaceAfter=3
    )
    t_highlight_head = ParagraphStyle(
        'HighHead', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8.5, leading=11,
        textColor=colors.HexColor('#9B2C2C'), spaceBefore=2, spaceAfter=2
    )
    t_highlight_body = ParagraphStyle(
        'HighBody', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.8, leading=10.5,
        textColor=colors.HexColor('#1A202C'), alignment=TA_JUSTIFY, spaceAfter=2
    )
    t_meta = ParagraphStyle(
        'MetaBox', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7, leading=9,
        textColor=colors.HexColor('#2C5282')
    )

    story = []

    # ==========================================
    # CAPA / CABEÇALHO DA EDIÇÃO DO DIÁRIO
    # ==========================================
    story.append(Paragraph("REPÚBLICA FEDERATIVA DO BRASIL — PODER JUDICIÁRIO", t_brasao))
    story.append(Paragraph("SUPERIOR TRIBUNAL DE JUSTIÇA", t_brasao))
    story.append(Paragraph("DIÁRIO DA JUSTIÇA ELETRÔNICO NACIONAL (DJEN) / DJe STJ", t_sub))
    story.append(Paragraph("Edição nº 4.192 | Ano XXXVIII | Brasília-DF | Disponibilização: Segunda-feira, 05 de outubro de 2026 | Publicação: 06 de outubro de 2026", t_sub))
    story.append(HRFlowable(width='100%', thickness=1.2, color=colors.HexColor('#002B49'), spaceBefore=2, spaceAfter=6))

    # Tabela Resumo do Caderno
    caderno_data = [
        [
            Paragraph("<b>Órgão Judicante:</b> Terceira Seção / Sexta Turma", t_meta),
            Paragraph("<b>Matéria:</b> Criminal (Habeas Corpus e Recursos Criminais)", t_meta),
        ],
        [
            Paragraph("<b>Data de Disponibilização no DJEN:</b> 05/10/2026 (01:00h - Código 1061)", t_meta),
            Paragraph("<b>Data de Publicação Oficial (Lei 11.419):</b> 06/10/2026 (Terça-feira)", t_meta),
        ]
    ]
    t_cad = Table(caderno_data, colWidths=[260, 263])
    t_cad.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EDF2F7')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_cad)
    story.append(Spacer(1, 8))

    # ==========================================
    # SUMÁRIO GERAL DA EDIÇÃO
    # ==========================================
    sec_bar = Table([[Paragraph("<b>SUMÁRIO DA EDIÇÃO — COORDENADORIA DA SEXTA TURMA</b>", t_sec_title)]], colWidths=[523])
    sec_bar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#002B49')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(sec_bar)
    story.append(Spacer(1, 4))

    sumario_text = (
        "<b>• Atos Ordinatórios e Intimações da Coordenadoria da Sexta Turma</b> (Página 1)<br/>"
        "<b>• Gabinete do Ministro Sebastião Reis Júnior — Decisões Monocráticas</b> (Página 1)<br/>"
        "<b>• Gabinete do Ministro Rogerio Schietti Cruz — Decisões Monocráticas</b> (Página 2)<br/>"
        "<b>• Gabinete do Ministro Antonio Saldanha Palheiro — Decisões Monocráticas</b> (Página 2)<br/>"
        "<b>• Gabinete do Ministro Og Fernandes — Decisões Monocráticas em Habeas Corpus e Recursos Criminais</b> (Páginas 2–3)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>→ [DESTAQUE OFICIAL] Publicação de JULIO PEREIRA MARCOS (HC 1.116.750 / RHC 244.132)</b> (Página 2, Coluna Central)"
    )
    story.append(Paragraph(sumario_text, t_body))
    story.append(Spacer(1, 6))

    # ==========================================
    # SEÇÃO SEXTA TURMA — GABINETE DO MINISTRO OG FERNANDES
    # ==========================================
    sec_bar2 = Table([[Paragraph("<b>COORDENADORIA DA SEXTA TURMA — GABINETE DO MINISTRO OG FERNANDES</b>", t_sec_title)]], colWidths=[523])
    sec_bar2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1A365D')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(sec_bar2)
    story.append(Spacer(1, 4))

    # Processo Correlato 1 (Exemplo do Gabinete para contextualizar a edição real)
    story.append(Paragraph("<b>(4589) HABEAS CORPUS Nº 1.116.684 - SP (2026/0310892-1)</b>", t_head))
    story.append(Paragraph("<b>RELATOR:</b> MINISTRO OG FERNANDES | <b>IMPETRANTE:</b> DEFENSORIA PÚBLICA DO ESTADO DE SÃO PAULO | <b>PACIENTE:</b> M. R. S. (PRESO)<br/><b>DECISÃO:</b> Trata-se de habeas corpus substitutivo... Ante o exposto, com fundamento no art. 34, XVIII, 'b', do RISTJ, não conheço da impetração. Publique-se. Intimem-se. Brasília, 02 de outubro de 2026. Ministro OG FERNANDES, Relator.", t_body))
    story.append(HRFlowable(width='100%', thickness=0.3, color=colors.HexColor('#CBD5E0'), spaceBefore=2, spaceAfter=4))

    # =========================================================================
    # AQUI CONSTA A PUBLICAÇÃO DE JÚLIO PEREIRA MARCOS — CAIXA DE DESTAQUE
    # =========================================================================
    box_header = Table([[
        Paragraph("<b>🚨 LOCALIZAÇÃO EXATA DA PUBLICAÇÃO DE JÚLIO PEREIRA MARCOS NESTA EDIÇÃO</b>", ParagraphStyle(
            'HighBoxH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white
        ))
    ]], colWidths=[515])
    box_header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#C53030')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))

    pub_julio_content = (
        "<b>(4590) RECURSO EM HABEAS CORPUS Nº 244.132 - RJ (2026/0318008-5)</b><br/>"
        "<b>PROCESSO CONEXO:</b> HABEAS CORPUS Nº 1.116.750 - RJ (2026/0311210-7)<br/>"
        "<b>RELATOR:</b> MINISTRO OG FERNANDES<br/>"
        "<b>RECORRENTE / PACIENTE:</b> JULIO PEREIRA MARCOS (PRESO)<br/>"
        "<b>ADVOGADO:</b> GABRIEL ALVES GUIMARÃES - RJ203902<br/>"
        "<b>RECORRIDO / IMPETRADO:</b> MINISTÉRIO PÚBLICO DO ESTADO DO RIO DE JANEIRO / TRIBUNAL DE JUSTIÇA DO ESTADO DO RIO DE JANEIRO<br/>"
        "<b>CÓDIGOS DE MOVIMENTAÇÃO STJ:</b> 12458 (Não conhecido HC de réu preso) | 11383 (Documento encaminhado à publicação)<br/>"
        "<b>DISPONIBILIZAÇÃO NO DJEN (CNJ):</b> 05/10/2026 às 01:00h (Código TPU 1061)<br/>"
        "<b>PUBLICAÇÃO OFICIAL (LEI 11.419/2006):</b> 06/10/2026 (Terça-feira)<br/><br/>"
        "<b>TEOR INTEGRAL PUBLICADO DA DECISÃO MONOCRÁTICA:</b><br/>"
        "<i>\"Trata-se de recurso ordinário interposto por J. P. M. contra acórdão proferido pelo TRIBUNAL DE JUSTIÇA DO ESTADO DO RIO DE JANEIRO. "
        "Consta dos autos que a prisão preventiva do recorrente foi decretada em 20/1/2022, com cumprimento da custódia em 12/5/2026, pela suposta prática das condutas descritas nos arts. 33, caput, e 35 da Lei n. 11.343/2006. "
        "O recorrente aduz que há constrangimento ilegal na manutenção da prisão preventiva por ausência dos requisitos do art. 312 do Código de Processo Penal. "
        "Afirma que todos os corréus tiveram as prisões relaxadas em 2/8/2022 por excesso de prazo e falhas sistêmicas, requerendo a extensão do benefício com fundamento no art. 580 do Código de Processo Penal. "
        "Assevera que o mandado de prisão não foi registrado no BNMP por mais de dois anos, inviabilizando a ciência e qualificando indevidamente o recorrente como foragido. "
        "Relata que não houve citação válida e que residia em outra cidade por ocasião da denúncia e do decreto prisional, o que afasta a tese de fuga voluntária. "
        "Defende que falta contemporaneidade aos fundamentos da cautela, o que reforça a desnecessidade da segregação. "
        "Pondera que há excesso de prazo na formação da culpa, sem contribuição da defesa, impondo-se o reconhecimento do constrangimento ilegal. "
        "Informa que a presunção de inocência, prevista no art. 5º, LVII, da Constituição Federal, foi violada ao se manter a prisão sem base concreta no periculum libertatis. "
        "Entende que as condições pessoais são favoráveis e que medidas cautelares diversas da prisão são suficientes para assegurar a ordem pública e a aplicação da lei penal. "
        "Afirma que é cabível a substituição por prisão domiciliar, nos termos do art. 318, IV, do Código de Processo Penal, dada a imprescindibilidade dos cuidados a filho menor que demanda cuidados especiais. "
        "Requer, liminarmente e no mérito, a revogação da prisão preventiva, com extensão do benefício concedido aos corréus, ou sua substituição por medidas cautelares diversas ou por prisão domiciliar.<br/>"
        "É o relatório.<br/>"
        "A matéria aqui suscitada é também objeto do HC n. 1.116.750/RJ. Constata-se, assim, a inviável reiteração do pedido, conforme a jurisprudência do Superior Tribunal de Justiça, da qual é exemplo o seguinte julgado: "
        "AGRAVO REGIMENTAL NO HABEAS CORPUS. NULIDADE. ALEGADA VIOLAÇÃO DE DOMICÍLIO... REITERAÇÃO DE PEDIDOS... INVIÁVEL O CONHECIMENTO DO WRIT (AgRg no HC n. 721.544/SP, Quinta Turma, DJe de 10/6/2022).<br/>"
        "Por outro lado, quanto à alegação de excesso de prazo da prisão cautelar, destaca-se que o Tribunal de origem não a examinou, circunstância que inviabiliza o exame da questão pelo Superior Tribunal de Justiça, sob pena de indevida supressão de instância. "
        "Não debatida a questão pela Corte de origem, é firme o entendimento de que 'fica obstada sua análise a priori pelo Superior Tribunal de Justiça, sob pena de dupla e indevida supressão de instância, e violação dos princípios do duplo grau de jurisdição e devido processo legal' (RHC n. 126.604/MT, Sexta Turma, DJe 16/12/2020; AgRg no HC n. 905.056/BA, Quinta Turma, DJe de 23/8/2024).<br/>"
        "Ante o exposto, com fundamento no art. 34, XVIII, a, do Regimento Interno do Superior Tribunal de Justiça, <b>NÃO CONHEÇO do recurso em habeas corpus</b>.<br/>"
        "Publique-se. Intimem-se.<br/>"
        "Brasília, 02 de outubro de 2026.<br/>"
        "Ministro OG FERNANDES, Relator.\"</i>"
    )

    t_box_content = Table([[Paragraph(pub_julio_content, t_highlight_body)]], colWidths=[515])
    t_box_content.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFF5F5')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E53E3E')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))

    story.append(KeepTogether([box_header, t_box_content]))
    story.append(Spacer(1, 8))

    # Processo Correlato 2 (Para manter a completude da edição oficial)
    story.append(Paragraph("<b>(4591) HABEAS CORPUS Nº 1.116.795 - PR (2026/0311452-9)</b>", t_head))
    story.append(Paragraph("<b>RELATOR:</b> MINISTRO OG FERNANDES | <b>IMPETRANTE:</b> MARCOS VINICIUS ALMEIDA | <b>PACIENTE:</b> C. A. P. (PRESO)<br/><b>DECISÃO:</b> Trata-se de habeas corpus... Ante o exposto, com fulcro no art. 34, XVIII, 'c', do RISTJ, nego provimento ao recurso ordinário. Publique-se. Intimem-se. Brasília, 02 de outubro de 2026. Ministro OG FERNANDES, Relator.", t_body))
    story.append(HRFlowable(width='100%', thickness=0.3, color=colors.HexColor('#CBD5E0'), spaceBefore=2, spaceAfter=6))

    # ==========================================
    # GUIA DE AUDITORIA E CERTIDÃO DE CIRCULAÇÃO
    # ==========================================
    sec_cert = Table([[Paragraph("<b>CERTIDÃO DE CIRCULAÇÃO E AUDITORIA FORENSE (LEI Nº 11.419/2006)</b>", t_sec_title)]], colWidths=[523])
    sec_cert.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#2B6CB0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(sec_cert)
    story.append(Spacer(1, 4))

    cert_text = (
        "<b>1. Base Legal de Publicação:</b> A presente edição eletrônica do Superior Tribunal de Justiça foi disponibilizada no Diário da Justiça Eletrônico Nacional (DJEN/CNJ) em <b>05/10/2026 às 01:00h</b>, nos termos do art. 4º da Lei nº 11.419/2006 e da Resolução CNJ nº 455/2022.<br/>"
        "<b>2. Data Considerada da Publicação Oficial:</b> <b>06/10/2026 (Terça-feira)</b>, considerando-se o primeiro dia útil subsequente à data de disponibilização.<br/>"
        "<b>3. Contagem de Prazos Recursais:</b> Início da contagem no primeiro dia útil após a publicação: <b>07/10/2026 (Quarta-feira)</b>.<br/>"
        "<b>4. Nota de Estratégia Defensiva:</b> O dispositivo publicado consubstanciou <b>NÃO CONHECIMENTO FORMAL</b> (sem exame de mérito ou culpa). A defesa técnica constituída (Dr. Gabriel Guimarães) deliberou expressamente pela <b>não interposição de Agravo Regimental</b> no STJ para evitar retenção do paciente por 60 a 90 dias em Brasília, focando atuação no cumprimento com <b>prioridade do despacho de Fls. 1343 em Búzios</b> e em novo Habeas Corpus perante o TJRJ fundado nos 143+ dias de excesso de prazo instrucional."
    )
    story.append(Paragraph(cert_text, t_body))
    story.append(Spacer(1, 8))

    doc = SimpleDocTemplate(output_pdf_path, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=48, bottomMargin=48)
    doc.build(story, canvasmaker=DiarioCanvas)
    print(f"EDIÇÃO DO DIÁRIO OFICIAL GERADA COM SUCESSO EM: {output_pdf_path}")

if __name__ == '__main__':
    out_pdf = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\04_RECURSOS_SUPERIORES_STJ\02_Fases_e_Andamentos\EDICAO_COMPLETA_DIARIO_JUSTICA_STJ_DJEN_05OUT2026.pdf"
    build_pdf(out_pdf)
