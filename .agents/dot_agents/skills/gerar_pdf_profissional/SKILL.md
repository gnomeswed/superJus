---
name: Gerar PDF Profissional
description: Converte relatorios em Markdown ou HTML para PDFs com design de altissimo padrao visual, tipografia impecavel, tabelas estilizadas, rodape com numeracao de paginas e suporte nativo a acentos em portugues sem erros.
---

# Diretrizes da Skill: Gerar PDF Profissional

Esta skill foi projetada para criar documentos e relatorios juridicos em formato PDF com acabamento visual impecavel, elegante e corporativo. Ela previne erros de codificacao (acentuacao), paginas em branco, tabelas desalinhadas e quebras de texto inadequadas.

---

## 1. Diretrizes de Design e Layout

Ao converter qualquer relatorio para PDF, o documento resultante DEVE seguir o padrao de identidade visual executiva do Super Analista Juridico:

* Paleta de Cores Primaria:
  * Azul Marinho (Cabecalhos/Titulos): #1A365D (RGB: 26, 54, 93)
  * Azul Real (Destaques/Tabelas): #2B6CB0 (RGB: 43, 108, 176)
  * Cinza Neutro (Texto Principal): #2D3748 (RGB: 45, 55, 72)
  * Fundo Alternado de Tabelas: #F7FAFC (RGB: 247, 250, 252)
  * Linhas Divisorias: #CBD5E0 (RGB: 203, 213, 224)

* Tipografia e Espacamento:
  * Fonte Principal: Helvetica ou Arial
  * Titulo Principal: 16pt, Negrito, Azul Marinho com linha decorativa.
  * Titulos de Secao (H2/H3): 12pt/11pt, Negrito, Azul Real.
  * Corpo de Texto: 9.5pt a 10pt, Entrelinha de 13.5pt, Alinhamento Justificado.
  * Marcadores (Bullets): Indentacao a esquerda de 12pt.

* Tabelas Profissionais:
  * Cabecalho com fundo Azul Real (#2B6CB0) e texto em Branco em negrito.
  * Linhas com fundo zebrado (alternando entre Branco e Cinza Claro #F7FAFC).
  * Bordas sutis em cinza (#CBD5E0).
  * Quebra automatica de texto em todas as celulas (word-wrap).

* Cabecalho e Rodape Automaticos:
  * Cabecalho: Titulo discreto da empresa com barra divisoria.
  * Rodape: Numeracao dinamica de paginas e nota de confidencialidade.

---

## 2. Como Executar a Conversao

Utilize o script de conversao oficial localizado nesta skill:

python c:\Projetos\Super Analista Juridico\.agents\skills\gerar_pdf_profissional\scripts\gerar_pdf_profissional.py c:\caminho\input.md c:\caminho\output.pdf