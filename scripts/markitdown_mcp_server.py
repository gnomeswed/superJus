# -*- coding: utf-8 -*-
"""
SUPERJUS — MARKITDOWN MCP SERVER
Servidor MCP para conversão de documentos jurídicos (PDF, DOCX, XLSX, áudios) em Markdown estruturado.
Utiliza Microsoft MarkItDown e FastMCP.
"""

import os
import sys
from pathlib import Path
from fastmcp import FastMCP
from markitdown import MarkItDown

sys.stdout.reconfigure(encoding="utf-8")

# Inicializa FastMCP
mcp = FastMCP(
    name="SuperJus Document Intelligence (MarkItDown)",
    instructions=(
        "Servidor MCP do SuperJus para processamento e ingestão de documentos jurídicos. "
        "Converte PDFs de processos, inquéritos policiais, denúncias, decisões judiciais "
        "e planilhas de interceptações telefônicas em Markdown estruturado e limpo."
    )
)

md = MarkItDown()

@mcp.tool()
def convert_to_markdown(file_path: str) -> str:
    """Converte um documento jurídico (PDF, DOCX, XLSX, HTML, áudio) em texto formatado em Markdown.
    
    Args:
        file_path: Caminho absoluto para o arquivo que deve ser convertido.
    
    Returns:
        O conteúdo integral do documento convertido em Markdown limpo.
    """
    p = Path(file_path)
    if not p.exists():
        return f"Erro: Arquivo '{file_path}' não foi encontrado."
    
    try:
        result = md.convert(str(p))
        return result.text_content
    except Exception as e:
        return f"Erro ao converter documento com MarkItDown: {str(e)}"

@mcp.tool()
def convert_and_save_markdown(file_path: str, output_path: str = "") -> str:
    """Converte um arquivo para Markdown e salva no disco.
    
    Args:
        file_path: Caminho absoluto do arquivo original.
        output_path: (Opcional) Caminho absoluto do arquivo .md de saída. Se omitido, salva ao lado com extensão .md.
    
    Returns:
        Status do salvamento e primeiros 500 caracteres do conteúdo gerado.
    """
    p = Path(file_path)
    if not p.exists():
        return f"Erro: Arquivo '{file_path}' não foi encontrado."
    
    if not output_path:
        output_path = str(p.with_suffix(".md"))
    
    try:
        result = md.convert(str(p))
        content = result.text_content
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Sucesso! Arquivo salvo em: {output_path} (Tamanho: {len(content)} caracteres).\nPrévia:\n{content[:500]}..."
    except Exception as e:
        return f"Erro ao converter e salvar: {str(e)}"

if __name__ == "__main__":
    mcp.run()
