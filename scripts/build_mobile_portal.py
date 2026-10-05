import os
import json
import glob

def build_portal():
    base_dir = r"c:\Projetos\superJus\graphify-out"
    wiki_dir = os.path.join(base_dir, "wiki")
    graph_json_path = os.path.join(base_dir, "graph.json")
    report_path = os.path.join(base_dir, "GRAPH_REPORT.md")
    output_html_path = os.path.join(base_dir, "portal_mobile.html")

    # 1. Carrega dados do grafo
    with open(graph_json_path, "r", encoding="utf-8") as f:
        graph_data = json.load(f)

    # 2. Carrega artigos da Wiki
    wiki_articles = {}
    wiki_files = glob.glob(os.path.join(wiki_dir, "*.md"))
    for wf in sorted(wiki_files):
        filename = os.path.basename(wf)
        title = filename.replace(".md", "").replace("_", " ").replace("-", " ")
        with open(wf, "r", encoding="utf-8") as f:
            content = f.read()
        wiki_articles[filename] = {
            "title": title,
            "filename": filename,
            "content": content
        }

    # 3. Carrega GRAPH_REPORT.md
    report_content = ""
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            report_content = f.read()

    # Prepara JSON strings seguras para injetar no script
    graph_json_str = json.dumps(graph_data, ensure_ascii=False)
    wiki_articles_str = json.dumps(wiki_articles, ensure_ascii=False)
    report_str = json.dumps(report_content, ensure_ascii=False)

    html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>SuperJus • Júlio Pereira Marcos (Grafo & Wiki Mobile)</title>
  <!-- Bibliotecas CDN de visualização e Markdown -->
  <script src="https://unpkg.com/vis-network@9.1.6/standalone/umd/vis-network.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    :root {{
      --bg: #0b0f19;
      --surface: #111827;
      --surface-card: #1f2937;
      --border: #374151;
      --primary: #3b82f6;
      --primary-hover: #2563eb;
      --accent: #10b981;
      --gold: #f59e0b;
      --danger: #ef4444;
      --text: #f3f4f6;
      --text-muted: #9ca3af;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}
    /* Top Header */
    header {{
      background: rgba(17, 24, 39, 0.95);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid var(--border);
      padding: 10px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      z-index: 50;
      flex-shrink: 0;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .brand-logo {{
      width: 34px;
      height: 34px;
      background: linear-gradient(135deg, #1e3a8a, #3b82f6);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      color: #fff;
      font-size: 16px;
      box-shadow: 0 0 10px rgba(59, 130, 246, 0.4);
    }}
    .brand-title {{
      font-size: 14px;
      font-weight: 700;
      line-height: 1.2;
    }}
    .brand-sub {{
      font-size: 11px;
      color: var(--gold);
      font-weight: 500;
    }}
    /* Navigation Bar / Tabs */
    .tab-bar {{
      display: flex;
      background: #0f172a;
      border-bottom: 1px solid var(--border);
      overflow-x: auto;
      scrollbar-width: none;
      flex-shrink: 0;
    }}
    .tab-btn {{
      flex: 1;
      padding: 12px 10px;
      background: none;
      border: none;
      color: var(--text-muted);
      font-size: 13px;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 7px;
      cursor: pointer;
      border-bottom: 2px solid transparent;
      transition: all 0.2s ease;
      white-space: nowrap;
    }}
    .tab-btn.active {{
      color: #fff;
      border-bottom-color: var(--primary);
      background: rgba(59, 130, 246, 0.08);
    }}
    /* Main View Area */
    main {{
      flex: 1;
      position: relative;
      overflow: hidden;
    }}
    .view-pane {{
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      display: none;
      flex-direction: column;
    }}
    .view-pane.active {{
      display: flex;
    }}
    /* View: Grafo */
    #graph-container {{
      flex: 1;
      width: 100%;
      height: 100%;
      background: radial-gradient(circle at center, #111827 0%, #080c14 100%);
    }}
    .graph-search-bar {{
      position: absolute;
      top: 12px;
      left: 12px;
      right: 12px;
      z-index: 20;
      display: flex;
      gap: 8px;
    }}
    .graph-search-bar input {{
      flex: 1;
      background: rgba(17, 24, 39, 0.9);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border);
      color: #fff;
      padding: 10px 14px;
      border-radius: 20px;
      font-size: 13px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5);
      outline: none;
    }}
    .graph-btn-reset {{
      background: rgba(31, 41, 55, 0.9);
      border: 1px solid var(--border);
      color: var(--text);
      width: 38px;
      height: 38px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5);
      cursor: pointer;
    }}
    /* Quick Community Badges */
    .community-chips {{
      position: absolute;
      top: 58px;
      left: 12px;
      right: 12px;
      display: flex;
      gap: 6px;
      overflow-x: auto;
      padding-bottom: 4px;
      z-index: 15;
      scrollbar-width: none;
    }}
    .chip {{
      padding: 5px 10px;
      border-radius: 14px;
      background: rgba(31, 41, 55, 0.85);
      backdrop-filter: blur(6px);
      border: 1px solid var(--border);
      font-size: 11px;
      white-space: nowrap;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      color: #e5e7eb;
    }}
    .chip-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }}
    /* Bottom Sheet Drawer for Node Info */
    #node-sheet {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: rgba(17, 24, 39, 0.98);
      backdrop-filter: blur(12px);
      border-top: 1px solid var(--border);
      border-radius: 18px 18px 0 0;
      padding: 16px;
      max-height: 60vh;
      overflow-y: auto;
      z-index: 40;
      box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.7);
      transform: translateY(105%);
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    #node-sheet.open {{
      transform: translateY(0);
    }}
    .sheet-handle {{
      width: 36px;
      height: 4px;
      background: #4b5563;
      border-radius: 2px;
      margin: 0 auto 12px auto;
    }}
    .sheet-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 10px;
    }}
    .sheet-title {{
      font-size: 16px;
      font-weight: 700;
      color: #60a5fa;
    }}
    .sheet-close {{
      background: none;
      border: none;
      color: var(--text-muted);
      font-size: 18px;
      cursor: pointer;
      padding: 4px;
    }}
    .sheet-meta {{
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 8px;
    }}
    .sheet-body {{
      font-size: 13px;
      line-height: 1.6;
      color: #d1d5db;
    }}
    /* View: Wiki */
    .wiki-container {{
      display: flex;
      flex-direction: column;
      height: 100%;
      background: var(--bg);
    }}
    .wiki-selector-wrap {{
      padding: 10px 14px;
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      display: flex;
      gap: 8px;
    }}
    .wiki-select {{
      flex: 1;
      background: var(--surface-card);
      color: var(--text);
      border: 1px solid var(--border);
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 13px;
      outline: none;
    }}
    .wiki-article-view {{
      flex: 1;
      overflow-y: auto;
      padding: 16px 20px 80px 20px;
      line-height: 1.7;
    }}
    .wiki-article-view h1 {{
      font-size: 20px;
      color: #60a5fa;
      margin-bottom: 14px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 8px;
    }}
    .wiki-article-view h2 {{
      font-size: 16px;
      color: #93c5fd;
      margin: 18px 0 10px 0;
    }}
    .wiki-article-view h3 {{
      font-size: 14px;
      color: var(--gold);
      margin: 14px 0 8px 0;
    }}
    .wiki-article-view p {{
      margin-bottom: 12px;
      font-size: 14px;
      color: #e5e7eb;
    }}
    .wiki-article-view ul, .wiki-article-view ol {{
      margin-left: 20px;
      margin-bottom: 14px;
      font-size: 13px;
      color: #d1d5db;
    }}
    .wiki-article-view li {{
      margin-bottom: 6px;
    }}
    .wiki-article-view blockquote {{
      border-left: 3px solid var(--primary);
      padding-left: 12px;
      margin: 14px 0;
      color: #9ca3af;
      font-style: italic;
      background: rgba(59, 130, 246, 0.05);
      border-radius: 0 6px 6px 0;
    }}
    .wiki-article-view code {{
      background: #1f2937;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 12px;
      color: #f472b6;
      font-family: monospace;
    }}
    /* View: Relatório */
    .report-view {{
      flex: 1;
      overflow-y: auto;
      padding: 16px 20px 80px 20px;
    }}
  </style>
</head>
<body>

  <!-- Top Header -->
  <header>
    <div class="brand">
      <div class="brand-logo">SJ</div>
      <div>
        <div class="brand-title">SuperJus Knowledge Hub</div>
        <div class="brand-sub"><i class="fa-solid fa-scale-balanced"></i> Caso Júlio Pereira Marcos</div>
      </div>
    </div>
    <div style="font-size: 11px; background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4); padding: 4px 8px; border-radius: 12px;">
      <i class="fa-solid fa-wifi"></i> 5G Mobile
    </div>
  </header>

  <!-- Tab Bar -->
  <div class="tab-bar">
    <button class="tab-btn active" onclick="switchTab('graph')">
      <i class="fa-solid fa-circle-nodes"></i> Grafo Interativo
    </button>
    <button class="tab-btn" onclick="switchTab('wiki')">
      <i class="fa-solid fa-book-open"></i> Wiki Estratégica (19)
    </button>
    <button class="tab-btn" onclick="switchTab('report')">
      <i class="fa-solid fa-chart-pie"></i> Relatório & Métricas
    </button>
  </div>

  <!-- Main Area -->
  <main>
    <!-- View: Grafo -->
    <div id="pane-graph" class="view-pane active">
      <div class="graph-search-bar">
        <input type="text" id="node-search" placeholder="🔍 Buscar nós, ministros, teses, processos..." oninput="onSearchNodes()">
        <button class="graph-btn-reset" onclick="resetGraphView()" title="Centralizar Grafo">
          <i class="fa-solid fa-compress"></i>
        </button>
      </div>

      <div class="community-chips" id="community-chips"></div>

      <div id="graph-container"></div>

      <!-- Bottom Sheet Drawer -->
      <div id="node-sheet">
        <div class="sheet-handle" onclick="closeSheet()"></div>
        <div class="sheet-header">
          <div>
            <div id="sheet-title" class="sheet-title">Nó Selecionado</div>
            <div id="sheet-community" class="sheet-meta">Comunidade</div>
          </div>
          <button class="sheet-close" onclick="closeSheet()"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <div id="sheet-body" class="sheet-body">Detalhes do nó...</div>
        <div id="sheet-connections" style="margin-top: 14px;">
          <h4 style="font-size: 12px; color: #9ca3af; text-transform: uppercase; margin-bottom: 6px;">Conexões Diretas:</h4>
          <div id="sheet-neighbors" style="display: flex; flex-wrap: wrap; gap: 6px;"></div>
        </div>
      </div>
    </div>

    <!-- View: Wiki -->
    <div id="pane-wiki" class="view-pane">
      <div class="wiki-container">
        <div class="wiki-selector-wrap">
          <select id="wiki-select" class="wiki-select" onchange="loadSelectedArticle()">
            <!-- Populado dinamicamente -->
          </select>
        </div>
        <div id="wiki-content" class="wiki-article-view"></div>
      </div>
    </div>

    <!-- View: Relatório -->
    <div id="pane-report" class="view-pane">
      <div id="report-content" class="report-view wiki-article-view"></div>
    </div>
  </main>

  <script>
    // Injeção de dados estruturados
    const rawGraphData = {graph_json_str};
    const wikiArticles = {wiki_articles_str};
    const reportMd = {report_str};

    let network = null;
    let nodesDataSet = null;
    let edgesDataSet = null;
    const communityColors = [
      "#3b82f6", "#10b981", "#f59e0b", "#ec4899", 
      "#8b5cf6", "#06b6d4", "#f97316", "#14b8a6"
    ];

    // Alternar Abas
    function switchTab(tab) {{
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.view-pane').forEach(p => p.classList.remove('active'));

      if (tab === 'graph') {{
        document.querySelector('.tab-btn:nth-child(1)').classList.add('active');
        document.getElementById('pane-graph').classList.add('active');
        if (network) network.fit();
      }} else if (tab === 'wiki') {{
        document.querySelector('.tab-btn:nth-child(2)').classList.add('active');
        document.getElementById('pane-wiki').classList.add('active');
      }} else if (tab === 'report') {{
        document.querySelector('.tab-btn:nth-child(3)').classList.add('active');
        document.getElementById('pane-report').classList.add('active');
      }}
    }}

    // Inicializar Grafo
    function initGraph() {{
      const container = document.getElementById('graph-container');
      const communities = [...new Set(rawGraphData.nodes.map(n => n.community))].sort();

      // Renderizar chips de comunidade
      const chipsContainer = document.getElementById('community-chips');
      chipsContainer.innerHTML = '';
      communities.forEach((comm, idx) => {{
        const color = communityColors[idx % communityColors.length];
        const chip = document.createElement('div');
        chip.className = 'chip';
        chip.innerHTML = `<span class="chip-dot" style="background:${{color}}"></span> Comunidade ${{comm}}`;
        chip.onclick = () => focusCommunity(comm);
        chipsContainer.appendChild(chip);
      }});

      // Mapear nós para Vis.js
      const nodes = rawGraphData.nodes.map(n => {{
        const color = communityColors[n.community % communityColors.length] || "#3b82f6";
        return {{
          id: n.id,
          label: n.label || n.id,
          community: n.community,
          raw: n,
          color: {{
            background: color,
            border: '#ffffff',
            highlight: {{ background: '#f59e0b', border: '#ffffff' }}
          }},
          font: {{ color: '#f3f4f6', size: 12, face: 'sans-serif' }},
          shape: 'dot',
          size: Math.max(12, (n.degree || 1) * 3)
        }};
      }});

      // Mapear arestas para Vis.js
      const edges = rawGraphData.links.map(l => ({{
        from: l.source,
        to: l.target,
        color: {{ color: '#4b5563', highlight: '#f59e0b', opacity: 0.5 }},
        width: 1.2
      }}));

      nodesDataSet = new vis.DataSet(nodes);
      edgesDataSet = new vis.DataSet(edges);

      const data = {{ nodes: nodesDataSet, edges: edgesDataSet }};
      const options = {{
        physics: {{
          barnesHut: {{
            gravitationalConstant: -2800,
            centralGravity: 0.3,
            springLength: 95,
            springConstant: 0.04,
            damping: 0.09
          }},
          stabilization: {{ iterations: 120 }}
        }},
        interaction: {{
          hover: true,
          touchAngle: 45,
          zoomView: true,
          dragView: true
        }}
      }};

      network = new vis.Network(container, data, options);

      // Evento de clique no nó (Touch & Desktop)
      network.on("click", function(params) {{
        if (params.nodes.length > 0) {{
          const nodeId = params.nodes[0];
          showNodeDetails(nodeId);
        }}
      }});
    }}

    function showNodeDetails(nodeId) {{
      const node = rawGraphData.nodes.find(n => n.id === nodeId);
      if (!node) return;

      document.getElementById('sheet-title').innerText = node.label || node.id;
      document.getElementById('sheet-community').innerText = `Comunidade ${{node.community}} • Tipo: ${{node.type || 'Entidade Jurídica'}}`;
      
      let bodyText = node.description || (node.attributes ? JSON.stringify(node.attributes, null, 2) : 'Sem detalhes adicionais.');
      document.getElementById('sheet-body').innerHTML = `<p>${{bodyText}}</p>`;

      // Encontrar vizinhos conectados
      const connectedNeighbors = rawGraphData.links
        .filter(l => l.source === nodeId || l.target === nodeId)
        .map(l => l.source === nodeId ? l.target : l.source);

      const neighborsContainer = document.getElementById('sheet-neighbors');
      neighborsContainer.innerHTML = '';
      [...new Set(connectedNeighbors)].forEach(nbId => {{
        const btn = document.createElement('button');
        btn.style.cssText = "background: #1f2937; border: 1px solid #374151; color: #60a5fa; padding: 4px 8px; border-radius: 6px; font-size: 11px; cursor: pointer;";
        btn.innerText = nbId;
        btn.onclick = () => {{
          network.focus(nbId, {{ scale: 1.2, animation: true }});
          showNodeDetails(nbId);
        }};
        neighborsContainer.appendChild(btn);
      }});

      document.getElementById('node-sheet').classList.add('open');
    }}

    function closeSheet() {{
      document.getElementById('node-sheet').classList.remove('open');
    }}

    function resetGraphView() {{
      network.fit({{ animation: true }});
    }}

    function focusCommunity(commId) {{
      const targetNodes = rawGraphData.nodes.filter(n => n.community === commId).map(n => n.id);
      network.fit({{ nodes: targetNodes, animation: true }});
    }}

    function onSearchNodes() {{
      const term = document.getElementById('node-search').value.toLowerCase().trim();
      if (!term) return;
      const matched = rawGraphData.nodes.find(n => (n.label || n.id).toLowerCase().includes(term));
      if (matched) {{
        network.focus(matched.id, {{ scale: 1.3, animation: true }});
        showNodeDetails(matched.id);
      }}
    }}

    // Inicializar Wiki
    function initWiki() {{
      const select = document.getElementById('wiki-select');
      select.innerHTML = '';
      
      const fileKeys = Object.keys(wikiArticles);
      fileKeys.forEach(key => {{
        const opt = document.createElement('option');
        opt.value = key;
        opt.innerText = wikiArticles[key].title;
        if (key === 'index.md') opt.selected = true;
        select.appendChild(opt);
      }});

      loadSelectedArticle();
    }}

    function loadSelectedArticle() {{
      const select = document.getElementById('wiki-select');
      const chosenKey = select.value;
      const article = wikiArticles[chosenKey];
      if (article) {{
        document.getElementById('wiki-content').innerHTML = marked.parse(article.content);
      }}
    }}

    // Inicializar Relatório
    function initReport() {{
      if (reportMd) {{
        document.getElementById('report-content').innerHTML = marked.parse(reportMd);
      }}
    }}

    // Inicialização ao carregar
    window.addEventListener('DOMContentLoaded', () => {{
      initGraph();
      initWiki();
      initReport();
    }});
  </script>
</body>
</html>
"""

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"Sucesso! Portal Mobile compilado com sucesso em: {output_html_path} ({os.path.getsize(output_html_path)} bytes)")

if __name__ == "__main__":
    build_portal()
