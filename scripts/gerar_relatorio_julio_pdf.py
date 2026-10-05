# -*- coding: utf-8 -*-
import sys, os
sys.stdout.reconfigure(encoding="utf-8")
from fpdf import FPDF

def safe(t):
    """Replace non-latin1 chars for Helvetica built-in font."""
    return t.replace('\u2014','-').replace('\u2013','-').replace('\u2018',"'").replace('\u2019',"'").replace('\u201c','"').replace('\u201d','"').replace('\u2022','>')

class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "Julio Pereira Marcos - Relatorio Processual 08/08/2026", align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}}", align="C")

    def title_h1(self, txt):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(26, 54, 93)
        self.multi_cell(0, 10, txt)
        self.set_draw_color(43, 108, 179)
        self.set_line_width(0.6)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def title_h2(self, txt):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(44, 82, 130)
        self.multi_cell(0, 8, txt)
        self.ln(1)

    def body(self, txt):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, safe(txt))
        self.ln(2)

    def quote(self, txt):
        self.set_fill_color(240, 245, 255)
        self.set_draw_color(43, 108, 179)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(50, 50, 50)
        self.set_x(self.l_margin + 3)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 6, 5, safe(txt), fill=True)
        self.ln(3)

    def bullet(self, txt):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.cell(6, 5.5, ">")
        self.multi_cell(self.w - self.l_margin - self.r_margin - 10, 5.5, safe(txt))
        self.ln(1)

    def alert(self, txt):
        self.set_fill_color(255, 243, 224)
        self.set_draw_color(230, 126, 34)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(120, 69, 13)
        self.multi_cell(self.w - self.l_margin - self.r_margin, 5.5, safe(txt), border=1, fill=True)
        self.ln(3)

    def table(self, cols, rows, widths):
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(26, 54, 93)
        self.set_text_color(255, 255, 255)
        for i, c in enumerate(cols):
            self.cell(widths[i], 7, safe(c), border=1, fill=True, align="C")
        self.ln()
        self.set_font("Helvetica", "", 9)
        self.set_text_color(30, 30, 30)
        self.set_fill_color(248, 250, 252)
        for row in rows:
            for i, c in enumerate(row):
                self.cell(widths[i], 6, safe(str(c)), border=1, fill=True)
            self.ln()

pdf = PDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

# ── CAPA ──
pdf.set_font("Helvetica", "B", 28)
pdf.set_text_color(26, 54, 93)
pdf.ln(25)
pdf.cell(0, 15, "RELATORIO PROCESSUAL", align="C")
pdf.ln(20)
pdf.set_font("Helvetica", "", 14)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 10, "Analise baseada em documentos primarios", align="C")
pdf.ln(15)
pdf.set_draw_color(43, 108, 179)
pdf.set_line_width(1)
pdf.line(60, pdf.get_y(), 150, pdf.get_y())
pdf.ln(12)
pdf.set_font("Helvetica", "B", 16)
pdf.set_text_color(30, 30, 30)
pdf.cell(0, 10, "JULIO PEREIRA MARCOS", align="C")
pdf.ln(13)
pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(60, 60, 60)
pdf.cell(0, 7, "Processo n. 0023013-51.2021.8.19.0078", align="C")
pdf.ln(7)
pdf.cell(0, 7, "2a Vara Criminal de Armacao dos Buzios - TJRJ", align="C")
pdf.ln(7)
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(43, 108, 179)
pdf.cell(0, 7, "Art. 33 e 35 - Lei 11.343/06", align="C")
pdf.ln(15)
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 6, "Data: 08 de agosto de 2026", align="C")
pdf.ln(6)
pdf.cell(0, 6, "Classificacao: USO EXCLUSIVO DA DEFESA TECNICA", align="C")
pdf.ln(10)
pdf.set_font("Helvetica", "I", 9)
pdf.set_text_color(130, 130, 130)
pdf.cell(0, 5, "Base documental: Transcricao da Audiencia de Instrucao e Julgamento (1h58min),", align="C")
pdf.ln(5)
pdf.cell(0, 5, "metadados do processo, timeline oficial, HC impetrado, andamentos TJRJ/STJ", align="C")

# ── SEÇÃO 1 ──
pdf.add_page()
pdf.title_h1("1. DOS FATOS - O QUE A AUDIENCIA REVELOU")

pdf.title_h2("1.1 Origem da investigacao")
pdf.body("A investigacao nasceu em marco de 2021, quando policiais militares flagraram Jose Guilherme com aproximadamente 218g de macoha (Del. Rodrigo disse 'cerca de 200g'; Del. Nelson disse '280g' - divergencia relevante). Jose Guilherme alegou consumo proprio e indicou o telefone de quem lhe forneceu a droga.")
pdf.body("O telefone indicado estava cadastrado em nome de Julio Pereira Marcos, mas com endereco ficticio em Sao Paulo. A partir dai, foram decretadas quatro rodadas de interceptacao telefonica.")

pdf.title_h2("1.2 Modelo de atuacao do grupo")
pdf.quote("Del. Rodrigo Moreira: 'Nao havia uma venda explicita nas ruas. Era uma coisa escamoteada, por isso ate que a gente deu o nome de Delivery.' (07:52)")
pdf.quote("Del. Rodrigo: 'Nao foi identificada faccao criminosa. Eles nao ostentavam armas, nao tinham um local fixo, uma boca de fumo.' (20:41-20:59)")
pdf.quote("Del. Nelson Esquiba: 'E uma relacao de usuarios que tambem vendem drogas.' (50:32)")
pdf.quote("Del. Nelson: 'Eles trabalham fora de comunidades carentes, atraves de telefonemas, WhatsApp, entregando na casa das pessoas.' (114:58)")
pdf.body("O grupo operava no centro de Buzios por telefone e WhatsApp, usando codigos velados: 'bulioba' (bagulho ao contrario), 'lacoste verdinha' (macoha), 'arroba' (extase).")

pdf.title_h2("1.3 Papel de Julio na investigacao")
pdf.quote("Del. Nelson Esquiba: 'O Julio tinha conexoes fora de Buzios, entao ele tinha conexoes mais estabilizadas com traficantes de outras localidades.' (41:23)")
pdf.body("Jose Guilherme declarou na delegacia que o fornecedor era o titular do telefone - identificado como Julio.")
pdf.quote("Del. Rodrigo: 'Nao foram apreendidas drogas com eles, mas ficou ali evidenciado que um pedia para o outro negociacao de compra e venda de drogas.' (16:47-16:53)")
pdf.body("Uma interceptacao especifica registrou Julio cobrando R$600 por meio quilo de macoha que Paulo Henrique teria pego para vender e nao pagou.")

pdf.title_h2("1.4 O que NAO existe contra Julio")
pdf.bullet("Nenhuma droga apreendida com Julio - 'Nao foram apreendidas drogas com eles' (Del. Rodrigo, 16:47)")
pdf.bullet("Sem pericia de confronto vocalico - 'Negativo, nao houve' (Del. Rodrigo, 19:31)")
pdf.bullet("Julio e Cristiano nao compareceram a delegacia - bloquearam o WhatsApp do delegado e destruiram o chip")
pdf.bullet("Identificacao por cadastro de operadora + banco Credlink + palavra da mae - sem pericia tecnica ou depoimento pessoal de Julio")

pdf.title_h2("1.5 Sobre a associacao (Art. 35)")
pdf.quote("Del. Nelson Esquiba: 'Todos eles tem aquela estabilidade prevista no artigo 35, mas nao aquela divisao hierarquizada, com subdivisoes, com posicao dentro de uma organizacao que pudesse gerar a tipificacao de crime.' (114:03)")
pdf.quote("Del. Nelson: 'Se eles integram essa faccao de forma enraizada, eu imagino que nao.' (115:25)")

# ── SEÇÃO 2 ──
pdf.add_page()
pdf.title_h1("2. SITUACAO PROCESSUAL ATUAL")
pdf.table(
    ["Processo", "Orgao", "Situacao"],
    [
        ["0023013-51.2021.8.19.0078", "2a Vara Buzios", "Processamento - juntada 04/08"],
        ["0029845-67.2026.8.19.0000", "7a Camara TJRJ", "HC denegado 11/06/2026"],
        ["HC 1.116.750/RJ", "6a Turma STJ", "Liminar indeferida 29/07 - MPF"],
        ["ROC/RHC 2026.141.00580", "STJ", "Autuado e remetido 29/07"],
        ["0022975-39.2021.8.19.0078", "2a Vara Buzios", "Correus soltos desde 02/08/2022"],
    ],
    [52, 55, 83],
)

# ── SEÇÃO 3 ──
pdf.ln(5)
pdf.title_h1("3. DADOS PROCESSUAIS FUNDAMENTAIS")
pdf.table(
    ["Data", "Evento"],
    [
        ("27/01/2022", "Prisao preventiva decretada"),
        ("17/05/2022", "Desmembramento do processo de Julio"),
        ("02/08/2022", "Soltura de TODOS os 5 correus (excesso de prazo)"),
        ("05/05/2026", "HC preventivo impetrado (Julio em liberdade)"),
        ("12/05/2026", "Mandado de prisao cumprido"),
        ("11/06/2026", "HC TJRJ denegado por unanimidade"),
        ("24/07/2026", "Indeferimento fl. 1297 (per relationem)"),
        ("29/07/2026", "ROC remetido ao STJ - HC liminar indeferida"),
        ("31/07/2026", "TJRJ presta informacoes ao STJ (Oficio SEI)"),
        ("04/08/2026", "Juntada de documento na 1a instancia"),
    ],
    [35, 155],
)

# ── SEÇÃO 4 ──
pdf.add_page()
pdf.title_h1("4. PONTOS CRITICOS EXTRAIDOS DOS DOCUMENTOS PRIMARIOS")

pdf.title_h2("4.1 Divergencia de quantidade de droga")
pdf.body("Del. Rodrigo: 'cerca de 200 gramas de macoha' (15:55). Del. Nelson: 'algo em torno de 280 gramas' (36:47). A segunda diligencia produziu quantidade 'muito pequena' tipificada como Art. 28 (uso). Nenhuma quantidade foi apreendida com Julio.")

pdf.title_h2("4.2 Fragilidade da autoria de Julio")
pdf.bullet("Linha telefonica cadastrada em nome de Julio (confirmado pela operadora)")
pdf.bullet("Mae confirmou a titularidade - nao Julio pessoalmente")
pdf.bullet("Sem confronto vocalico - 'Negativo, nao houve' (Del. Rodrigo, 19:31)")
pdf.bullet("Julio nunca prestou depoimento na delegacia - bloqueou o delegado no WhatsApp")
pdf.bullet("Identificacao por cadastro de operadora, banco Credlink e palavra da mae - sem prova tecnica direta")

pdf.title_h2("4.3 Julio destruiu o chip durante a investigacao")
pdf.quote("Del. Nelson: 'O Julio extinguiu aquela linha, parou de usar aquela linha, porque eu falei que era da policia.' (843-844)")
pdf.body("Isso indica que as rodadas finais de interceptacao (3a e 4a, conduzidas por Del. Nelson) ja nao captaram a linha de Julio.")

pdf.title_h2("4.4 Origem do mandado e HC preventivo")
pdf.body("O mandado de prisao de Julio nao constava do BNMP nos primeiros anos. Uma certidao de 07/10/2024 corrigiu essa falha. Julio impetrou HC preventivo em 05/05/2026 - sete dias antes de ter o mandado cumprido em 12/05/2026, o que e incompativel com a condicao de 'foragido' que o MP utilizou.")

pdf.title_h2("4.5 Os 5 correus estao soltos; Julio e o unico preso")
pdf.body("A audiencia foi realizada com apenas Paulo Henrique presente. Os demais correus (Jose Guilherme, Cristiano, Emerson, Juliano Lucas) ja respondem em liberdade - inclusive Jose Guilherme, que foi flagrado com a droga.")

# ── SEÇÃO 5 ──
pdf.add_page()
pdf.title_h1("5. TESES QUE EMERGEM DOS DOCUMENTOS PRIMARIOS")

pdf.title_h2("Tese 1 - Falta de contemporaneidade")
pdf.body("Os fatos investigados datam de marco a setembro de 2021. Julio foi preso em 12/05/2026 - cinco anos depois. Nao ha nos autos qualquer indicio de atividade criminosa entre 2022 e 2026. A prisao preventiva exige perigo atual (Art. 312, par. 2, CPP).")

pdf.title_h2("Tese 2 - Isonomia com os correus soltos (Art. 580, CPP)")
pdf.body("Todos os 5 correus do processo principal foram libertos em 02/08/2022 por excesso de prazo, incluindo Jose Guilherme (flagrado com droga). O desmembramento nao pode justificar a manutencao de Julio como unico preso.")

pdf.title_h2("Tese 3 - Nulidade da decisao per relationem (fl. 1297)")
pdf.body("O Juiz adotou o parecer do MP como 'integral razao de decidir' sem enfrentar nenhuma tese defensiva. O Art. 315, par. 2, V, CPP (Pacote Anticrime) proibe expressamente essa pratica.")

pdf.title_h2("Tese 4 - Descaracterizacao da associacao (Art. 35)")
pdf.body("O proprio Delegado Nelson Esquiba - que conduziu a investigacao - descreveu o grupo como 'usuarios que tambem vendem drogas', sem hierarquia, sem organizacao, sem vinculo enraizado com faccao. Nao se enquadra no tipo do Art. 35.")

pdf.title_h2("Tese 5 - Fragilidade da autoria e materialidade")
pdf.body("Sem droga apreendida, sem pericia vocalica, sem depoimento pessoal, com destruicao do chip antes das rodadas finais - a prova contra Julio e indireta e baseada em cadastro de operadora e palavra de terceiros.")

# ── SEÇÃO 6 ──
pdf.add_page()
pdf.title_h1("6. ALERTAS TATICOS")

pdf.alert("NAO contestar a autoria das interceptacoes em termos absolutos - a linha era cadastrada em nome de Julio e a mae confirmou. A tese e fragilidade da prova, nao negacao.")
pdf.alert("Corrigir referencia a 'cocaina' em documentos internos - a droga apreendida era macoha.")
pdf.alert("Verificar jurisprudencia citada nos autos antes de novo protocolo - confirmar numeros de HCs no portal do STJ (scon.stj.jus.br).")
pdf.alert("Juntar prova emprestada - depoimentos devastadores dos delegados foram no processo principal (0022975-39.2021); podem nao estar nos autos desmembrados.")

pdf.ln(5)
pdf.set_font("Helvetica", "I", 9)
pdf.set_text_color(130, 130, 130)
pdf.multi_cell(0, 5, "Fontes: transcricao da audiencia (1h58min), case_meta.json, timeline.json, analise_ia.json, Habeas_Corpus.md, CATALOGO_INDEX_PROCESSO.md, andamentos TJRJ/STJ verificados em 08/08/2026.")

out = os.path.join("Clientes", "Julio_Pereira_Marcos", "Caso_Principal", "analises", "Relatorio_Processual_Julio_08_08_2026.pdf")
os.makedirs(os.path.dirname(out), exist_ok=True)
pdf.output(out)
print(f"PDF gerado: {os.path.abspath(out)}")
