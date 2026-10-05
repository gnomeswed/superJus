# -*- coding: utf-8 -*-
"""
Gerador de Relatório Executivo Profissional em PDF — Daniel Ferreira Lima (AUDITADO E SEM ALUCINAÇÃO)
Audiência: Família e Advogados de Defesa
Caso: Apelação Criminal nº 0004301-33.2018.8.19.0073 (4ª Câmara Criminal TJRJ)
"""
import os
import sys
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas

sys.stdout.reconfigure(encoding="utf-8")

client_dir = r"C:\Projetos\superJus\Clientes\Daniel_Ferreira_Lima\04_Analises_e_Estrategias"
os.makedirs(client_dir, exist_ok=True)
pdf_client_path = os.path.join(client_dir, "Relatorio_Julgamento_Apelacao_Daniel_Ferreira_Lima.pdf")
desktop_path = r"C:\Users\Administrator\Desktop\Relatorio_Julgamento_Apelacao_Daniel_Ferreira_Lima.pdf"
brain_dir = r"C:\Users\Administrator\.gemini\antigravity\brain\40a66b95-675e-4702-8a49-f67c7dbd0dad"
os.makedirs(brain_dir, exist_ok=True)
pdf_brain_path = os.path.join(brain_dir, "Relatorio_Julgamento_Apelacao_Daniel_Ferreira_Lima.pdf")

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
        self.line(36, 804, 559, 804)
        self.setFont('Helvetica-Bold', 7.5)
        self.setFillColor(colors.HexColor('#1A365D'))
        self.drawString(36, 810, 'SUPERJUS INTELIGÊNCIA JURÍDICA — RELATÓRIO PROCESSUAL DE ACÓRDÃO')
        self.setFont('Helvetica', 7.5)
        self.setFillColor(colors.HexColor('#4A5568'))
        self.drawRightString(559, 810, 'Cliente: Daniel Ferreira Lima | TJRJ 4ª Câm. Crim.')
        
        # Bottom rule and footer
        self.setStrokeColor(colors.HexColor('#CBD5E0'))
        self.setLineWidth(0.6)
        self.line(36, 36, 559, 36)
        self.setFont('Helvetica', 7.5)
        self.setFillColor(colors.HexColor('#718096'))
        self.drawString(36, 25, 'Documento de Compliance Jurídico e Estratégia Recursal — Uso da Família e Defesa')
        page_str = f'Página {self._pageNumber} de {page_count}'
        self.drawRightString(559, 25, page_str)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        pdf_client_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )
    
    styles = getSampleStyleSheet()
    
    # Custom palette
    c_primary = colors.HexColor('#1A365D')    # Azul Marinho
    c_secondary = colors.HexColor('#2B6CB0')  # Azul Real
    c_text = colors.HexColor('#2D3748')       # Cinza Escuro Texto
    c_red = colors.HexColor('#C53030')        # Vermelho Alerta
    c_green = colors.HexColor('#276749')      # Verde Sucesso/Estratégia
    c_light_bg = colors.HexColor('#F7FAFC')   # Fundo Tabela
    c_alert_bg = colors.HexColor('#FFF5F5')   # Fundo Alerta
    c_border = colors.HexColor('#E2E8F0')
    
    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=c_primary,
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#4A5568'),
        alignment=TA_CENTER
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_primary,
        spaceBefore=8,
        spaceAfter=3
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=c_secondary,
        spaceBefore=6,
        spaceAfter=2
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_text,
        alignment=TA_JUSTIFY,
        spaceAfter=4
    )

    alert_box_style = ParagraphStyle(
        'AlertBoxText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#742A2A'),
        alignment=TA_JUSTIFY
    )

    family_box_style = ParagraphStyle(
        'FamilyBoxText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor('#22543D'),
        alignment=TA_JUSTIFY
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        alignment=TA_CENTER
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9,
        textColor=c_text,
        alignment=TA_LEFT
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold'
    )

    table_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=table_cell,
        alignment=TA_CENTER
    )

    story = []
    
    # Header Banner
    story.append(Spacer(1, 3))
    story.append(Paragraph("RELATÓRIO FORENSE DE AUDITORIA PROCESSUAL E RECURSAL", title_style))
    story.append(Paragraph("ANÁLISE DO ACÓRDÃO DA APELAÇÃO CRIMINAL Nº 0004301-33.2018.8.19.0073 (TJRJ)", subtitle_style))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=1.2, color=c_primary, spaceBefore=2, spaceAfter=6))
    
    # Tabela de Identificação Processual
    info_data = [
        [
            Paragraph("<b>CLIENTE / APELANTE:</b> Daniel Ferreira Lima", table_cell),
            Paragraph("<b>PROCESSO ORIGINÁRIO:</b> 0004301-33.2018.8.19.0073 (2ª Vara de Guapimirim)", table_cell)
        ],
        [
            Paragraph("<b>ÓRGÃO JULGADOR:</b> TJRJ — 4ª Câmara Criminal", table_cell),
            Paragraph("<b>REGISTRO 2ª INSTÂNCIA:</b> 2026.050.10760", table_cell)
        ],
        [
            Paragraph("<b>RELATORA:</b> Desª Márcia Perrini Bodart", table_cell),
            Paragraph("<b>REVISOR:</b> Des. Luiz Marcio Victor Alves Pereira", table_cell)
        ],
        [
            Paragraph("<b>DATA DA SESSÃO:</b> 24/09/2026 (Presencial)", table_cell),
            Paragraph("<b>PUBLICAÇÃO DO ACÓRDÃO:</b> 28/09/2026 (DJERJ)", table_cell)
        ],
        [
            Paragraph("<b>SITUAÇÃO CAUTELAR:</b> Preso Cautelar desde 14/03/2024", table_cell),
            Paragraph("<b>PENA FIXADA:</b> 13 anos e 4 meses de reclusão (Regime Fechado)", table_cell)
        ]
    ]
    t_info = Table(info_data, colWidths=[260, 263])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EDF2F7')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_info)
    story.append(Spacer(1, 6))
    
    # Box de Alerta Vermelho de Prazos
    alert_content = [
        [
            Paragraph(
                "<b>🚨 ALERTA LEGAL DE PRAZOS RECURSAIS EM CURSO (OUTUBRO/2026):</b><br/>"
                "O Acórdão foi publicado no DJERJ em <b>28/09/2026</b>, com juntada de petição em <b>29/09/2026</b>. "
                "O prazo para <b>Embargos de Declaração é de 2 (dois) dias</b> (Art. 619 do CPP). "
                "O prazo para <b>Recurso Especial ao STJ e Recurso Extraordinário ao STF é de 15 (quinze) dias contínuos/corridos</b>, nos termos do Art. 798 do CPP c/c Art. 994 e 1.003, § 5º, do CPC e Art. 26 da Lei nº 8.038/1990 (inaplicável a contagem em dias úteis no processo penal).",
                alert_box_style
            )
        ]
    ]
    t_alert = Table(alert_content, colWidths=[523])
    t_alert.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_alert_bg),
        ('BOX', (0,0), (-1,-1), 1.2, c_red),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_alert)
    story.append(Spacer(1, 6))

    # SEÇÃO 1: PARA A FAMÍLIA (REALISMO E TRANSPARÊNCIA TOTAL)
    story.append(Paragraph("1. INFORMAÇÃO TRANSPARENTE E REALISTA PARA A FAMÍLIA DE DANIEL", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=1, spaceAfter=4))
    
    fam_intro = [
        [
            Paragraph(
                "<b>À Família de Daniel Ferreira Lima,</b><br/><br/>"
                "Com total transparência e respeito, apresentamos a realidade processual após o julgamento do Tribunal de Justiça do Rio de Janeiro:<br/><br/>"
                "<b>1. O que foi decidido em 24/09/2026?</b> Os desembargadores da 4ª Câmara Criminal decidiram manter a condenação de 13 anos e 4 meses em regime fechado, rejeitando os pedidos de anulação do júri nesta fase estadual.<br/>"
                "<b>2. O processo acabou? Não.</b> O Tribunal de Justiça do Rio de Janeiro encerrou a fase estadual ordinária. A defesa técnica agora levará o caso a Brasília, perante o <b>Superior Tribunal de Justiça (STJ)</b> e o <b>Supremo Tribunal Federal (STF)</b>.<br/>"
                "<b>3. A dura realidade sobre a prisão e a detração penal:</b> Daniel está preso desde 14/03/2024 (cumpriu cerca de 2 anos e meio). A pena restante ainda é de aproximadamente <b>10 anos e 10 meses</b>. Pela lei brasileira (Art. 33 do Código Penal), qualquer pena superior a 8 anos exige regime inicial fechado. Portanto, mesmo abatendo o tempo já cumprido, ele não vai para o semiaberto de imediato apenas pela detração. O objetivo central dos recursos em Brasília será <b>derrubar a qualificadora do motivo fútil ou anular o julgamento</b>, pois somente reduzindo a pena total para patamar inferior a 8 anos será possível alcançar a transferência para o regime semiaberto.<br/>"
                "<b>4. O foco de combate:</b> O Acórdão do Rio cometeu contradições evidentes e erros na dosimetria que serão rigorosamente explorados pelos advogados nas Cortes Superiores.",
                family_box_style
            )
        ]
    ]
    t_fam = Table(fam_intro, colWidths=[523])
    t_fam.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0FFF4')),
        ('BOX', (0,0), (-1,-1), 1, c_green),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_fam)
    story.append(Spacer(1, 7))

    # SEÇÃO 2: RAIO-X FORENSE DO ACÓRDÃO (PARA OS ADVOGADOS)
    story.append(Paragraph("2. AUDITORIA TÉCNICA E FALHAS DO ACÓRDÃO (PARA A BANCA DEFENSIVA)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=1, spaceAfter=4))

    # Ponto 1
    story.append(Paragraph("Ponto 1: Erro Material e Confusão Estrutural na 3ª Fase da Dosimetria (Fls. 16)", h2_style))
    story.append(Paragraph(
        "A Desembargadora Relatora consignou no voto condutor (fls. 16): <i>'Na terceira fase, ausentes causas de diminuição de pena. Apesar do reconhecimento pelo Conselho de Sentença da <b>causa de aumento de pena prevista no art. 121, § 2º, II, do C.Penal</b>, a sentenciante deixou de aplicá-la...'</i>. "
        "O Art. 121, § 2º, II do CP (Motivo Fútil) <b>é qualificadora</b> (que fixa a baliza da pena em abstrato na 1ª fase de 12 a 30 anos) e <b>não majorante de 3ª fase</b>. Trata-se de erro material evidente e confusão dogmática passível de correção via <b>Embargos de Declaração (Art. 619 do CPP)</b> para fins de prequestionamento.",
        body_style
    ))

    # Ponto 2
    story.append(Paragraph("Ponto 2: A Tese do Motivo Fútil e os Limites da Súmula 7 do STJ (Fls. 5 e 12)", h2_style))
    story.append(Paragraph(
        "O acórdão transcreveu a denúncia e reconheceu expressamente a ocorrência de atrito anterior: <i>'aproximadamente 01 (um) mês antes dos fatos, a vítima se desentendeu com o acusado e o corréu, em razão do volume alto do som do veículo'</i> (fls. 5 e 12). "
        "Embora o STJ afirme que discussão prévia nem sempre exclui de plano a futilidade, havendo divergências fáticas apreciadas pelos jurados (Súmula 7/STJ), a defesa técnica demonstrará em Recurso Especial a <b>desproporção na subsunção típica</b>, sustentando que a mola propulsora reconhecida nos autos foi a animosidade pretérita, o que afasta a futilidade imediata.",
        body_style
    ))

    # Ponto 3
    story.append(Paragraph("Ponto 3: Distinção Dogmática entre Motivo Subjetivo e Meio de Execução", h2_style))
    story.append(Paragraph(
        "A violência dos atos de execução (tiros, pauladas e chutes) não convalida o motivo fútil:<br/>"
        "• <b>Meio de Execução vs. Motivo:</b> A brutalidade física diz respeito ao meio executório (que poderia configurar meio cruel - inciso III). O Ministério Público <b>não imputou meio cruel</b> na denúncia nem foi quesitado aos jurados. Não cabe ao Tribunal substituir a qualificadora não imputada sob pena de afronta ao Princípio da Correlação e à Súmula 453 do STF.<br/>"
        "• <b>Bis in Idem:</b> Os atos de agressão já foram valorados para exasperar a pena-base na 1ª fase em 2/6 (fls. 14/15). Utilizá-los para justificar a qualificadora do motivo importaria em dupla punição pelo mesmo fato.",
        body_style
    ))

    # Ponto 4
    story.append(Paragraph("Ponto 4: Detração Penal (Art. 387, § 2º, CPP) e Regime Prisional (Fls. 17)", h2_style))
    story.append(Paragraph(
        "A Câmara rejeitou a aplicação imediata da detração ao fundamento genérico de que <i>'a quantidade de pena não deve ser o único fator (...) cabendo ao Juízo da Execução decidir'</i>. "
        "Embora com o desconto de 2 anos e meio a pena permaneça acima de 8 anos (restando 10a e 10m em regime fechado pelo Art. 33, § 2º, 'a', CP), a recusa pura e simples em motivar a detração concreta viola o comando cogente do Art. 387, § 2º, do CPP c/c Art. 315, § 2º, III, do CPP, devendo ser saneada para fixação precisa dos marcos executórios.",
        body_style
    ))

    # Ponto 5
    story.append(Paragraph("Ponto 5: Controle Judicial do Debate vs. Plenitude de Defesa (Fls. 1 e Fls. 7-8)", h2_style))
    story.append(Paragraph(
        "A Juíza Presidente cerceou a manifestação defensiva sobre a absolvição do corréu Julio Leonam no feito conexo. A Câmara respaldou a juíza com base no controle judicial do debate. Em Recurso Extraordinário perante o STF, a defesa sustentará a violação à <b>Plenitude de Defesa (Art. 5º, XXXVIII, 'a', da CF)</b>, uma vez que a acusação utilizou elementos conexos por prova emprestada (testemunha Jonathan), violando a paridade de armas.",
        body_style
    ))

    story.append(Spacer(1, 6))

    # SEÇÃO 3: CRONOGRAMA DE PRAZOS
    story.append(Paragraph("3. CRONOGRAMA DE PRAZOS RECURSAIS", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=1, spaceAfter=4))
    
    deadlines_data = [
        [
            Paragraph("RECURSO / PEÇA", table_header),
            Paragraph("PRAZO LEGAL", table_header),
            Paragraph("REGIME DE CONTAGEM", table_header),
            Paragraph("FINALIDADE PROCESSUAL", table_header)
        ],
        [
            Paragraph("<b>Embargos de Declaração</b><br/>(Art. 619 do CPP)", table_cell_bold),
            Paragraph("2 dias", table_cell_center),
            Paragraph("Contínuo (Art. 798 CPP)", table_cell_center),
            Paragraph("Sanar erro material da fls. 16 (qualificadora como majorante) e <b>prequestionar expressamente</b> matéria federal e constitucional. <b>Interrompe o prazo para REsp e RE</b>.", table_cell)
        ],
        [
            Paragraph("<b>Recurso Especial (REsp)</b><br/>(Art. 105, III, CF - STJ)", table_cell_bold),
            Paragraph("15 dias corridos", table_cell_center),
            Paragraph("Art. 798 CPP / CPC Art. 1.003", table_cell_center),
            Paragraph("Questionar a subsunção do motivo fútil e a exasperação da pena-base na 1ª fase (Art. 59 do CP), buscando reduzir a pena total para patamar inferior a 8 anos.", table_cell)
        ],
        [
            Paragraph("<b>Recurso Extraordinário (RE)</b><br/>(Art. 102, III, CF - STF)", table_cell_bold),
            Paragraph("15 dias corridos", table_cell_center),
            Paragraph("Art. 798 CPP / CPC Art. 1.003", table_cell_center),
            Paragraph("Nulidade do Júri por cerceamento da Plenitude de Defesa (Art. 5º, XXXVIII, 'a', CF) diante da vedação de menção à absolvição do corréu conexo.", table_cell)
        ]
    ]
    t_deadlines = Table(deadlines_data, colWidths=[100, 65, 80, 278])
    t_deadlines.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('BOX', (0,0), (-1,-1), 0.8, c_secondary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg])
    ]))
    story.append(t_deadlines)
    story.append(Spacer(1, 6))

    # SEÇÃO 4: PLANO DE AÇÃO
    story.append(Paragraph("4. PLANO DE AÇÃO OPERACIONAL DA DEFESA TÉCNICA", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=1, spaceAfter=4))
    
    plan_data = [
        [
            Paragraph("<b>PASSO 1: EMBARGOS DE DECLARAÇÃO (TJRJ)</b><br/>Protocolar os Embargos de Declaração para sanar o erro material da fls. 16, exigir fundamentação sobre a detração e consolidar o prequestionamento legal indispensável para a admissibilidade do REsp e do RE.", table_cell),
            Paragraph("<b>PASSO 2: RECURSO ESPECIAL (STJ)</b><br/>Interpor Recurso Especial perante o STJ com foco na dosimetria da pena (redução da pena-base da 1ª fase e discussão sobre a qualificadora). Se a pena for reduzida para menos de 8 anos, viabiliza-se o regime semiaberto.", table_cell),
            Paragraph("<b>PASSO 3: GESTÃO EXECUTÓRIA PENAL</b><br/>Acompanhar a execução provisória da pena na VEP para garantir que a detração do tempo cumprido (desde 14/03/2024) seja computada para fins de progressão de regime e benefícios da LEP.", table_cell)
        ]
    ]
    t_plan = Table(plan_data, colWidths=[174, 175, 174])
    t_plan.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EDF2F7')),
        ('BOX', (0,0), (-1,-1), 0.8, c_secondary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_plan)
    story.append(Spacer(1, 8))

    # Assinatura Institucional
    story.append(KeepTogether([
        HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#CBD5E0'), spaceBefore=2, spaceAfter=5),
        Paragraph("<b>SUPERJUS — NÚCLEO DE INTELIGÊNCIA PENAL ESTRATÉGICA & TRIBUNAIS SUPERIORES</b>", ParagraphStyle('SignTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=c_primary, alignment=TA_CENTER)),
        Paragraph("Documento de Auditoria e Compliance Recursal — Processo nº 0004301-33.2018.8.19.0073", ParagraphStyle('SignSub', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9, textColor=colors.HexColor('#718096'), alignment=TA_CENTER))
    ]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] PDF Principal Auditado gerado em: {pdf_client_path}")
    
    # Copiar para Desktop e pasta do Brain
    try:
        shutil.copy2(pdf_client_path, desktop_path)
        print(f"[OK] Cópia salva na Área de Trabalho: {desktop_path}")
    except Exception as e:
        print(f"Erro ao copiar para Desktop: {e}")
        
    try:
        shutil.copy2(pdf_client_path, pdf_brain_path)
        print(f"[OK] Cópia salva no Brain Artifacts: {pdf_brain_path}")
    except Exception as e:
        print(f"Erro ao copiar para Brain: {e}")

if __name__ == "__main__":
    build_pdf()
