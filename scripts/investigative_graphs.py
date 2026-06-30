import networkx as nx
from pyvis.network import Network
import os
import json

def build_investigative_graph(case_path, output_html=None):
    """
    Gera um mapa investigativo interativo profissional.
    Lê dados de um arquivo graph_data.json se existir, ou gera demo tático.
    """
    if output_html is None:
        output_html = os.path.join(case_path, "analises", "Teia_Tatica_Defesa.html")
    
    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    
    G = nx.DiGraph()  # Grafo direcionado para mostrar fluxo
    
    # Verifica se existe um arquivo de dados customizado
    data_path = os.path.join(case_path, "analises", "graph_data.json")
    
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for node in data.get("nodes", []):
            G.add_node(node["id"], **{k:v for k,v in node.items() if k != "id"})
        for edge in data.get("edges", []):
            G.add_edge(edge["from"], edge["to"], **{k:v for k,v in edge.items() if k not in ("from","to")})
    else:
        # ── DEMO: Caso Julio Pereira Marcos ──
        
        # CLIENTE (Centro do mapa)
        G.add_node("Julio Marcos", 
                    label="JULIO MARCOS\n(Cliente)", 
                    group="cliente",
                    title="<b>Julio Pereira Marcos</b><br>Status: PRESO (Preventiva)<br>Art. 33 + Art. 35 Lei 11.343/06<br><i>Unico preso entre 6 correus</i>",
                    size=40, color="#ef4444", font={"size": 16, "color": "#ffffff"}, 
                    shape="dot", borderWidth=3, borderWidthSelected=5)
        
        # CORREUS (Todos soltos - cor verde)
        correus = [
            ("Guilherme", "Apreendido com 218g de cocaina\nSTATUS: SOLTO"),
            ("Rodrigo", "Correu - mesmo inquerito\nSTATUS: SOLTO"),
            ("Correu 3", "Correu - mesmo inquerito\nSTATUS: SOLTO"),
            ("Correu 4", "Correu - mesmo inquerito\nSTATUS: SOLTO"),
            ("Correu 5", "Correu - mesmo inquerito\nSTATUS: SOLTO"),
        ]
        for name, desc in correus:
            G.add_node(name, 
                        label=f"{name}\n(Solto)", 
                        group="correu_solto",
                        title=f"<b>{name}</b><br>{desc}<br><span style='color:#22c55e'>Art. 580 CPP - Isonomia</span>",
                        size=22, color="#22c55e", font={"size": 12, "color": "#ffffff"},
                        shape="dot", borderWidth=2)
        
        # PROVAS
        G.add_node("Chip 4432", 
                    label="CHIP 4432\n(Prova Fragil)", 
                    group="prova",
                    title="<b>Chip Telefonico Final 4432</b><br>Nao houve pericia de voz<br>Nao ha laudo tecnico vinculando ao cliente<br><span style='color:#f59e0b'>PROVA NULA?</span>",
                    size=30, color="#f59e0b", font={"size": 13, "color": "#000000"},
                    shape="diamond", borderWidth=2)
        
        G.add_node("Droga 218g",
                    label="218g Cocaina\n(Apreensao)",
                    group="prova",
                    title="<b>Apreensao de Drogas</b><br>218g de cocaina<br>Apreendida com GUILHERME, nao com Julio",
                    size=25, color="#f59e0b", font={"size": 11, "color": "#000000"},
                    shape="diamond", borderWidth=2)
        
        # AUTORIDADES / TESTEMUNHAS
        G.add_node("Del. Rodrigo",
                    label="Del. Rodrigo\n(Depoimento)",
                    group="autoridade",
                    title="<b>Delegado Rodrigo</b><br>Admitiu: NAO foi feito laudo de voz<br><span style='color:#ef4444'>Fragiliza a acusacao</span>",
                    size=18, color="#64748b", font={"size": 11, "color": "#ffffff"},
                    shape="square", borderWidth=1)
        
        G.add_node("Del. Nelson",
                    label="Del. Nelson\n(Depoimento)",
                    group="autoridade",
                    title="<b>Delegado Nelson</b><br>Declarou: NAO ha evidencia de faccao<br><span style='color:#22c55e'>Favoravel a defesa</span>",
                    size=18, color="#64748b", font={"size": 11, "color": "#ffffff"},
                    shape="square", borderWidth=1)
        
        # TESES JURIDICAS
        G.add_node("Isonomia Art.580",
                    label="ISONOMIA\nArt. 580 CPP",
                    group="tese",
                    title="<b>Extensao de Efeitos</b><br>Se 5 correus estao soltos, Julio tambem deve ser<br>Jurisprudencia consolidada no STJ",
                    size=28, color="#2563eb", font={"size": 12, "color": "#ffffff"},
                    shape="star", borderWidth=2)
        
        G.add_node("Ausencia Materialidade",
                    label="SEM PROVA\nMATERIAL",
                    group="tese",
                    title="<b>Ausencia de Materialidade</b><br>Nenhuma droga apreendida com Julio<br>Chip sem laudo pericial",
                    size=25, color="#2563eb", font={"size": 11, "color": "#ffffff"},
                    shape="star", borderWidth=2)
        
        # ── CONEXOES (Arestas) ──
        
        # Julio -> Provas (linha vermelha tracejada = vinculo fragil)
        G.add_edge("Julio Marcos", "Chip 4432", 
                    label="Vinculo SUPOSTO", color={"color": "#ef4444", "opacity": 0.7},
                    dashes=True, width=2, font={"size": 9, "color": "#ef4444"})
        
        # Chip -> Delegados (confirma fragilidade)
        G.add_edge("Chip 4432", "Del. Rodrigo",
                    label="Sem laudo", color={"color": "#f59e0b", "opacity": 0.8},
                    width=2, font={"size": 9, "color": "#f59e0b"})
        
        G.add_edge("Del. Nelson", "Julio Marcos",
                    label="Afastou Art.35", color={"color": "#22c55e", "opacity": 0.8},
                    width=2, font={"size": 9, "color": "#22c55e"})
        
        # Droga -> Guilherme (nao a Julio)
        G.add_edge("Droga 218g", "Guilherme",
                    label="Apreendida COM ELE", color={"color": "#f59e0b", "opacity": 0.8},
                    width=3, font={"size": 9, "color": "#f59e0b"})
        
        # Correus entre si (isonomia)
        for name, _ in correus:
            G.add_edge(name, "Isonomia Art.580",
                        color={"color": "#22c55e", "opacity": 0.4},
                        width=1, dashes=[5,5])
        
        G.add_edge("Julio Marcos", "Isonomia Art.580",
                    label="DEVE SER ESTENDIDO", color={"color": "#2563eb", "opacity": 0.9},
                    width=3, font={"size": 10, "color": "#2563eb"})
        
        G.add_edge("Chip 4432", "Ausencia Materialidade",
                    label="Sem pericia", color={"color": "#2563eb", "opacity": 0.7},
                    width=2, font={"size": 9, "color": "#2563eb"})
        
        G.add_edge("Droga 218g", "Ausencia Materialidade",
                    label="Nao era de Julio", color={"color": "#2563eb", "opacity": 0.7},
                    width=2, font={"size": 9, "color": "#2563eb"})

    # ── RENDERIZAR COM PYVIS ──
    net = Network(
        height="560px", 
        width="100%", 
        bgcolor="#09090b",       # Zinc-950
        font_color="#fafafa",    # Zinc-50
        directed=True,
        select_menu=False,
        filter_menu=False,
    )
    
    # Fisica otimizada para layout bonito
    net.set_options(json.dumps({
        "physics": {
            "enabled": True,
            "solver": "forceAtlas2Based",
            "forceAtlas2Based": {
                "gravitationalConstant": -80,
                "centralGravity": 0.008,
                "springLength": 180,
                "springConstant": 0.04,
                "damping": 0.5
            },
            "stabilization": {
                "enabled": True,
                "iterations": 200
            }
        },
        "interaction": {
            "hover": True,
            "tooltipDelay": 100,
            "navigationButtons": True,
            "keyboard": True,
            "zoomView": True
        },
        "edges": {
            "smooth": {
                "type": "curvedCW",
                "roundness": 0.15
            },
            "arrows": {
                "to": {"enabled": True, "scaleFactor": 0.6}
            }
        },
        "nodes": {
            "shadow": {
                "enabled": True,
                "color": "rgba(0,0,0,0.3)",
                "size": 8
            }
        }
    }))
    
    net.from_nx(G)
    
    # Gerar HTML e injetar legenda
    net.write_html(output_html)
    
    # Adicionar legenda customizada ao HTML gerado
    with open(output_html, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()
    
    legend = """
    <div style="position:absolute; top:10px; right:10px; background:rgba(9,9,11,0.85); 
                border:1px solid #1e1e24; border-radius:8px; padding:12px 16px; 
                font-family:'DM Sans',sans-serif; font-size:11px; color:#a1a1aa; z-index:999;">
        <div style="font-weight:600; color:#fafafa; margin-bottom:8px; font-size:12px;">LEGENDA</div>
        <div style="margin:4px 0;"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#ef4444;margin-right:6px;"></span> Cliente (Preso)</div>
        <div style="margin:4px 0;"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#22c55e;margin-right:6px;"></span> Correus (Soltos)</div>
        <div style="margin:4px 0;"><span style="display:inline-block;width:10px;height:10px;background:#f59e0b;margin-right:6px;transform:rotate(45deg);"></span> Provas</div>
        <div style="margin:4px 0;"><span style="display:inline-block;width:10px;height:10px;background:#64748b;margin-right:6px;"></span> Autoridades</div>
        <div style="margin:4px 0;"><span style="display:inline-block;width:12px;height:12px;background:#2563eb;margin-right:6px;clip-path:polygon(50% 0%,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%);"></span> Teses de Defesa</div>
        <div style="margin-top:8px; border-top:1px solid #1e1e24; padding-top:6px; font-size:10px; color:#52525b;">
            --- tracejado = vinculo fragil<br>
            Passe o mouse nos nos para detalhes
        </div>
    </div>
    """
    
    html = html.replace("</body>", legend + "</body>")
    
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"[+] Teia Investigativa Profissional salva em: {output_html}")
    return output_html

if __name__ == "__main__":
    case_path = r"c:\Projetos\Super Analista Juridico\Clientes\Julio_Pereira_Marcos\Caso_Principal"
    build_investigative_graph(case_path)
