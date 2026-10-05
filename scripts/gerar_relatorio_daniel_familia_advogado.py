# -*- coding: utf-8 -*-
import os
import sys
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas

sys.stdout.reconfigure(encoding="utf-8")

client_dir = r"C:\Projetos\superJus\Clientes\Daniel_Ferreira_Lima"
pdf_client_path = os.path.join(client_dir, "04_Analises_e_Estrategias", "Relatorio_Executivo_Daniel_Ferreira_Lima.pdf")
desktop_path = r"C:\Users\Administrator\Desktop\Relatorio_Executivo_Daniel_Ferreira_Lima.pdf"
brain_dir = r"C:\Users\Administrator\.gemini\antigravity\brain\8956167e-5498-4b7b-8577-663c5f130522"
pdf_brain_path = os.path.join(brain_dir, "Relatorio_Executivo_Daniel_Ferreira_Lima.pdf")

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
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        self.saveState()
        # Top rule and header
        self.setStrokeColor(colors.HexColor('#1A365D'))
        self.setLineWidth(1)
        self.line(40, 802, 555, 802)
        self.setFont('Helvetica-Bold', 8)
        self.setFillColor(colors.HexColor('#1A365D'))
        self.drawString(40, 808, 'SUPERJUS INTELIGÊNCIA JURÍDICA — RELATÓRIO PROCESSUAL ESTRATÉGICO')
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#4A5568'))
        self.drawRightString(555, 808, 'Caso: Daniel Ferreira Lima')
        
        # Bottom rule and footer
        self.setStrokeColor(colors.HexColor('#CBD5E0'))
        self.setLineWidth(0.6)
        self.line(40, 38, 555, 38)
        self.setFont('Helvetica', 7.5)
        self.setFillColor(colors.HexColor('#718096'))
        self.drawString(40, 26, 'Documento Informativo e Estratégico — Uso Exclusivo da Família e Defesa Técnica')
        page_str = f'Página {self._pageNumber} de {page_count}'
        self.drawRightString(555, 26, page_str)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        pdf_client_path,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=50,
        bottomMargin=50
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#1A365D'),
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#4A5568'),
        alignment=TA_CENTER
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#1A365D'),
        spaceBefore=12,
        spaceAfter=6
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#2B6CB0'),
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.2,
        textColor=colors.HexColor('#2D3748'),
        alignment=TA_JUSTIFY,
        spaceAfter=5
    )

    body_bold = ParagraphStyle(
        'Body_Bold_Custom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#2D3748')
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white,
        alignment=TA_CENTER
    )
    
    callout_text = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1A365D')
    )

    story = []
    
    # Header Banner
    story.append(Spacer(1, 5))
    story.append(Paragraph("RELATÓRIO ESTRATÉGICO PROCESSUAL E DOSSIÊ EXECUTIVO", title_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("AÇÃO PENAL Nº <b>0004301-33.2018.8.19.0073</b> — TRIBUNAL DE JUSTIÇA DO RIO DE JANEIRO", subtitle_style))
    story.append(Paragraph("Destinatários: <b>Família de Daniel Ferreira Lima</b> e <b>Advogado Constituído (Defesa Técnica)</b>", subtitle_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1A365D'), spaceAfter=10))

    # Tabela de Identificação
    meta_data = [
        [Paragraph("<b>Cliente / Apelante:</b>", table_cell), Paragraph("Daniel Ferreira Lima", table_cell),
         Paragraph("<b>Juízo de Origem:</b>", table_cell), Paragraph("Guapimirim / RJ — 2ª Vara Criminal (Júri)", table_cell)],
        [Paragraph("<b>Processo Principal:</b>", table_cell), Paragraph("0004301-33.2018.8.19.0073", table_cell),
         Paragraph("<b>Fase Atual:</b>", table_cell), Paragraph("Apelação Criminal remetida ao TJRJ (15/06/2026)", table_cell)],
        [Paragraph("<b>Imputação Penal:</b>", table_cell), Paragraph("Art. 121, § 2º, II do CP (Homicídio Qualificado)", table_cell),
         Paragraph("<b>Pena Sentenciada:</b>", table_cell), Paragraph("13 anos e 4 meses de reclusão (Regime Fechado)", table_cell)],
        [Paragraph("<b>Custódia Cautelar:</b>", table_cell), Paragraph("Preso preventivamente desde 14/03/2024", table_cell),
         Paragraph("<b>Defesa Técnica:</b>", table_cell), Paragraph("Advogado Constituído nos Autos", table_cell)]
    ]
    meta_table = Table(meta_data, colWidths=[110, 150, 100, 155])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # SEÇÃO 1: RESUMO EM LINGUAGEM CLARA PARA A FAMÍLIA
    story.append(Paragraph("1. RESUMO DA SITUAÇÃO ATUAL (CLARO E DIRETO PARA A FAMÍLIA)", h1_style))
    story.append(Paragraph(
        "Este documento foi elaborado para que a família e a defesa técnica tenham total clareza sobre o momento processual de <b>Daniel Ferreira Lima</b>. "
        "No dia <b>18 de maio de 2026</b>, ocorreu a sessão de julgamento pelo Tribunal do Júri na Comarca de Guapimirim. O Conselho de Sentença decidiu pela condenação de Daniel, "
        "e a Juíza Presidente fixou uma pena de <b>13 anos e 4 meses de reclusão em regime inicial fechado</b>, negando o direito de recorrer em liberdade.",
        body_style
    ))
    story.append(Paragraph(
        "<b>O que aconteceu depois do júri?</b> A defesa de Daniel não aceitou esse resultado e já <b>interpôs o Recurso de Apelação Criminal</b> no dia seguinte. "
        "O Ministério Público apresentou suas contrarrazões em 10 de junho de 2026 e, em <b>15 de junho de 2026</b>, o processo foi formalmente enviado para o <b>Tribunal de Justiça do Estado do Rio de Janeiro (TJRJ)</b> na capital. "
        "Portanto, o caso <b>NÃO está encerrado</b>. Ele agora será reexaminado por um colegiado de 3 Desembargadores especializados em Direito Penal, que têm o poder de anular o julgamento ou reduzir substancialmente a pena aplicada.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # Box de Destaque / Alinhamento de Expectativas
    alert_data = [[
        Paragraph("<b>PONTO FUNDAMENTAL DE TRANQUILIDADE PARA A FAMÍLIA:</b><br/>"
                  "A sentença do juiz de primeiro grau não é definitiva. O Ministério Público, em suas próprias contrarrazões, <b>confessou fatos que abrem caminho jurídico concreto</b> "
                  "no Superior Tribunal de Justiça (STJ) e no TJRJ para desclassificar o homicídio qualificado para simples e aplicar a detração penal, possibilitando a redução drástica da pena e a conquista do regime semiaberto.", callout_text)
    ]]
    alert_table = Table(alert_data, colWidths=[515])
    alert_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EBF8FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#3182CE')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(alert_table)
    story.append(Spacer(1, 10))

    # SEÇÃO 2: RADIOGRAFIA DA SENTENÇA CONDENATÓRIA
    story.append(Paragraph("2. RADIOGRAFIA DA CONDENAÇÃO (O QUE PESOU CONTRA DANIEL)", h1_style))
    story.append(Paragraph(
        "Para atuar com eficiência, a defesa auditou minuciosamente cada fração de pena e critério utilizado pelo Juiz Presidente na noite de 18/05/2026:",
        body_style
    ))
    
    calc_data = [
        [Paragraph("Fase da Dosimetria", table_header), Paragraph("Critério do Magistrado", table_header), Paragraph("Resultado Numérico", table_header), Paragraph("Vício Apontado pela Defesa", table_header)],
        [Paragraph("<b>1ª Fase:<br/>Pena-Base</b>", table_cell),
         Paragraph("Aumentou em <b>+2/6 (+4 anos)</b> alegando amizade prévia réu-vítima e pluralidade de agressões (tiros, pauladas e chutes).", table_cell),
         Paragraph("<b>16 anos</b><br/>(Mínimo legal era 12 anos)", table_cell),
         Paragraph("Ilegalidade: Amizade não integra culpabilidade extrema; ausência de individualização da conduta de Daniel na briga generalizada.", table_cell)],
        [Paragraph("<b>2ª Fase:<br/>Atenuantes</b>", table_cell),
         Paragraph("Reconheceu a <b>menoridade relativa (Art. 65, I, CP)</b>, reduzindo a pena na fração legal de <b>-1/6</b>.", table_cell),
         Paragraph("<b>13 anos e 4 meses</b><br/>(Pena Provisória)", table_cell),
         Paragraph("Acerto da sentença, mas a base de cálculo de onde partiu a redução estava indevidamente inflada.", table_cell)],
        [Paragraph("<b>3ª Fase:<br/>Causas de Aumento/Diminuição</b>", table_cell),
         Paragraph("Não foram reconhecidas causas de aumento nem minorantes de participação de menor importância.", table_cell),
         Paragraph("<b>13 anos e 4 meses</b><br/>(Pena Definitiva)", table_cell),
         Paragraph("Omissão de quesito obrigatório sobre participação secundária (Art. 29, § 1º, CP).", table_cell)],
        [Paragraph("<b>Detração Penal<br/>(Art. 387, § 2º CPP)</b>", table_cell),
         Paragraph("O Juiz <b>recusou-se a abater</b> o tempo em que Daniel esteve preso preventivamente (desde 14/03/2024), jogando o cálculo para a VEP.", table_cell),
         Paragraph("<b>Regime Fechado Mantido</b>", table_cell),
         Paragraph("<b>Erro Crítico:</b> O Art. 387, § 2º do CPP é norma obrigatória para o juiz de conhecimento fixar regime mais brando.", table_cell)]
    ]
    calc_table = Table(calc_data, colWidths=[85, 175, 95, 160])
    calc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2B6CB0')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#FFFFFF')),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#F7FAFC')),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor('#FFFFFF')),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(calc_table)
    story.append(Spacer(1, 12))

    # SEÇÃO 3: AS 4 GRANDES BRECHAS PARA O TJRJ
    story.append(Paragraph("3. OS 4 GRANDES PILARES DE ATAQUE NA APELAÇÃO (TJRJ)", h1_style))
    story.append(Paragraph(
        "A análise técnica das contrarrazões do Ministério Público revelou vulnerabilidades decisivas que serão exploradas pela defesa perante os Desembargadores do TJRJ:",
        body_style
    ))
    
    story.append(Paragraph("<b>A) Desavença Prévia por Som Automotivo AFASTA o Motivo Fútil (Precedente STJ):</b>", h2_style))
    story.append(Paragraph(
        "Na página 9 das contrarrazões, a própria Promotora de Justiça admitiu textualmente que o crime ocorreu em <i>'contexto de desavença anterior envolvendo os agentes e a vítima, relacionada ao volume de som automotivo'</i>. "
        "O Superior Tribunal de Justiça (STJ) tem entendimento consolidado e pacificado no sentido de que <b>a existência de anterior atrito verbal, animosidade ou desavença prévia entre autor e vítima afasta por completo a qualificadora do motivo fútil</b> "
        "(<b>STJ REsp 1.480.898/RS</b>, Rel. Min. Rogerio Schietti Cruz e <b>STJ AgRg no AREsp 1.442.278/MG</b>, Rel. Min. Sebastião Reis Júnior). "
        "<br/><b>Efeito Prático:</b> Ao afastar o motivo fútil, o crime passa de qualificado para <b>Homicídio Simples (Art. 121, caput, CP: 6 a 20 anos)</b>. "
        "A pena-base cai de 12 para 6 anos, e a pena final de Daniel desaba para a faixa de <b>5 a 7 anos de reclusão</b>!",
        body_style
    ))
    
    story.append(Paragraph("<b>B) Ilegalidade da Recusa da Detração Penal (Artigo 387, § 2º, do CPP):</b>", h2_style))
    story.append(Paragraph(
        "Daniel Ferreira Lima está preso ininterruptamente desde <b>14 de março de 2024</b> (mais de 2 anos e 3 meses de prisão cautelar cumprida). "
        "A Lei Federal nº 12.736/2012 determinou expressamente que o Juiz da condenação DEVE computar o tempo de prisão provisória para fins de fixação do regime inicial. "
        "O STJ já firmou a tese de que constitui constrangimento ilegal empurrar a detração para a Vara de Execuções Penais (VEP) quando o abatimento do tempo de prisão altera o regime prisional "
        "(<b>STJ HC 577.892/SP</b>, Rel. Min. Rogerio Schietti Cruz). Com a redução da pena e a detração dos 2 anos e 3 meses, Daniel passa a ter direito ao <b>regime semiaberto ou aberto</b>.",
        body_style
    ))
    
    story.append(Paragraph("<b>C) Violação à Plenitude de Defesa no Tribunal do Júri (Art. 5º, XXXVIII, 'a', da CF):</b>", h2_style))
    story.append(Paragraph(
        "A garantia constitucional do Júri assegura a <b>Plenitude de Defesa</b> (mais ampla que a ampla defesa comum). "
        "Durante os debates em plenário, a Juíza Presidente cerceou a fala da defesa técnica ao proibir menção à sentença do corréu e documentos anexos. "
        "Essa advertência pública causou manifesto prejuízo, pois induziu o Conselho de Sentença a acreditar que a defesa estaria utilizando argumentos ilegítimos. "
        "Trata-se de nulidade absoluta por violação ao princípio constitucional (Art. 564, IV c/c Art. 593, III, 'a', do CPP), justificando a <b>anulação da sessão e a realização de novo júri</b>.",
        body_style
    ))

    story.append(Paragraph("<b>D) O Período Foragido NÃO Autoriza Aumento de Pena-Base:</b>", h2_style))
    story.append(Paragraph(
        "A tentativa da acusação de utilizar os 4 anos de processo suspenso (Art. 366 do CPP) para justificar a gravidade da pena e a manutenção da prisão viola o entendimento do STJ "
        "(<b>Informativo de Jurisprudência nº 642 do STJ</b> e <b>HC 435.539/SP</b>). A fuga decorre do instinto natural de autodefesa e liberdade do ser humano, "
        "sendo estritamente vedado utilizá-la como vetor de conduta social ou personalidade negativa para inflar a pena-base do Art. 59 do Código Penal.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # SEÇÃO 4: LINHA DO TEMPO RECONSTITUÍDA
    story.append(Paragraph("4. HISTÓRICO E LINHA DO TEMPO PROCESSUAL AUDITADA", h1_style))
    timeline_data = [
        [Paragraph("Data", table_header), Paragraph("Instância / Órgão", table_header), Paragraph("Ato / Movimentação Decodificada", table_header), Paragraph("Efeito Prático", table_header)],
        [Paragraph("03/05/2018", table_cell), Paragraph("Guapimirim - 2ª Vara", table_cell), Paragraph("Distribuição da Ação Penal pelo MPRJ", table_cell), Paragraph("Início formal da persecução penal.", table_cell)],
        [Paragraph("2019 - 2024", table_cell), Paragraph("Guapimirim - 2ª Vara", table_cell), Paragraph("Suspensão do processo (Art. 366 do CPP)", table_cell), Paragraph("Período foragido / prazo suspenso.", table_cell)],
        [Paragraph("01/04/2024", table_cell), Paragraph("Guapimirim - 2ª Vara", table_cell), Paragraph("Cumprimento do Mandado de Prisão", table_cell), Paragraph("Prisão cautelar efetivada e retomada do feito.", table_cell)],
        [Paragraph("26/11/2024", table_cell), Paragraph("Guapimirim - 2ª Vara", table_cell), Paragraph("Decisão de Pronúncia ao Júri", table_cell), Paragraph("Juiz submete o réu a julgamento popular.", table_cell)],
        [Paragraph("22/05/2025", table_cell), Paragraph("TJRJ - 2ª Instância", table_cell), Paragraph("RESE julgado pela Desª Márcia Perrini Bodart", table_cell), Paragraph("Negado provimento ao recurso da defesa.", table_cell)],
        [Paragraph("18/05/2026", table_cell), Paragraph("Tribunal do Júri", table_cell), Paragraph("Sessão Plenária de Julgamento (13h às 21h03)", table_cell), Paragraph("Condenação a 13 anos e 4 meses (regime fechado).", table_cell)],
        [Paragraph("19/05/2026", table_cell), Paragraph("Guapimirim - 2ª Vara", table_cell), Paragraph("Interposição da Apelação Criminal", table_cell), Paragraph("Defesa impugna a condenação tempestivamente.", table_cell)],
        [Paragraph("10/06/2026", table_cell), Paragraph("MPRJ - Guapimirim", table_cell), Paragraph("Contrarrazões do Ministério Público (Index 1743)", table_cell), Paragraph("Promotora pede manutenção da condenação.", table_cell)],
        [Paragraph("15/06/2026", table_cell), Paragraph("TJRJ / 2ª Instância", table_cell), Paragraph("Remessa em Grau de Recurso (Cód. 123)", table_cell), Paragraph("Autos chegam ao TJRJ para julgamento colegiado.", table_cell)]
    ]
    timeline_table = Table(timeline_data, colWidths=[65, 110, 195, 145])
    timeline_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2B6CB0')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#FFFFFF')),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#F7FAFC')),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor('#FFFFFF')),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor('#F7FAFC')),
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor('#FFFFFF')),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor('#F7FAFC')),
        ('BACKGROUND', (0,7), (-1,7), colors.HexColor('#FFFFFF')),
        ('BACKGROUND', (0,8), (-1,8), colors.HexColor('#F7FAFC')),
        ('BACKGROUND', (0,9), (-1,9), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(timeline_table)
    story.append(Spacer(1, 10))

    # SEÇÃO 5: PLANO DE AÇÃO IMEDIATO
    story.append(Paragraph("5. PLANO DE AÇÃO IMEDIATO DA DEFESA TÉCNICA", h1_style))
    story.append(Paragraph(
        "A estratégia delineada pela banca para os próximos passos no Tribunal de Justiça do Estado do Rio de Janeiro é composta por 3 etapas sequenciais:",
        body_style
    ))
    story.append(Paragraph(
        "<b>Etapa 1 — Monitoramento de Distribuição no TJRJ:</b><br/>"
        "Acompanhar o sorteio da Câmara Criminal e a designação do Desembargador Relator no TJRJ para onde foram remetidos os autos em 15/06/2026.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Etapa 2 — Memoriais de Despacho com o Relator:</b><br/>"
        "Confecção e protocolo de Memorial sucinto e de alto impacto técnico para ser despachado diretamente no gabinete do Desembargador Relator, com ênfase absoluta na descaracterização do motivo fútil (jurisprudência STJ) e aplicação inadiável da detração na sentença (Art. 387, § 2º, CPP).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Etapa 3 — Sustentação Oral em Plenário no TJRJ:</b><br/>"
        "Inscrição para sustentação oral no dia do julgamento da Apelação para demonstrar aos Desembargadores que a confissão expressa do Ministério Público sobre desavença anterior impede a manutenção da qualificadora e impõe a reforma da dosimetria para regime prisional semiaberto.",
        body_style
    ))
    story.append(Spacer(1, 12))

    # Assinatura institucional
    sign_data = [
        [Paragraph("<b>DEFESA TÉCNICA CONSTITUÍDA</b><br/>Comarca de Guapimirim / TJRJ<br/><i>Patrocínio Processual Ativo</i>", table_cell),
         Paragraph("<b>SUPERJUS INTELIGÊNCIA JURÍDICA</b><br/>Auditoria e Compliance Processual Criminal<br/><i>Emissão: Setembro/2026</i>", table_cell)]
    ]
    sign_table = Table(sign_data, colWidths=[255, 260])
    sign_table.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,-1), 1, colors.HexColor('#1A365D')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
    ]))
    story.append(sign_table)

    # Build PDF with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] PDF gerado em: {pdf_client_path}")

    # Copiar para Desktop e Brain
    shutil.copyfile(pdf_client_path, desktop_path)
    print(f"[OK] PDF copiado para Desktop: {desktop_path}")
    
    shutil.copyfile(pdf_client_path, pdf_brain_path)
    print(f"[OK] PDF copiado para Brain Artifacts: {pdf_brain_path}")

if __name__ == "__main__":
    build_pdf()
