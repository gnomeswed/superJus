import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.retriever import create_retriever_tool
from core.vector_store import get_vector_store
from core.jurisprudence_tool import get_jurisprudence_tool
from dotenv import load_dotenv

load_dotenv()

def get_legal_agent():
    # Inicializar LLM
    # Importante: defina a variável GOOGLE_API_KEY no arquivo .env
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.2)
    
    tools = []
    
    # 1. Ferramenta de Retenção de Documentos (RAG dos autos)
    vector_store = get_vector_store()
    if vector_store:
        retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        autos_tool = create_retriever_tool(
            retriever,
            "buscar_autos_processo",
            "Busca informações detalhadas nos documentos, laudos, depoimentos e peças do Processo do Júlio. Use esta ferramenta sempre que precisar responder sobre os fatos do caso."
        )
        tools.append(autos_tool)
    else:
        print("Aviso: Banco vetorial não encontrado. O agente não terá acesso aos autos. Execute core/vector_store.py primeiro.")

    # 2. Ferramenta de Jurisprudência
    jurisprudence_tool = get_jurisprudence_tool()
    tools.append(jurisprudence_tool)

    # Configurar o Prompt do Agente
    system_message = """Você é um 'Super Analista Jurídico', um assistente virtual especializado em direito criminal, dedicado ao Processo do Júlio.
Seu objetivo é ajudar os advogados de defesa analisando o processo, apontando contradições nos depoimentos, sugerindo teses defensivas e redigindo minutas de peças processuais.
Você tem acesso a duas ferramentas principais:
1. 'buscar_autos_processo': Para ler os documentos oficiais do processo do Júlio. Baseie-se ESTRITAMENTE nos fatos encontrados aqui. Se não encontrar a informação nos autos, diga que não consta no processo.
2. 'Busca de Jurisprudência': Para pesquisar decisões de tribunais superiores (STJ, STF) que apoiem as teses de defesa.

Seja técnico, analítico e utilize o jargão jurídico adequado. Formate suas respostas de maneira clara usando Markdown.
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Criar o Agente
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor

if __name__ == "__main__":
    agent = get_legal_agent()
    response = agent.invoke({"input": "Faça um resumo de quais são as principais acusações contra o Júlio segundo os autos."})
    print(response['output'])
