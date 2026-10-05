# -*- coding: utf-8 -*-
"""
SUPERJUS · GERADOR DE RELATÓRIO EXECUTIVO EM PDF
Cliente: JOÃO ROBERTO PEREIRA ALIBERTI
Processo: 0807146-37.2026.8.19.0004 (1ª Vara Criminal de São Gonçalo)
"""

import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
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
        # Cabeçalho
        self.setStrokeColor(colors.HexColor('#1A365D'))
        self.setLineWidth(1)
        self.line(36, 804, 559, 804)
        
        self.setFont('Helvetica-Bold', 8)
        self.setFillColor(colors.HexColor('#1A365D'))
        self.drawString(36, 810, 'SUPERJUS · RELATÓRIO EXECUTIVO DE AUDITORIA PROCESSUAL')
        
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#4A5568'))
        self.drawRightString(559, 810, 'PROCESSO: 0807146-37.2026.8.19.0004')

        # Rodapé
        self.setStrokeColor(colors.HexColor('#CBD5E0'))
        self.setLineWidth(0.5)
        self.line(36, 42, 559, 42)
        
        self.setFont('Helvetica', 7.5)
        self.setFillColor(colors.HexColor('#718096'))
        self.drawString(36, 30, 'Documento de Análise Jurídica Estratégica · Uso Restrito e Confidencial')
        
        page_str = f'Página {self._pageNumber} de {page_count}'
        self.drawRightString(559, 30, page_str)
        self.restoreState()


def build_pdf(output_path):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=50,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Estilos customizados
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#1A365D'),
        alignment=TA_LEFT,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#4A5568'),
        alignment=TA_LEFT,
        spaceAfter=8
    )

    sec_title = ParagraphStyle(
        'SecTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1A365D'),
        spaceBefore=10,
        spaceAfter=4
    )

    subsec_title = ParagraphStyle(
        'SubSecTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#2B6CB0'),
        spaceBefore=6,
        spaceAfter=3
    )

    body = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#2D3748'),
        alignment=TA_JUSTIFY,
        spaceAfter=4
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body,
        fontName='Helvetica-Bold'
    )

    bullet = ParagraphStyle(
        'BulletItem',
        parent=body,
        leftIndent=12,
        spaceAfter=3
    )

    box_text = ParagraphStyle(
        'BoxText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1A202C')
    )

    th_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=TA_CENTER
    )

    td_style = ParagraphStyle(
        'TD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#1A202C')
    )

    td_bold = ParagraphStyle(
        'TDBold',
        parent=td_style,
        fontName='Helvetica-Bold'
    )

    story = []

    # Cabeçalho Principal
    story.append(Paragraph('RELATÓRIO EXECUTIVO PROCESSUAL · SITUAÇÃO CARCERÁRIA E ESTRATÉGIA', title_style))
    story.append(Paragraph('<b>Cliente:</b> JOÃO ROBERTO PEREIRA ALIBERTI &nbsp;|&nbsp; <b>CPF:</b> 001.585.661-57 &nbsp;|&nbsp; <b>Data da Consulta:</b> 01/10/2026', subtitle_style))
    story.append(HRFlowable(width='100%', thickness=1.5, color=colors.HexColor('#2B6CB0'), spaceBefore=2, spaceAfter=8))

    # Box Resumo Geral / Status Atual
    box_data = [
        [
            Paragraph('<b>STATUS ATUAL:</b> PRESO PREVENTIVAMENTE (Condenado em 1º Grau)', box_text),
            Paragraph('<b>DATA DA PRISÃO:</b> 14/04/2026 (170 dias cumpridos)', box_text)
        ],
        [
            Paragraph('<b>PENA TOTAL:</b> 04 anos e 06 meses de reclusão', box_text),
            Paragraph('<b>REGIME ATUAL:</b> FECHADO (Fixado em Embargos em 29/09/2026)', box_text)
        ],
        [
            Paragraph('<b>JUÍZO:</b> 1ª Vara Criminal de São Gonçalo / TJRJ', box_text),
            Paragraph('<b>DEFESA ATUAL:</b> Defensoria Pública do Estado do RJ', box_text)
        ]
    ]
    t_box = Table(box_data, colWidths=[260, 263])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EDF2F7')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_box)
    story.append(Spacer(1, 8))

    # 1. FATOS E HISTÓRICO DA PRISÃO
    story.append(Paragraph('1. Histórico da Prisão e Imputação Acusatória', sec_title))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#CBD5E0'), spaceBefore=1, spaceAfter=4))
    story.append(Paragraph(
        'O réu <b>JOÃO ROBERTO PEREIRA ALIBERTI</b> foi preso em flagrante delito em <b>14 de abril de 2026</b>, por volta das 14h20, por agentes da Polícia Rodoviária Federal na Rodovia BR-101 (km 313, Boa Vista, Comarca de São Gonçalo/RJ), conduzindo o automóvel <b>FIAT/FASTBACK AUDACE</b>, cor cinza, ano/modelo 2025/2025, ostentando placas TIR2G81.',
        body
    ))
    story.append(Paragraph(
        'Conforme laudo pericial (ID 282281355), o veículo apresentava adulteração física na gravação do chassi e numeração do motor lixada/ilegível. Em <b>16 de abril de 2026</b>, em audiência de custódia realizada na Central de Benfica (Capital), a prisão em flagrante foi convertida em <b>Prisão Preventiva</b>. O Ministério Público denunciou o acusado pela prática do <b>Artigo 311, § 2º, inciso III, do Código Penal</b> (adulteração de sinal identificador veicular na modalidade conduzir veículo remarcado que devia saber estar adulterado).',
        body
    ))

    # 2. STATUS EM TEMPO REAL: CONDENAÇÃO E EMBARGOS (SETEMBRO/2026)
    story.append(Paragraph('2. Condenação Recente e Reforma via Embargos de Declaração', sec_title))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#CBD5E0'), spaceBefore=1, spaceAfter=4))
    story.append(Paragraph(
        'O processo teve desfecho em 1ª Instância em setembro de 2026, perante a Juíza Titular Dra. Simone Ferraz Holmes:',
        body
    ))
    story.append(Paragraph(
        '• <b>Sentença Condenatória (23/09/2026 - ID 308795133):</b> A denúncia foi julgada integralmente PROCEDENTE. Originalmente, por equívoco na 3ª fase da dosimetria (diminuição indevida de 1/6), a juíza havia fixado a pena em 3 anos e 9 meses e determinado o regime semiaberto.',
        bullet
    ))
    story.append(Paragraph(
        '• <b>Acolhimento de Embargos do MP (29/09/2026 - ID 309698418):</b> O Ministério Público apontou erro material na 3ª fase. A magistrada acolheu os embargos do parquet e <b>retificou a pena para 04 (quatro) anos e 06 (seis) meses de reclusão</b> e 14 dias-multa, <b>AGRAVANDO o regime inicial para FECHADO</b> (art. 33, § 2º, "b", a contrario sensu, e § 3º do CP), fundamentando na multirreincidência e maus antecedentes.',
        bullet
    ))
    story.append(Paragraph(
        '• <b>Manutenção da Prisão Cautelar:</b> Foi expressamente <b>negado o direito de recorrer em liberdade</b>, permanecendo João Roberto custodiado preventivamente.',
        bullet
    ))
    story.append(Paragraph(
        '• <b>Último Andamento (30/09/2026 às 11:25):</b> Juntada de petição de ciência da Defensoria Pública/MP. O prazo para <b>Apelação Criminal</b> está transcorrendo neste momento.',
        bullet
    ))

    # 3. QUANTO TEMPO ATÉ O REGIME SEMIABERTO? (MEMÓRIA DE CÁLCULO LEP)
    story.append(Paragraph('3. Cálculo de Benefícios na Execução Penal (Quanto Tempo até o Semiaberto)', sec_title))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#CBD5E0'), spaceBefore=1, spaceAfter=4))
    story.append(Paragraph(
        'Para fins de progressão de regime prisional, o crime do Artigo 311 do Código Penal é delito comum, <b>cometido sem violência física ou grave ameaça à pessoa</b>. Pelo Pacote Anticrime (Lei 13.964/2019), aplica-se a seguinte métrica:',
        body
    ))

    calc_table_data = [
        [Paragraph('PARÂMETRO LEGAL', th_style), Paragraph('REGRA APLICADA', th_style), Paragraph('DETALHAMENTO', th_style), Paragraph('DATA PREVISTA', th_style)],
        [
            Paragraph('<b>Pena Total</b>', td_bold),
            Paragraph('04 anos e 06 meses', td_style),
            Paragraph('54 meses (1.642 dias)', td_style),
            Paragraph('Término: 14/10/2030', td_style)
        ],
        [
            Paragraph('<b>Fração de Progressão</b>', td_bold),
            Paragraph('<b>20% da Pena</b>', td_bold),
            Paragraph('Art. 112, II da LEP (Reincidente em crime sem violência)', td_style),
            Paragraph('Exige: <b>10 meses e 24 dias</b> (328 dias)', td_bold)
        ],
        [
            Paragraph('<b>Tempo Já Cumprido</b>', td_bold),
            Paragraph('170 dias de prisão', td_style),
            Paragraph('De 14/04/2026 até hoje (01/10/2026)', td_style),
            Paragraph('<b>5 meses e 20 dias</b>', td_bold)
        ],
        [
            Paragraph('<b>Saldo Restante (LEP)</b>', td_bold),
            Paragraph('<b>158 dias</b>', td_bold),
            Paragraph('Tempo faltante para completar o lapso temporal objetivo', td_style),
            Paragraph('<b>📅 08 de março de 2027</b>', td_bold)
        ]
    ]
    t_calc = Table(calc_table_data, colWidths=[110, 110, 190, 113])
    t_calc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2B6CB0')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F7FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_calc)
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '<i>* Nota sobre Remição: Caso o apenado comprove trabalho na unidade prisional (1 dia remido a cada 3 trabalhados) ou leitura orientada de livros (Resolução CNJ nº 391/2021 — até 48 dias remidos/ano), o requisito objetivo do semiaberto será atingido antecipadamente, entre <b>dezembro de 2026 e janeiro de 2027</b>.</i>',
        body
    ))

    # 4. VIA ESTRATÉGICA RÁPIDA: APELAÇÃO E HABEAS CORPUS NO TJRJ
    story.append(Paragraph('4. Linha de Ação Imediata: Como Conquistar o Semiaberto ou Soltura Agora', sec_title))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#CBD5E0'), spaceBefore=1, spaceAfter=4))
    story.append(Paragraph(
        'Aguardar passivamente março de 2027 pela LEP não é a melhor estratégia técnica. A sentença de 1º Grau possui vícios graves que autorizam a <b>imediata concessão do regime semiaberto ou da liberdade provisória perante o Tribunal de Justiça (TJRJ)</b>:',
        body
    ))
    story.append(Paragraph(
        '1. <b>Nulidade da Exasperação da Pena-Base (1ª Fase):</b> A magistrada aumentou a pena-base em 1/4 sustentando "delito de natureza interestadual" e "promessa de recompensa". O crime do Art. 311 do CP não possui majorante interestadual. Criar causa de aumento pretoriana fora das balizas estritas do tipo penal viola o princípio da estrita legalidade e da proporcionalidade.',
        bullet
    ))
    story.append(Paragraph(
        '2. <b>Incidência da Súmula 269 do Superior Tribunal de Justiça (STJ):</b> Afastada a exasperação indevida da 1ª fase, a pena corporal cairá para patamar igual ou inferior a 4 anos. A Súmula 269/STJ dispõe categoricamente: <i>"É admissível a adoção do regime prisional semiaberto aos reincidentes condenados a pena igual ou inferior a quatro anos se favoráveis as circunstâncias judiciais"</i>.',
        bullet
    ))
    story.append(Paragraph(
        '3. <b>Detração Penal Obrigatória (Artigo 387, § 2º, do CPP):</b> O juiz ou Tribunal deve computar o período de prisão cautelar para determinar o regime de cumprimento. Abatendo-se os quase 6 meses que João Roberto já cumpriu em regime fechado cautelar, o saldo restante de pena autoriza a fixação imediata do regime semiaberto no julgamento colegiado.',
        bullet
    ))
    story.append(Paragraph(
        '4. <b>Habeas Corpus de Soltura por Incompatibilidade da Prisão Preventiva:</b> Manter o réu preso preventivamente em regime fechado para aguardar o trânsito em julgado de crime sem violência é flagrantemente mais severo do que a execução definitiva futura (Princípio da Homogeneidade das Cautelares — Precedentes STF HC 187.672 e STJ HC 648.887).',
        bullet
    ))

    # 5. QUADRO DE PROVIDÊNCIAS URGENTES
    story.append(Paragraph('5. Quadro de Providências Imediatas Recomendadas', sec_title))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#CBD5E0'), spaceBefore=1, spaceAfter=4))

    action_data = [
        [Paragraph('MEDIDA PROCESSUAL', th_style), Paragraph('OBJETIVO / IMPACTO', th_style), Paragraph('PRAZO / STATUS', th_style)],
        [
            Paragraph('<b>1. Habilitação de Defesa Particular</b>', td_bold),
            Paragraph('Juntada de Procuração revogando a atuação da Defensoria Pública para assunção privativa dos autos.', td_style),
            Paragraph('<b>Imediato</b>', td_bold)
        ],
        [
            Paragraph('<b>2. Interposição de Apelação Criminal</b>', td_bold),
            Paragraph('Recorrer da sentença com pedido expresso de apresentação das razões diretamente no TJRJ (Art. 600, § 4º, CPP).', td_style),
            Paragraph('<b>Prazo Aberto</b> (Ciência em 30/09)', td_bold)
        ],
        [
            Paragraph('<b>3. Impetração de Habeas Corpus no TJRJ</b>', td_bold),
            Paragraph('Pleitear a imediata concessão de liberdade provisória ou fixação de regime semiaberto provisório até o julgamento final.', td_style),
            Paragraph('Distribuição Imediata às Câmaras Criminais', td_style)
        ]
    ]
    t_action = Table(action_data, colWidths=[140, 260, 123])
    t_action.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A365D')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F7FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_action)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f'PDF gerado com sucesso em: {output_path}')

if __name__ == '__main__':
    out_client = r'c:\Projetos\superJus\Clientes\Joao_Roberto_Pereira_Aliberti\03_Documentos_do_Processo\Resumo_Executivo_Joao_Roberto_Pereira.pdf'
    out_root = r'c:\Projetos\superJus\Resumo_Executivo_Joao_Roberto_Pereira.pdf'
    out_brain = r'C:\Users\Administrator\.gemini\antigravity\brain\d96fd02d-8378-458e-8786-3df5a8e554ec\Resumo_Executivo_Joao_Roberto_Pereira.pdf'
    
    build_pdf(out_client)
    build_pdf(out_root)
    build_pdf(out_brain)
