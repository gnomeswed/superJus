# Arquitetura de Servidores MCP no Windows (SuperJus Standard)

Esta regra técnica estabelece o padrão arquitetural obrigatório para desenvolvimento, configuração e execução de servidores MCP no ambiente Windows do SuperJus.

## 1. Framework Obrigatório: FastMCP
- Todo novo servidor MCP local deve ser implementado utilizando o **`FastMCP`** (`from fastmcp import FastMCP`).
- **Motivação:** O SDK de baixo nível `mcp` (especialmente versões <= 1.6.0) não possui tratamento para métodos modernos de probing como `server/discover`, gerando exceções do Pydantic (`ValidationError`), fechamento abrupto de pipe e o erro `connection closed: EOF` no cliente. O `FastMCP` gerencia todo o ciclo de vida sem falhas.

## 2. Interpretador Python Oficial (Global)
- No arquivo `~/.gemini/config/mcp_config.json`, utilize SEMPRE o Python global do sistema:
  `"command": "C:/Users/Administrator/AppData/Local/Programs/Python/Python312/python.exe"`
- **Proibição:** NUNCA configure shims de ambientes virtuais (`.venv/Scripts/python.exe`) ou comandos envoltos em `uv run` como executáveis diretos no `mcp_config.json`. No Windows, esses wrappers geram deadlocks de subprocesso, falhas de pipe stdio e encerramento com `exit status 0xffffffff`.

## 3. Configuração Mandatória de I/O
- No início de qualquer script de servidor MCP Python, inclua expressamente:
  ```python
  import sys
  sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
  ```
- No bloco `env` do `mcp_config.json`, configure sempre:
  ```json
  "env": {
    "PYTHONIOENCODING": "utf-8"
  }
  ```
