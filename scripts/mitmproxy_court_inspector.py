# -*- coding: utf-8 -*-
"""
SUPERJUS — INSPETOR DE TRÁFEGO DE TRIBUNAIS (MITMPROXY COURT INSPECTOR)
=======================================================================
Blueprint e Addon para mitmproxy voltado à engenharia reversa de portais judiciais.
Intercepta, filtra, analisa e cataloga requisições REST/XHR e respostas JSON
dos principais sistemas de tribunais brasileiros (TJRJ, STJ, PJe, eproc, DataJud).

Funcionalidades:
  1. Filtra automaticamente domínios judiciais (*.tjrj.jus.br, *.stj.jus.br, *.pje.jus.br,
     comunica.pje.jus.br, *eproc*, *.cnj.jus.br).
  2. Ignora tráfego ruidoso (imagens, scripts estáticos, fontes, CSS).
  3. Extrai cabeçalhos de autenticação e sessão (Cookies, Bearer, CSID, CSRF tokens).
  4. Infere esquemas JSON estruturados (tipos, chaves e campos obrigatórios).
  5. Gera comandos 'curl' prontos para reprodução direta sem navegador.
  6. Documenta endpoints ocultos automaticamente em:
     - c:\\Projetos\\superJus\\docs\\endpoints_tribunais_catalog.json
     - c:\\Projetos\\superJus\\docs\\ENDPOINTS_TRIBUNAIS.md
  7. Modo Standalone / Synthetic Test para testes sem necessidade de tráfego real.
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import urllib
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path("c:/Projetos/superJus")
DOCS_DIR = ROOT_DIR / "docs"
CATALOG_JSON_PATH = DOCS_DIR / "endpoints_tribunais_catalog.json"
CATALOG_MD_PATH = DOCS_DIR / "ENDPOINTS_TRIBUNAIS.md"

# Padrões regex para identificar portais judiciais
COURT_DOMAINS = [
    re.compile(r".*tjrj\.jus\.br.*", re.IGNORECASE),
    re.compile(r".*stj\.jus\.br.*", re.IGNORECASE),
    re.compile(r".*pje\.jus\.br.*", re.IGNORECASE),
    re.compile(r".*comunica\.pje\.jus\.br.*", re.IGNORECASE),
    re.compile(r".*eproc.*", re.IGNORECASE),
    re.compile(r".*trf[1-6]\.jus\.br.*", re.IGNORECASE),
    re.compile(r".*datajud\.cnj\.jus\.br.*", re.IGNORECASE),
    re.compile(r".*tjsp\.jus\.br.*", re.IGNORECASE),
    re.compile(r".*tjmg\.jus\.br.*", re.IGNORECASE),
]

# Extensões ignoradas para focar estritamente em APIs e JSON
IGNORED_EXTENSIONS = {
    ".js", ".css", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg",
    ".woff", ".woff2", ".ttf", ".eot", ".map", ".mp4", ".webp"
}


def infer_schema(data: Any, depth: int = 0) -> Any:
    """Infere tipos recursivamente para gerar o schema do payload JSON."""
    if depth > 5:
        return "any"
    if isinstance(data, dict):
        schema = {}
        for k, v in list(data.items())[:30]:
            schema[k] = infer_schema(v, depth + 1)
        return schema
    elif isinstance(data, list):
        if not data:
            return ["empty_array"]
        sample_types = [infer_schema(item, depth + 1) for item in data[:3]]
        return [sample_types[0]] if sample_types else ["any"]
    elif isinstance(data, bool):
        return "boolean"
    elif isinstance(data, int):
        return "integer"
    elif isinstance(data, float):
        return "float"
    elif isinstance(data, str):
        if len(data) > 60:
            return "string(long)"
        return "string"
    elif data is None:
        return "null"
    return type(data).__name__


def generate_curl(method: str, url: str, headers: Dict[str, str], body: str = "") -> str:
    """Gera um snippet curl formatado e pronto para execução no terminal."""
    lines = [f"curl -X {method} \"{url}\""]
    for k, v in headers.items():
        if k.lower() in ["content-type", "accept", "authorization", "x-csrf-token", "origin", "referer", "cookie"]:
            # Trunca cookies muito longos no comando demonstrativo
            v_clean = v[:150] + "..." if len(v) > 150 and k.lower() == "cookie" else v
            lines.append(f"  -H \"{k}: {v_clean}\"")
    if body and method in ["POST", "PUT", "PATCH"]:
        clean_body = body.replace('"', '\\"').replace("\n", "")
        if len(clean_body) > 300:
            clean_body = clean_body[:300] + "..."
        lines.append(f"  -d \"{clean_body}\"")
    return " \\\n".join(lines)


class CourtTrafficInspector:
    """
    Addon do mitmproxy para auditoria e catalogação automática de APIs de tribunais.
    """

    def __init__(self, output_json: Path = CATALOG_JSON_PATH, output_md: Path = CATALOG_MD_PATH):
        self.output_json = Path(output_json)
        self.output_md = Path(output_md)
        self.catalog: Dict[str, Dict[str, Any]] = self._load_catalog()
        self.captured_count = 0

    def _load_catalog(self) -> Dict[str, Dict[str, Any]]:
        if self.output_json.exists():
            try:
                with open(self.output_json, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_catalog(self):
        self.output_json.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_json, "w", encoding="utf-8") as f:
            json.dump(self.catalog, f, ensure_ascii=False, indent=2)
        self._export_markdown()

    def _is_court_traffic(self, url: str) -> bool:
        parsed_path = url.split("?")[0].lower()
        if any(parsed_path.endswith(ext) for ext in IGNORED_EXTENSIONS):
            return False
        return any(pattern.match(url) for pattern in COURT_DOMAINS)

    def _classify_court(self, url: str) -> str:
        u = url.lower()
        if "tjrj" in u:
            return "TJRJ (Tribunal de Justiça do Rio de Janeiro)"
        if "stj" in u:
            return "STJ (Superior Tribunal de Justiça)"
        if "pje" in u or "comunica" in u:
            return "PJe / PDPJ-Br (Processo Judicial Eletrônico)"
        if "eproc" in u:
            return "eproc (Sistema Processual da Justiça Federal / Estadual)"
        if "datajud" in u:
            return "DataJud (Base Nacional de Dados do CNJ)"
        return "Tribunal Geral"

    def process_http_exchange(
        self,
        method: str,
        url: str,
        request_headers: Dict[str, str],
        request_body: str,
        response_status: int,
        response_headers: Dict[str, str],
        response_body: str,
        duration_ms: float = 0.0
    ):
        """Processa um par request/response e adiciona ao catálogo de endpoints."""
        if not self._is_court_traffic(url):
            return

        court_name = self._classify_court(url)
        parsed_url = urllib.parse.urlparse(url)
        path = parsed_url.path or "/"
        endpoint_key = f"{method.upper()} {parsed_url.netloc}{path}"

        # Parser do Request Body
        req_json = None
        req_schema = None
        if request_body:
            try:
                req_json = json.loads(request_body)
                req_schema = infer_schema(req_json)
            except Exception:
                req_schema = "raw_text_or_form"

        # Parser do Response Body
        resp_json = None
        resp_schema = None
        is_json_response = "json" in response_headers.get("content-type", "").lower() or response_body.strip().startswith(("{", "["))
        if is_json_response and response_body:
            try:
                resp_json = json.loads(response_body)
                resp_schema = infer_schema(resp_json)
            except Exception:
                resp_schema = "unparsed_json"
        elif "html" in response_headers.get("content-type", "").lower():
            resp_schema = "html_document"

        # Cabeçalhos sensíveis/relevantes
        relevant_headers = {}
        for h, v in request_headers.items():
            if h.lower() in ["content-type", "accept", "authorization", "origin", "referer", "cookie", "x-csrf-token", "x-requested-with"]:
                relevant_headers[h] = v

        entry = {
            "endpoint_key": endpoint_key,
            "court": court_name,
            "method": method.upper(),
            "host": parsed_url.netloc,
            "path": path,
            "query_params": dict(urllib.parse.parse_qsl(parsed_url.query)),
            "last_seen": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status_code": response_status,
            "duration_ms": duration_ms,
            "relevant_request_headers": relevant_headers,
            "request_schema": req_schema,
            "request_example": req_json if req_json else (request_body[:200] if request_body else None),
            "response_schema": resp_schema,
            "response_sample_keys": list(resp_json.keys())[:15] if isinstance(resp_json, dict) else None,
            "reproducible_curl": generate_curl(method.upper(), url, request_headers, request_body)
        }

        self.catalog[endpoint_key] = entry
        self.captured_count += 1
        self._save_catalog()

    def _export_markdown(self):
        """Exporta o catálogo como documentação Markdown navegável."""
        now_str = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for entry in self.catalog.values():
            court = entry.get("court", "Outros")
            grouped.setdefault(court, []).append(entry)

        md = [
            "# 🏛️ Catálogo de Endpoints e Engenharia Reversa de Tribunais (SuperJus)",
            "",
            "> Documento gerado automaticamente pelo `mitmproxy_court_inspector.py`.",
            f"> **Última Atualização:** {now_str} | **Total de Endpoints Mapeados:** {len(self.catalog)}",
            "",
            "---",
            "",
            "## 📋 Índice por Tribunal",
            ""
        ]

        for court in sorted(grouped.keys()):
            anchor = court.lower().replace(" ", "-").replace("(", "").replace(")", "").replace("/", "")
            md.append(f"- [{court}](#{anchor}) ({len(grouped[court])} endpoints)")

        md.append("\n---\n")

        for court, entries in sorted(grouped.items()):
            md.append(f"## {court}\n")
            for e in entries:
                md.append(f"### `{e['method']}` `{e['path']}`")
                md.append(f"- **Host:** `https://{e['host']}`")
                md.append(f"- **Status:** `{e['status_code']}` | **Latência:** `{e.get('duration_ms', 0):.1f} ms`")
                if e.get("query_params"):
                    md.append(f"- **Query Parameters:** `{json.dumps(e['query_params'], ensure_ascii=False)}`")
                
                if e.get("request_schema"):
                    md.append("\n**Request Schema:**")
                    md.append("```json")
                    md.append(json.dumps(e["request_schema"], indent=2, ensure_ascii=False))
                    md.append("```")

                if e.get("response_schema"):
                    md.append("\n**Response Schema:**")
                    md.append("```json")
                    md.append(json.dumps(e["response_schema"], indent=2, ensure_ascii=False))
                    md.append("```")

                md.append("\n**Comando cURL Reproduzível:**")
                md.append("```bash")
                md.append(e.get("reproducible_curl", ""))
                md.append("```")
                md.append("\n---\n")

        with open(self.output_md, "w", encoding="utf-8") as f:
            f.write("\n".join(md))


# =============================================================================
# HOOKS NATIVOS DO MITMPROXY (Executados quando roda via `mitmdump -s`)
# =============================================================================
inspector_instance: Optional[CourtTrafficInspector] = None

try:
    from mitmproxy import http

    def load(loader):
        global inspector_instance
        inspector_instance = CourtTrafficInspector()
        print("[MitmproxyCourtInspector] Addon carregado com sucesso. Monitorando tráfego judicial...")

    def response(flow: http.HTTPFlow):
        global inspector_instance
        if inspector_instance is None:
            inspector_instance = CourtTrafficInspector()

        url = flow.request.pretty_url
        if not inspector_instance._is_court_traffic(url):
            return

        method = flow.request.method
        req_headers = dict(flow.request.headers)
        req_body = flow.request.get_text() or ""
        resp_status = flow.response.status_code if flow.response else 0
        resp_headers = dict(flow.response.headers) if flow.response else {}
        resp_body = flow.response.get_text() if flow.response else ""

        duration_ms = 0.0
        if flow.response and flow.response.timestamp_end and flow.request.timestamp_start:
            duration_ms = (flow.response.timestamp_end - flow.request.timestamp_start) * 1000

        inspector_instance.process_http_exchange(
            method=method,
            url=url,
            request_headers=req_headers,
            request_body=req_body,
            response_status=resp_status,
            response_headers=resp_headers,
            response_body=resp_body,
            duration_ms=duration_ms
        )
        print(f"[CAPTURA JUDICIAL] {method} {url[:90]} -> {resp_status} ({duration_ms:.1f}ms)")

except ImportError:
    pass


# =============================================================================
# MODO DE TESTE SINTÉTICO (Validação de catálogo e infraestrutura sem tráfego)
# =============================================================================
def run_synthetic_test():
    """Simula trocas HTTP representativas para validar e popular o catálogo inicial."""
    print("=" * 80)
    print("🧪 SUPERJUS — TESTE SINTÉTICO DO INSPETOR DE TRÁFEGO DE TRIBUNAIS")
    print("=" * 80)

    inspector = CourtTrafficInspector()

    # 1. Endpoint TJRJ /por-numeracao-unica
    inspector.process_http_exchange(
        method="POST",
        url="https://www3.tjrj.jus.br/consultaprocessual/api/processos/por-numeracao-unica",
        request_headers={
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json",
            "Origin": "https://www3.tjrj.jus.br",
            "Referer": "https://www3.tjrj.jus.br/consultaprocessual/"
        },
        request_body=json.dumps({"tipoProcesso": "1", "codigoProcesso": "0023013-51.2021.8.19.0078"}),
        response_status=200,
        response_headers={"Content-Type": "application/json;charset=UTF-8"},
        response_body=json.dumps([{
            "idProcesso": 133666226,
            "numProcesso": "0023013-51.2021.8.19.0078",
            "classe": "Ação Penal de Competência do Júri",
            "descricaoServentia": "1ª Vara de Búzios",
            "ultimoMovimento": "Conclusão ao Juiz",
            "dtUltimoMovimento": "2026-08-20T14:30:00.000Z"
        }]),
        duration_ms=420.5
    )

    # 2. Endpoint TJRJ /movimentos
    inspector.process_http_exchange(
        method="POST",
        url="https://www3.tjrj.jus.br/consultaprocessual/api/processos/por-numero/movimentos",
        request_headers={
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json",
            "Origin": "https://www3.tjrj.jus.br"
        },
        request_body=json.dumps({
            "tipoProcesso": 1,
            "codigoProcesso": "2021.078.023002-1",
            "indProcVolumoso": "N",
            "ultimaOrdemExibida": None
        }),
        response_status=200,
        response_headers={"Content-Type": "application/json;charset=UTF-8"},
        response_body=json.dumps([
            {
                "ordem": 58,
                "dtMovimento": "20/08/2026",
                "dtJuntada": "20/08/2026 14:35",
                "descrMov": "Conclusão ao Juiz",
                "movimentosExibicao": [{"tipoMovimento": "Decisão", "detalhesMovimento": "Autos conclusos para despacho"}]
            }
        ]),
        duration_ms=380.2
    )

    # 3. Endpoint DataJud CNJ STJ
    inspector.process_http_exchange(
        method="POST",
        url="https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search",
        request_headers={
            "Authorization": "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==",
            "Content-Type": "application/json"
        },
        request_body=json.dumps({"query": {"match": {"numeroProcesso": "00298456720268190000"}}, "size": 5}),
        response_status=200,
        response_headers={"Content-Type": "application/json"},
        response_body=json.dumps({
            "hits": {
                "total": {"value": 1},
                "hits": [{
                    "_source": {
                        "numeroProcesso": "00298456720268190000",
                        "classe": {"codigo": 307, "nome": "Habeas Corpus"},
                        "orgaoJulgador": {"codigo": 160, "nome": "6ª Turma"},
                        "nivelSigilo": 0
                    }
                }]
            }
        }),
        duration_ms=640.8
    )

    # 4. Endpoint PJe Comunica (DJEN Nacional)
    inspector.process_http_exchange(
        method="POST",
        url="https://comunica.pje.jus.br/api/v1/comunicacao",
        request_headers={
            "Content-Type": "application/json",
            "Origin": "https://comunica.pje.jus.br"
        },
        request_body=json.dumps({"siglaTribunal": "STJ", "numeroProcesso": "1116750", "meio": "D"}),
        response_status=200,
        response_headers={"Content-Type": "application/json"},
        response_body=json.dumps({
            "status": "success",
            "count": 1,
            "items": [{
                "id": 8941203,
                "data_disponibilizacao": "2026-08-14",
                "tipoComunicacao": "Intimação",
                "destinatario": "GABRIEL ALVES GUIMARAES"
            }]
        }),
        duration_ms=510.0
    )

    print(f"✅ Teste concluído! {inspector.captured_count} endpoints processados.")
    print(f"📁 Catálogo JSON salvo em: {CATALOG_JSON_PATH}")
    print(f"📄 Documentação Markdown gerada em: {CATALOG_MD_PATH}")
    print("=" * 80)


def start_mitmproxy(port: int = 8080):
    """Inicia o mitmdump com o script de inspeção acoplado."""
    script_path = str(Path(__file__).resolve())
    python_312_scripts = Path(r"C:\Users\Administrator\AppData\Local\Programs\Python\Python312\Scripts\mitmdump.exe")
    mitm_cmd = str(python_312_scripts) if python_312_scripts.exists() else "mitmdump"

    cmd = [
        mitm_cmd,
        "-s", script_path,
        "-p", str(port),
        "--set", "block_global=false"
    ]
    print(f"🚀 Iniciando mitmproxy na porta {port}...")
    print(f"Comando: {' '.join(cmd)}")
    print(f"Configure o navegador com Proxy HTTP: 127.0.0.1:{port}")
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n🛑 Servidor mitmproxy encerrado.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SuperJus — Inspetor de Tráfego de Tribunais")
    parser.add_argument("--test-synthetic", action="store_true", help="Roda teste sintético para catalogar endpoints padrão")
    parser.add_argument("--start-proxy", action="store_true", help="Inicia o proxy mitmdump na porta especificada")
    parser.add_argument("--port", type=int, default=8080, help="Porta do proxy (padrão: 8080)")

    args = parser.parse_args()

    if args.test_synthetic:
        run_synthetic_test()
    elif args.start_proxy:
        start_mitmproxy(port=args.port)
    else:
        # Se nenhum argumento for passado, roda o teste sintético para gerar o catálogo
        run_synthetic_test()
