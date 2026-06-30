from openai import OpenAI
import os
import glob

DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE = "https://api.deepseek.com"

def _get_client():
    return OpenAI(api_key=DEEPSEEK_KEY, base_url=DEEPSEEK_BASE)

def _call_deepseek(system_prompt, user_prompt, temperature=0.3, max_tokens=2000):
    """Chamada genérica ao motor DeepSeek."""
    try:
        client = _get_client()
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na conexão com o Motor DeepSeek: {e}"

# ══════════════════════════════════════════════════════════════
# FEATURE 1: CHAT IA REAL (Lê arquivos do cliente e responde)
# ══════════════════════════════════════════════════════════════
def load_client_context(client_base_path):
    """Carrega o conteúdo de todos os .txt e .md da pasta do cliente."""
    context_parts = []
    for ext in ["*.txt", "*.md", "*.html"]:
        for filepath in glob.glob(os.path.join(client_base_path, "**", ext), recursive=True):
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()[:3000]  # Limita cada arquivo a 3000 chars
                    context_parts.append(f"--- Arquivo: {os.path.basename(filepath)} ---\n{content}")
            except:
                continue
    return "\n\n".join(context_parts[:10])  # Máximo 10 arquivos

def chat_with_case(question, client_base_path):
    """Chat inteligente que responde com base nos documentos do cliente."""
    context = load_client_context(client_base_path)
    if not context:
        context = "(Nenhum documento encontrado na pasta do cliente.)"
    
    system = """Você é o Super Analista Jurídico, um assistente de IA especializado em advocacia criminal brasileira.
Você tem acesso aos documentos do caso listados abaixo. Responda de forma precisa, citando 
os documentos quando relevante. Se não souber, diga claramente que a informação não consta nos autos."""
    
    user = f"""DOCUMENTOS DO CASO:
{context}

PERGUNTA DO ADVOGADO:
{question}"""
    
    return _call_deepseek(system, user, temperature=0.2, max_tokens=1500)

# ══════════════════════════════════════════════════════════════
# FEATURE 2: DETECTOR DE CONTRADIÇÕES
# ══════════════════════════════════════════════════════════════
def detect_contradictions(client_base_path):
    """Varre depoimentos e identifica contradições."""
    context = load_client_context(client_base_path)
    if not context:
        return "Nenhum documento encontrado para análise de contradições."
    
    system = "Você é um perito forense em análise de depoimentos criminais."
    user = f"""Analise os seguintes documentos e depoimentos de um processo criminal.
Identifique TODAS as contradições, divergências de datas, horários, versões e inconsistências.

Para cada contradição encontrada, liste:
## Contradição [N]
- **Documento A:** [trecho exato]
- **Documento B:** [trecho contraditório]
- **Impacto na Defesa:** [como explorar isso]

DOCUMENTOS:
{context}"""
    
    return _call_deepseek(system, user, temperature=0.1, max_tokens=2500)

# ══════════════════════════════════════════════════════════════
# FEATURE 3: GERADOR DE PEÇAS PROCESSUAIS
# ══════════════════════════════════════════════════════════════
def generate_legal_piece(piece_type, client_name, facts, client_base_path):
    """Gera petições criminais completas."""
    context = load_client_context(client_base_path)
    
    templates = {
        "Habeas Corpus": """Redija uma petição de HABEAS CORPUS LIBERATÓRIO completa, com:
- Endereçamento ao TJRJ (Tribunal de Justiça do Estado do Rio de Janeiro)
- Qualificação do Paciente
- DOS FATOS
- DO DIREITO (citando Art. 5°, LXVIII da CF, Art. 647/648 CPP e jurisprudência do STJ)
- DO PEDIDO LIMINAR
- DOS PEDIDOS FINAIS""",
        
        "Resposta à Acusação": """Redija uma RESPOSTA À ACUSAÇÃO (Art. 396-A do CPP) completa, com:
- Endereçamento ao Juízo competente
- PRELIMINARES (se houver nulidades)
- DO MÉRITO
- DAS PROVAS A PRODUZIR
- DOS PEDIDOS""",
        
        "Alegações Finais": """Redija ALEGAÇÕES FINAIS POR MEMORIAIS completas, com:
- SÍNTESE DA ACUSAÇÃO
- DA INSTRUÇÃO CRIMINAL
- TESE PRINCIPAL: ABSOLVIÇÃO (Art. 386, VII CPP — In dubio pro reo)
- TESE SUBSIDIÁRIA: DESCLASSIFICAÇÃO
- DOS PEDIDOS"""
    }
    
    template = templates.get(piece_type, templates["Habeas Corpus"])
    
    system = """Você é um advogado criminalista sênior com 20 anos de experiência em tribunais brasileiros.
Redija peças processuais no formato jurídico formal brasileiro, com linguagem técnica mas persuasiva.
Use citações doutrinárias e jurisprudenciais reais quando possível."""
    
    user = f"""{template}

DADOS DO CLIENTE: {client_name}
FATOS DO CASO: {facts}

CONTEXTO DOS AUTOS:
{context[:4000]}"""
    
    return _call_deepseek(system, user, temperature=0.3, max_tokens=4000)

# ══════════════════════════════════════════════════════════════
# FEATURE 6: LEITOR DE PDF COM EXTRAÇÃO DE FATOS
# ══════════════════════════════════════════════════════════════
def extract_pdf_facts(pdf_path):
    """Lê um PDF e extrai fatos-chave usando DeepSeek."""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages[:20]:  # Máximo 20 páginas
            text += page.extract_text() or ""
        
        if not text.strip():
            return "O PDF parece estar escaneado (imagem). Não foi possível extrair texto."
        
        system = "Você é um analista forense especializado em processos criminais brasileiros."
        user = f"""Analise o seguinte documento processual e extraia:

## 1. Tipo do Documento
(Inquérito, Denúncia, Depoimento, Laudo Pericial, Decisão, etc.)

## 2. Fatos-Chave Extraídos
(Liste cada fato relevante com a página onde aparece)

## 3. Datas e Horários Mencionados
(Cronologia dos eventos)

## 4. Pessoas Mencionadas e seus Papéis
(Réu, Testemunha, Vítima, Delegado, etc.)

## 5. Pontos Vulneráveis para a Defesa
(Inconsistências, ausência de provas, violações procedimentais)

TEXTO DO DOCUMENTO:
{text[:6000]}"""
        
        return _call_deepseek(system, user, temperature=0.1, max_tokens=2500)
    except Exception as e:
        return f"Erro ao ler PDF: {e}"

# ══════════════════════════════════════════════════════════════
# FEATURE 7: PERFIL DO MAGISTRADO
# ══════════════════════════════════════════════════════════════
def analyze_judge_profile(judge_name):
    """Gera um perfil analítico do magistrado baseado em conhecimento público."""
    system = """Você é um analista de litigation analytics especializado em tribunais brasileiros.
Com base no seu conhecimento sobre jurisprudência e perfis de magistrados, forneça uma análise estratégica."""
    
    user = f"""Gere um PERFIL TÁTICO do magistrado/desembargador: {judge_name}

Estruture assim:
## Perfil do Magistrado: {judge_name}

### Tendências Conhecidas
(Se houver informação pública sobre suas decisões)

### Recomendações Estratégicas
- Que tipo de argumento tende a ser mais eficaz
- Que tipo de argumento deve ser evitado
- Tom recomendado para sustentação oral

### Alertas
- Posições conhecidas sobre temas específicos

Se você não tiver informações específicas sobre este magistrado, forneça orientações gerais
baseadas no tribunal ao qual pertence e boas práticas de sustentação oral."""
    
    return _call_deepseek(system, user, temperature=0.4, max_tokens=1500)

# ══════════════════════════════════════════════════════════════
# TRIAGEM INICIAL (Já existia)
# ══════════════════════════════════════════════════════════════
def generate_screening_report(facts_summary):
    """Gera um relatório de triagem estruturado usando a API da DeepSeek."""
    system = "Você é um analista estratégico forense e criminalista."
    user = f"""Você é um Analista Jurídico Sênior focado em Advocacia Criminal.
Com base nos fatos reportados abaixo por um novo cliente ou seu familiar, elabore um "Relatório de Triagem Inicial Tático" formatado em Markdown.

Estrutura Obrigatória:
## 1. Resumo dos Fatos
## 2. Possível Tipificação Criminal
## 3. Alertas de Nulidade ou Abuso Policial (Se houver indícios)
## 4. Estratégia de Defesa Inicial Sugerida

Fatos Reportados:
"{facts_summary}"
"""
    return _call_deepseek(system, user, temperature=0.3, max_tokens=1500)
