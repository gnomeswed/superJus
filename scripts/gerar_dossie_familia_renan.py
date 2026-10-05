# -*- coding: utf-8 -*-
import sys
import os
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
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
        # Top Header
        self.setStrokeColor(colors.HexColor('#2B6CB0'))
        self.setLineWidth(1.0)
        self.line(36, 804, 559, 804)
        
        self.setFont('Helvetica-Bold', 8)
        self.setFillColor(colors.HexColor('#1A365D'))
        self.drawString(36, 810, 'ADVOCACIA CRIMINAL ESTRATÉGICA — SUPERJUS')
        
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#718096'))
        self.drawRightString(559, 810, 'RELATÓRIO INFORMATIVO PARA A FAMÍLIA')

        # Bottom Footer
        self.setStrokeColor(colors.HexColor('#CBD5E0'))
        self.setLineWidth(0.6)
        self.line(36, 36, 559, 36)
        
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#718096'))
        self.drawString(36, 24, 'Caso Renan Rodrigues de Souza — Documento Pessoal e Confidencial da Família')
        
        page_str = f'Página {self._pageNumber} de {page_count}'
        self.drawRightString(559, 24, page_str)
        self.restoreState()

def build_pdf(output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'MainTitle',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#1A365D'),
        alignment=TA_CENTER,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'SubTitle',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#2B6CB0'),
        alignment=TA_CENTER,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Heading1',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1A365D'),
        spaceBefore=12,
        spaceAfter=4
    )

    h2_style = ParagraphStyle(
        'Heading2',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#2B6CB0'),
        spaceBefore=8,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor('#2D3748'),
        alignment=TA_JUSTIFY,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#2D3748'),
        leftIndent=14,
        spaceAfter=3
    )

    card_title_style = ParagraphStyle(
        'CardTitle',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#22543D'),
        spaceAfter=3
    )

    card_text_style = ParagraphStyle(
        'CardText',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#234E52')
    )

    th_style = ParagraphStyle(
        'TH',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=TA_CENTER
    )

    td_style = ParagraphStyle(
        'TD',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#2D3748')
    )

    td_bold_style = ParagraphStyle(
        'TDBold',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1A365D')
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph('RELATÓRIO INFORMATIVO PARA A FAMÍLIA', title_style))
    story.append(Paragraph('ACOMPANHAMENTO PROCESSUAL E SITUAÇÃO PRISIONAL DE RENAN RODRIGUES DE SOUZA', subtitle_style))
    story.append(HRFlowable(width='100%', thickness=1.5, color=colors.HexColor('#2B6CB0'), spaceBefore=2, spaceAfter=8))

    # Header Card with Meta Info
    meta_data = [
        [
            Paragraph('<b>Cliente:</b> Renan Rodrigues de Souza', td_style),
            Paragraph('<b>CPF:</b> 198.249.487-59', td_style)
        ],
        [
            Paragraph('<b>Mãe:</b> Lenir Rodrigues Neto', td_style),
            Paragraph('<b>Data do Relatório:</b> 01 de Outubro de 2026', td_style)
        ],
        [
            Paragraph('<b>Processo da Execução (VEP):</b> 5014830-25.2026.8.19.0500', td_style),
            Paragraph('<b>Processo de Origem:</b> 0821248-17.2025.8.19.0031 (Maricá)', td_style)
        ],
        [
            Paragraph('<b>Juízo Competente:</b> Vara de Execuções Penais da Capital (RJ)', td_style),
            Paragraph('<b>Situação Atual:</b> <font color="#22543D"><b>ALVARÁ DE SOLTURA EXPEDIDO / PRISÃO DOMICILIAR</b></font>', td_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[260, 263])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    # Big Green Alert Box: A Grande Vitória
    alert_victory = [
        [Paragraph('<b>BOA NOTÍCIA: A LIBERDADE DE RENAN JÁ FOI DEFERIDA PELA JUSTIÇA!</b>', card_title_style)],
        [Paragraph(
            '<b>O Renan NÃO vai continuar preso em regime fechado e NÃO vai para presídio de semiaberto.</b> '
            'A Juíza da Vara de Execuções Penais (Dra. Larissa Duarte) já concedeu formalmente a <b>PROGRESSÃO PARA PRISÃO DOMICILIAR COM TORNOZELEIRA ELETRÔNICA</b> e o '
            '<b>Alvará de Soltura foi expedido no sistema nacional (BNMP) pelo Juiz Dr. Rafael Estrela Nóbrega</b>. '
            'A pendência que atrasou a saída dele na semana passada foi <b>declarada nula pela Juíza na noite de ontem (30/09)</b>, que determinou a liberação sem novas exigências policiais.',
            card_text_style
        )]
    ]
    t_victory = Table(alert_victory, colWidths=[523])
    t_victory.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0FFF4')),
        ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor('#38A169')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_victory)
    story.append(Spacer(1, 8))

    # Section 1: O que aconteceu e por que ele ainda não pisou na rua?
    story.append(Paragraph('1. RESUMO DA SITUAÇÃO: POR QUE ELE AINDA NÃO PISOU NA RUA?', h1_style))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#CBD5E0'), spaceBefore=1, spaceAfter=4))
    story.append(Paragraph(
        'Muitas famílias ficam angustiadas quando ouvem que a soltura foi deferida, mas o parente continua aguardando no presídio. '
        'Para que tudo fique absolutamente transparente, explicamos exatamente o trâmite que ocorreu nos autos da Execução nº <b>5014830-25.2026.8.19.0500</b>:',
        body_style
    ))
    story.append(Paragraph('• <b>No dia 22/09/2026:</b> A Juíza Dra. Larissa Duarte analisou o bom comportamento de Renan e o tempo de prisão já cumprido e <b>DEFERIU a progressão para Prisão Domiciliar com tornozeleira</b>.', bullet_style))
    story.append(Paragraph('• <b>No dia 24/09/2026 (às 13h10):</b> O Juiz Dr. Rafael Estrela Nóbrega <b>ASSINOU O ALVARÁ DE SOLTURA</b> no Banco Nacional de Medidas Penais (BNMP3).', bullet_style))
    story.append(Paragraph('• <b>No dia 25/09/2026 (O Travamento Burocrático):</b> Quando o alvará chegou para cumprimento, o cartório da VEP identificou no sistema da Polinter uma anotação antiga de 2021 (a ideia de que ele teria deixado de assinar no passado). O cartório lançou uma certidão de "Benefício Prejudicado" e segurou a saída dele provisoriamente.', bullet_style))
    story.append(Paragraph('• <b>Ontem, 30/09/2026 (às 23h49 — A Solução Definitiva):</b> A Juíza analisou pessoalmente o processo antigo e proferiu decisão histórica: constatou que <b>a pena antiga de 2021 já estava extinta e com alvará expedido</b>. A Juíza declarou a <b>INVALIDADE do impedimento</b> e ordenou expressamente que o benefício seja cumprido imediatamente, <b>independentemente de nova consulta à polícia</b>.', bullet_style))

    # Section 2: E a pena do furto da empresa de PVC em Maricá?
    story.append(Spacer(1, 4))
    story.append(Paragraph('2. COMO FICA A PENA DO PROCESSO DE MARICÁ (EMPRESA DE PVC)?', h1_style))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#CBD5E0'), spaceBefore=1, spaceAfter=4))
    story.append(Paragraph(
        'Uma dúvida comum da família é: <i>"Se ele foi condenado a 2 anos pelo furto em Maricá, ele já pagou essa pena?"</i> '
        'A resposta é muito positiva: <b>Renan já cumpriu quase metade da pena em regime fechado, e todo o restante será cumprido em liberdade domiciliar</b>.',
        body_style
    ))

    t_calc_data = [
        [Paragraph('PARÂMETRO', th_style), Paragraph('DETALHAMENTO', th_style), Paragraph('IMPACTO NA SITUAÇÃO DE RENAN', th_style)],
        [
            Paragraph('<b>Pena Total da Condenação</b>', td_bold_style),
            Paragraph('02 anos de reclusão (24 meses / 730 dias)', td_style),
            Paragraph('Pena máxima fixada na sentença da Comarca de Maricá.', td_style)
        ],
        [
            Paragraph('<b>Tempo Já Cumprido Preso</b>', td_bold_style),
            Paragraph('10 meses e 01 dia (306 dias ininterruptos)', td_style),
            Paragraph('<b>Mais de 41,9% da pena já foi paga</b> em regime fechado (desde 30/11/2025).', td_style)
        ],
        [
            Paragraph('<b>Saldo Remanescente</b>', td_bold_style),
            Paragraph('01 ano e 02 meses (aprox. 424 dias)', td_style),
            Paragraph('<b>NÃO SERÁ CUMPRIDO EM PRESÍDIO!</b> Será cumprido em casa, com tornozeleira.', td_style)
        ],
        [
            Paragraph('<b>Data do Livramento Condicional</b>', td_bold_style),
            Paragraph('<b>30 de Novembro de 2026 (DAQUI A 2 MESES)</b>', td_style),
            Paragraph('Completando 1 ano (metade da pena), a defesa já poderá requerer a <b>retirada definitiva da tornozeleira</b>!', td_style)
        ]
    ]
    t_calc = Table(t_calc_data, colWidths=[130, 160, 233])
    t_calc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2B6CB0')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F7FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_calc)
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '<i>Nota Adicional:</i> A defesa também interpôs recurso de Apelação no Tribunal de Justiça (TJRJ) visando desclassificar o crime para furto simples, '
        'o que pode reduzir a pena para 1 ano. Caso esse recurso seja provido, a pena será considerada integralmente extinta.',
        body_style
    ))

    # Section 3: Próximos Passos e Prazos
    story.append(Spacer(1, 4))
    story.append(Paragraph('3. PRÓXIMOS PASSOS E ESTIMATIVA DE LIBERAÇÃO', h1_style))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#CBD5E0'), spaceBefore=1, spaceAfter=4))
    story.append(Paragraph(
        'Agora que a Juíza destravou o processo e dispensou a burocracia da Polinter, as etapas práticas são as seguintes:',
        body_style
    ))
    story.append(Paragraph('1. <b>Cumprimento da Ordem pelo Cartório da VEP:</b> A secretaria da Vara de Execuções Penais certifica o cumprimento do despacho de 30/09 e comunica a SEAP (Secretaria de Administração Penitenciária).', bullet_style))
    story.append(Paragraph('2. <b>Instalação da Tornozeleira Eletrônica:</b> A Central de Monitoramento Eletrônico da SEAP agenda ou realiza a colocação do equipamento no custodiado.', bullet_style))
    story.append(Paragraph('3. <b>Assinatura do Termo de Compromisso e Liberação:</b> Renan assina o termo com as regras da prisão domiciliar e é colocado em liberdade para voltar para casa.', bullet_style))
    story.append(Paragraph('• <b>Atuação da Defesa:</b> Nossa equipe está mantendo contato direto com o Cartório Final RG 1 e 2 da VEP para cobrar agilidade na transmissão da certidão para a SEAP, evitando demoras burocráticas.', bullet_style))

    # Section 4: Guia de Regras de Ouro para a Família e Renan
    story.append(Spacer(1, 4))
    box_rules = [
        [Paragraph('<b>GUIA DE REGRAS DE OURO — O QUE RENAN E A FAMÍLIA DEVEM CUMPRIR RIGOROSAMENTE</b>', ParagraphStyle('AlertTitle', parent=card_title_style, textColor=colors.HexColor('#744210')))],
        [Paragraph(
            'Para que Renan desfrute de sua liberdade com tranquilidade e <b>nunca mais corra risco de voltar para a prisão</b>, '
            'é indispensável que toda a família o ajude a cumprir estas 5 regras inegociáveis:<br/><br/>'
            '<b>1. Carga Diária da Tornozeleira:</b> O aparelho deve ser carregado todos os dias na tomada, sem deixar descarregar. A bateria descarregada é interpretada pelo sistema como fuga e pode gerar mandado de prisão imediato.<br/>'
            '<b>2. Respeitar o Perímetro de Casa:</b> Ele não pode sair da área autorizada pela Justiça (especialmente no período noturno e aos finais de semana), salvo se tiver autorização judicial prévia para trabalho ou estudo.<br/>'
            '<b>3. Não Danificar ou Tentar Romper o Aparelho:</b> Qualquer tentativa de violação física aciona alerta automático via satélite na central da SEAP.<br/>'
            '<b>4. Endereço Sempre Atualizado:</b> Qualquer mudança de residência deve ser comunicada previamente ao advogado para que seja peticionada e autorizada pelo Juiz.<br/>'
            '<b>5. Comparecimento ao Fórum:</b> Cumprir todas as datas de comparecimento periódico que a Justiça determinar para assinar o termo de fiscalização.',
            ParagraphStyle('AlertBody', parent=card_text_style, textColor=colors.HexColor('#744210'), leading=12)
        )]
    ]
    t_rules = Table(box_rules, colWidths=[523])
    t_rules.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFAF0')),
        ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor('#DD6B20')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_rules)
    story.append(Spacer(1, 8))

    # Final Message
    story.append(Paragraph('<b>MENSAGEM DE APOIO DA DEFESA TÉCNICA:</b>', h2_style))
    story.append(Paragraph(
        'A etapa mais severa — o período de 10 meses em regime fechado e a incerteza jurídica da condenação — foi superada com êxito. '
        'A conquista da prisão domiciliar é a oportunidade concreta para que Renan retorne ao seio familiar, retome o trabalho e '
        'reconstrua sua vida com serenidade e dignidade. Permanecemos firmes no acompanhamento diário até o cumprimento total de sua liberdade.',
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f'PDF gerado com sucesso em: {output_pdf_path}')

if __name__ == '__main__':
    desktop_dir = r'C:\Users\Administrator\Desktop'
    desktop_pdf = os.path.join(desktop_dir, 'Dossie_Familia_Renan_Rodrigues.pdf')
    client_dir = r'C:\Projetos\superJus\Clientes\Renan'
    client_pdf = os.path.join(client_dir, 'Dossie_Familia_Renan_Rodrigues.pdf')

    build_pdf(desktop_pdf)
    shutil.copy(desktop_pdf, client_pdf)
    print(f'Copia de seguranca salva em: {client_pdf}')
