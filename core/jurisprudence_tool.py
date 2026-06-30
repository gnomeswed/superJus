from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import Tool

def get_jurisprudence_tool():
    """
    Returns a LangChain Tool configured to search the web for jurisprudence.
    Using DuckDuckGo as a free alternative to paid legal APIs.
    """
    search = DuckDuckGoSearchRun()
    
    def search_jurisprudence(query: str):
        # Enhance the query to target legal decisions
        enhanced_query = f"jurisprudência STJ STF TJ {query} site:jusbrasil.com.br OR site:stj.jus.br OR site:stf.jus.br"
        return search.run(enhanced_query)

    jurisprudence_tool = Tool(
        name="Busca de Jurisprudência",
        func=search_jurisprudence,
        description="Útil para buscar jurisprudência, acórdãos e decisões do STJ, STF e TJs sobre temas jurídicos. Forneça como entrada a tese jurídica (ex: 'nulidade busca apreensão invasão domicílio')."
    )
    
    return jurisprudence_tool

if __name__ == "__main__":
    tool = get_jurisprudence_tool()
    print("Testando busca de jurisprudência para 'tráfico privilegiado':")
    print(tool.run("tráfico privilegiado"))
