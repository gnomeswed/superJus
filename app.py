import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import streamlit.components.v1 as components
import os, json, sys, datetime, shutil, glob

# Garante que o diretório de scripts esteja no path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="Super Analista Jurídico",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
# THEME SYSTEM
# ══════════════════════════════════════════════════════════════
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "messages" not in st.session_state:
    st.session_state.messages = []

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

IS_DARK = st.session_state.theme == "dark"
CLIENTS_ROOT = r"c:\Projetos\Super Analista Jurídico\Clientes"

# ══════════════════════════════════════════════════════════════
# CSS DESIGN SYSTEM (Zinc / shadcn)
# ══════════════════════════════════════════════════════════════
css_fonts = '<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'
st.markdown(css_fonts, unsafe_allow_html=True)

css = f"""
<style>
:root {{
    --bg: {'#09090b' if IS_DARK else '#ffffff'};
    --bg-subtle: {'#0c0c0f' if IS_DARK else '#f9fafb'};
    --card: {'#0c0c0f' if IS_DARK else '#ffffff'};
    --card-hover: {'#131316' if IS_DARK else '#f4f4f5'};
    --border: {'#1e1e24' if IS_DARK else '#e4e4e7'};
    --border-subtle: {'#16161a' if IS_DARK else '#f0f0f2'};
    --text: {'#fafafa' if IS_DARK else '#09090b'};
    --text-muted: #71717a;
    --text-dim: {'#52525b' if IS_DARK else '#a1a1aa'};
    --accent: #2563eb;
    --accent-muted: #1d4ed8;
    --green: {'#22c55e' if IS_DARK else '#16a34a'};
    --green-muted: {'rgba(34,197,94,0.12)' if IS_DARK else 'rgba(22,163,74,0.08)'};
    --red: {'#ef4444' if IS_DARK else '#dc2626'};
    --red-muted: {'rgba(239,68,68,0.12)' if IS_DARK else 'rgba(220,38,38,0.08)'};
    --amber: {'#f59e0b' if IS_DARK else '#d97706'};
    --amber-muted: {'rgba(245,158,11,0.12)' if IS_DARK else 'rgba(217,119,6,0.08)'};
    --shadow: {'none' if IS_DARK else '0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.03)'};
    --radius: 10px;
}}

header[data-testid="stHeader"], #MainMenu, footer, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"], .stDeployButton {{
    display: none !important;
}}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .block-container, section[data-testid="stMain"] {{
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', -apple-system, sans-serif !important;
}}
.block-container {{
    padding: 1.5rem 2.5rem 3rem !important;
    max-width: 1360px !important;
}}

[data-testid="stSidebar"] {{
    background-color: var(--bg-subtle) !important;
    border-right: 1px solid var(--border) !important;
}}
[data-testid="stSidebar"] * {{
    color: var(--text) !important;
}}

button[data-baseweb="tab"] {{
    background: transparent !important;
    color: var(--text-muted) !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    padding: 0.5rem 0.9rem !important;
    border: 1px solid transparent !important;
    border-radius: 7px !important;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
    color: var(--text) !important;
    background: var(--card) !important;
    border-color: var(--border) !important;
}}
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] {{ display: none !important; }}
[data-baseweb="tab-list"] {{
    gap: 4px !important;
    background: var(--bg-subtle) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 3px;
}}

[data-testid="stHorizontalBlock"] {{ gap: 1rem !important; }}

.metric-card {{ background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.1rem 1.3rem; box-shadow: var(--shadow); transition: border-color 0.2s; }}
.metric-card:hover {{ border-color: var(--accent); }}
.metric-label {{ font-size: 0.72rem; color: var(--text-muted); font-weight: 500; text-transform: uppercase; letter-spacing: 0.04em; }}
.metric-value {{ font-size: 1.6rem; font-weight: 700; color: var(--text); letter-spacing: -0.03em; font-family: 'JetBrains Mono', monospace; }}
.metric-delta {{ font-size: 0.7rem; font-weight: 500; margin-top: 0.35rem; padding: 2px 8px; border-radius: 6px; display: inline-flex; align-items: center; gap: 3px; }}
.delta-up {{ color: var(--green); background: var(--green-muted); }}
.delta-down {{ color: var(--red); background: var(--red-muted); }}
.delta-warn {{ color: var(--amber); background: var(--amber-muted); }}

.chart-wrap {{ background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.2rem; box-shadow: var(--shadow); margin-bottom: 1rem; }}
.chart-title {{ font-size: 0.82rem; font-weight: 600; color: var(--text); }}
.chart-subtitle {{ font-size: 0.7rem; color: var(--text-dim); margin-bottom: 0.6rem; }}

.data-table {{ width: 100%; border-collapse: separate; border-spacing: 0; font-size: 0.78rem; }}
.data-table th {{ text-align: left; padding: 0.55rem 0.8rem; color: var(--text-muted); font-weight: 500; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.04em; border-bottom: 1px solid var(--border); }}
.data-table td {{ padding: 0.55rem 0.8rem; color: var(--text); border-bottom: 1px solid var(--border-subtle); }}
.data-table tr:last-child td {{ border-bottom: none; }}

.badge {{ display: inline-block; padding: 2px 9px; border-radius: 6px; font-size: 0.7rem; font-weight: 500; }}
.badge-green {{ color: var(--green); background: var(--green-muted); }}
.badge-red {{ color: var(--red); background: var(--red-muted); }}
.badge-amber {{ color: var(--amber); background: var(--amber-muted); }}
.badge-blue {{ color: var(--accent); background: rgba(37,99,235,0.1); }}

.brand-name {{ font-size: 1.3rem; font-weight: 700; color: var(--text); letter-spacing: -0.02em; }}
.brand-sub {{ font-size: 0.8rem; color: var(--text-muted); }}

.deadline-alert {{ animation: pulse 2s infinite; }}
@keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} }}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════
def metric_card(label, value, delta=None, delta_type="up"):
    cls = f"delta-{delta_type}"
    arrow = "↑" if delta_type == "up" else ("↓" if delta_type == "down" else "→")
    delta_html = f'<div class="metric-delta {cls}">{arrow} {delta}</div>' if delta else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def get_client_cases(client_folder):
    """FEATURE 10: Lista todos os casos de um cliente, com Caso_Principal sempre primeiro."""
    cases = []
    client_path = os.path.join(CLIENTS_ROOT, client_folder)
    for item in os.listdir(client_path):
        full = os.path.join(client_path, item)
        if os.path.isdir(full) and item.startswith("Caso"):
            cases.append(item)
    # Caso_Principal sempre em primeiro lugar
    if "Caso_Principal" in cases:
        cases.remove("Caso_Principal")
        cases.insert(0, "Caso_Principal")
    if not cases:
        cases = ["Caso_Principal"]
    return cases

def get_case_base_path(client_folder, case_name):
    return os.path.join(CLIENTS_ROOT, client_folder, case_name)

def load_deadlines(case_path):
    """FEATURE 8: Carrega prazos do arquivo deadlines.json."""
    dl_path = os.path.join(case_path, "deadlines.json")
    if os.path.exists(dl_path):
        with open(dl_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_deadlines(case_path, deadlines):
    dl_path = os.path.join(case_path, "deadlines.json")
    with open(dl_path, "w", encoding="utf-8") as f:
        json.dump(deadlines, f, ensure_ascii=False, indent=2)

def load_timeline(case_path):
    """FEATURE 4: Carrega timeline editável."""
    tl_path = os.path.join(case_path, "timeline.json")
    if os.path.exists(tl_path):
        with open(tl_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return [
        {"date": "2021-03", "event": "Inquérito Policial Instaurado"},
        {"date": "2022-08", "event": "Corréus liberados"},
        {"date": "2026-05", "event": "HC Preventivo impetrado"},
        {"date": "2026-06", "event": "Prisão preventiva efetivada"}
    ]

def save_timeline(case_path, timeline):
    tl_path = os.path.join(case_path, "timeline.json")
    with open(tl_path, "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)

# ══════════════════════════════════════════════════════════════
# SIDEBAR (Seleção de Clientes + Ferramentas)
# ══════════════════════════════════════════════════════════════
st.sidebar.markdown("""
<div style="text-align:center; padding: 0.5rem 0 1rem 0;">
    <div style="font-size: 2rem;">⚖️</div>
    <div class="brand-name">Super Analista</div>
    <div class="brand-sub">Motor Jurídico v2.0</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Lista dinâmica de clientes
clientes = []
if os.path.exists(CLIENTS_ROOT):
    clientes = sorted([d for d in os.listdir(CLIENTS_ROOT) if os.path.isdir(os.path.join(CLIENTS_ROOT, d))])

options = ["➕ Adicionar Novo Cliente..."] + clientes
selected_client = st.sidebar.selectbox("📂 Cliente", options, index=1 if clientes else 0)

# FEATURE 10: Multi-caso
selected_case = "Caso_Principal"
if selected_client != "➕ Adicionar Novo Cliente...":
    cases = get_client_cases(selected_client)
    if len(cases) > 1:
        selected_case = st.sidebar.selectbox("📁 Caso", cases)
    else:
        selected_case = cases[0]
    
    # Botão para adicionar novo caso
    if st.sidebar.button("➕ Novo Caso para este Cliente"):
        new_case_name = f"Caso_{len(cases)+1}"
        new_path = os.path.join(CLIENTS_ROOT, selected_client, new_case_name)
        os.makedirs(os.path.join(new_path, "analises"), exist_ok=True)
        os.makedirs(os.path.join(new_path, "pecas"), exist_ok=True)
        os.makedirs(os.path.join(new_path, "documentos_processo"), exist_ok=True)
        st.sidebar.success(f"Caso '{new_case_name}' criado!")
        st.rerun()

st.sidebar.markdown("---")

# Theme toggle
theme_label = "☀️ Modo Claro" if IS_DARK else "🌙 Modo Escuro"
st.sidebar.button(theme_label, on_click=toggle_theme, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# ONBOARDING (Cadastro de Novo Cliente)
# ══════════════════════════════════════════════════════════════
if selected_client == "➕ Adicionar Novo Cliente...":
    head_left, head_right = st.columns([8, 2])
    with head_left:
        st.markdown("""
        <div class="brand">
            <div class="brand-name">Cadastrar Novo Cliente</div>
            <div class="brand-sub">O Motor DeepSeek gerará automaticamente um Relatório de Triagem</div>
        </div><br>
        """, unsafe_allow_html=True)

    with st.form("form_onboarding", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome Completo do Cliente (Réu/Investigado)")
        with col2:
            num_processo = st.text_input("Número do Processo (Opcional)")
        
        fatos = st.text_area("Resumo dos Fatos (Cole o BO ou descreva o ocorrido)", height=200, placeholder="Ex: O cliente foi preso em flagrante no dia 01/06/2026 sob acusação de tráfico de drogas (Art. 33 Lei 11.343/06). A apreensão ocorreu na Rua X, bairro Y...")
        
        submitted = st.form_submit_button("⚡ Cadastrar e Gerar Análise DeepSeek", use_container_width=True)
    
    if submitted and nome:
        with st.spinner("Criando infraestrutura local e acionando DeepSeek..."):
            nome_pasta = nome.replace(" ", "_")
            base = os.path.join(CLIENTS_ROOT, nome_pasta, "Caso_Principal")
            os.makedirs(os.path.join(base, "analises"), exist_ok=True)
            os.makedirs(os.path.join(base, "pecas"), exist_ok=True)
            os.makedirs(os.path.join(base, "documentos_processo"), exist_ok=True)

            # Salvar timeline default
            save_timeline(base, [{"date": datetime.datetime.now().strftime("%Y-%m"), "event": "Caso cadastrado no sistema"}])

            # Salvar metadados básicos do caso/cadastro
            meta_path = os.path.join(base, "case_meta.json")
            try:
                with open(meta_path, "w", encoding="utf-8") as meta_file:
                    json.dump({"nome": nome, "numero_processo": (num_processo or "").strip()}, meta_file, ensure_ascii=False, indent=2)
            except Exception as meta_err:
                print(f"[extract] Falha ao salvar case_meta.json: {meta_err}")

            # Chamar DeepSeek se tiver fatos
            if fatos:
                try:
                    from scripts.ai_engine import generate_screening_report
                    report = generate_screening_report(fatos)
                    with open(os.path.join(base, "analises", "Relatorio_Triagem.md"), "w", encoding="utf-8") as f:
                        f.write(report)
                    st.success(f"✅ Cliente '{nome}' cadastrado! Relatório de Triagem gerado pela DeepSeek.")
                    st.markdown("---")
                    st.markdown(report)
                except Exception as e:
                    st.warning(f"Pastas criadas, mas houve erro na DeepSeek: {e}")
            else:
                st.success(f"✅ Cliente '{nome}' cadastrado! (Sem fatos para analisar)")
    
    st.stop()

# ══════════════════════════════════════════════════════════════
# DASHBOARD PRINCIPAL (Cliente Selecionado)
# ══════════════════════════════════════════════════════════════
case_path = get_case_base_path(selected_client, selected_case)
client_display = selected_client.replace("_", " ")

# Carregar metadados do cliente/caso de forma genérica
case_meta = {}
meta_path = os.path.join(case_path, "case_meta.json")
if os.path.exists(meta_path):
    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            case_meta = json.load(f) or {}
    except Exception:
        case_meta = {}

default_process_number = case_meta.get("numero_processo") or ""

# Montar dados básicos do cliente para a tela inicial
client_name = case_meta.get("nome") or client_display
client_process = default_process_number or "Número não informado"
client_rg = case_meta.get("rg") or ""
client_cpf = case_meta.get("cpf") or ""
client_article = case_meta.get("artigo") or ""
client_status = case_meta.get("status") or ""

# Header
head_left, head_right = st.columns([8, 2])
with head_left:
    st.markdown(f"""
    <div class="brand">
        <div class="brand-name">Super Analista Jurídico</div>
        <div class="brand-sub">{client_display} › {selected_case.replace('_', ' ')}</div>
    </div>
    """, unsafe_allow_html=True)

with head_right:
    if st.button("Recarregar caso", key="btn_reload_case", use_container_width=True):
        st.rerun()

# Card de identificação do cliente
with st.container():
    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    badge_status_html = (
        f"<span class='badge badge-amber' style='white-space:nowrap'>{client_status}</span>"
        if client_status
        else ""
    )
    st.markdown(
        f"""
        <div class="metric-card" style="margin-bottom:0.6rem">
            <div style="display:flex;justify-content:space-between;align-items:center;gap:0.5rem;flex-wrap:wrap">
                <div>
                    <div style="font-size:0.72rem;color:var(--text-muted);font-weight:500;text-transform:uppercase;letter-spacing:0.04em">Cliente</div>
                    <div style="font-size:1.05rem;font-weight:700;color:var(--text)">{client_name}</div>
                </div>
                <div style="display:flex;gap:0.5rem;align-items:center;flex-wrap:wrap">
                    <span class="badge badge-blue" style="white-space:nowrap">Processo: {client_process}</span>
                    {badge_status_html}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    base_info_cols = st.columns(3)
    with base_info_cols[0]:
        st.caption(f"RG: {client_rg or 'Não informado'}")
    with base_info_cols[1]:
        st.caption(f"CPF: {client_cpf or 'Não informado'}")
    with base_info_cols[2]:
        st.caption(f"Artigo/Imputação: {client_article or 'Não informado'}")

    with st.expander("Editar dados do cliente"):
        c1, c2, c3 = st.columns(3)
        with c1:
            nome = st.text_input("Nome", value=client_name, key="edit_nome")
        with c2:
            rg = st.text_input("RG", value=client_rg, key="edit_rg")
        with c3:
            cpf = st.text_input("CPF", value=client_cpf, key="edit_cpf")
        c4, c5, c6 = st.columns(3)
        with c4:
            artigo = st.text_input("Artigo/Imputação", value=client_article, key="edit_artigo")
        with c5:
            status = st.text_input("Status", value=client_status, key="edit_status")
        with c6:
            numero_processo = st.text_input("Número do Processo", value=default_process_number, key="edit_processo")
        if st.button("Salvar dados", key="btn_save_meta"):
            try:
                updated = dict(case_meta)
                updated["nome"] = nome
                updated["rg"] = rg
                updated["cpf"] = cpf
                updated["artigo"] = artigo
                updated["status"] = status
                updated["numero_processo"] = numero_processo
                with open(meta_path, "w", encoding="utf-8") as f:
                    json.dump(updated, f, ensure_ascii=False, indent=2)
                st.success("Dados atualizados.")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

    # FEATURE 8: Alerta de Prazos
    deadlines = load_deadlines(case_path)
    urgent = []
    for dl in deadlines:
        try:
            dt = datetime.datetime.strptime(dl["date"], "%Y-%m-%d")
            diff = (dt - datetime.datetime.now()).days
            if 0 <= diff <= 2:
                urgent.append(dl)
        except Exception:
            continue

    if urgent:
        for u in urgent:
            st.markdown(f"""
            <div class="metric-card deadline-alert" style="border-color: var(--red); margin: 0.5rem 0;">
                <span class="badge badge-red" style="font-size: 0.85rem; padding: 4px 12px;">🚨 PRAZO URGENTE</span>
                &nbsp;&nbsp;<strong>{u['label']}</strong> — {u['date']}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    # KPI Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Risco", "ALTO", delta="Preventiva Ativa", delta_type="down")
    with c2:
        metric_card("Isonomia", "5 Soltos", delta="Art. 580 CPP", delta_type="up")
    with c3:
        metric_card("Fase", "HC TJRJ", delta="Aguardando Pauta", delta_type="warn")
    with c4:
        metric_card("Prazo", "30d", delta="Excesso Prazo", delta_type="warn")

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # TABS (Todas as Features)
    # ══════════════════════════════════════════════════════════════
    (
        tab_vis,
        tab_teia,
        tab_chat,
        tab_pecas,
        tab_docs,
        tab_prazos,
        tab_juiz,
        tab_export,
        tab_busca_docs,
    ) = st.tabs([
        "📊 Visão Estratégica",
        "🕸️ Teia Investigativa",
        "🤖 Chat IA",
        "📝 Gerador de Peças",
        "📁 Documentos",
        "⏰ Prazos",
        "👨‍⚖️ Perfil Magistrado",
        "📄 Exportar Dossiê",
        "🔎 Busca nos Documentos",
    ])

    # ── TAB BUSCA NOS DOCUMENTOS ─────────────────────────────────
    docs_search_dir = os.path.join(case_path, "documentos_processo")
    try:
        from scripts.search_docs import search_docs as _sd
        HAVE_SEARCH = True
    except Exception:
        HAVE_SEARCH = False
        _sd = None

    if HAVE_SEARCH and tab_busca_docs is not None and docs_search_dir and os.path.exists(docs_search_dir):
        with tab_busca_docs:
            st.markdown(f"""
            <div class="chart-wrap">
                <div class="chart-title">Busca Textual em {os.path.basename(docs_search_dir)}</div>
                <div class="chart-subtitle">Filtra trechos relevantes em .txt / .html / .pdf</div>
            </div>
            """, unsafe_allow_html=True)

            q = st.text_input("Termo de busca", key="docs_search_q")
            if st.button("Buscar", key="btn_docs_search") and q.strip():
                st.session_state["_docs_search_active"] = q.strip()
                st.rerun()

            query = st.session_state.get("_docs_search_active", "").strip()
            if query:
                try:
                    hits = _sd(docs_search_dir, query, max_results=30)
                except Exception as search_err:
                    hits = []
                    st.warning(f"Falha na busca: {search_err}")

                if not hits:
                    st.caption("Nenhum trecho encontrado.")
                else:
                    st.caption(f"{len(hits)} resultado(s) relevante(s).")
                    for hit in hits:
                        st.markdown(f"""
                        <div class="metric-card" style="margin-bottom:.5rem">
                            <div style="display:flex;justify-content:space-between;align-items:center;gap:.5rem">
                                <strong style="font-size:.82rem;color:var(--text);word-break:break-all">{hit['name']}</strong>
                                <span class="badge badge-blue" style="white-space:nowrap">{hit['relevance']}%</span>
                            </div>
                            <div style="font-size:.78rem;color:var(--text-muted);margin-top:.4rem">{hit['snippet']}</div>
                        </div>
                        """, unsafe_allow_html=True)

    # ── TAB 1: VISÃO ESTRATÉGICA ────────────────────────────────
with tab_vis:
    col_tl, col_table = st.columns([6, 4])
    
    with col_tl:
        st.markdown("""<div class="chart-wrap">
            <div class="chart-title">Linha do Tempo do Processo</div>
            <div class="chart-subtitle">FEATURE 4: Editável via timeline.json</div>""", unsafe_allow_html=True)
        
        timeline = load_timeline(case_path)
        dates = [e["date"] for e in timeline]
        events = [e["event"] for e in timeline]
        
        fig = go.Figure(go.Scatter(
            x=dates, y=[1]*len(dates),
            mode="lines+markers+text", text=events, textposition="top center",
            marker=dict(size=14, color="#2563eb" if not IS_DARK else "#3b82f6"),
            line=dict(color="#2563eb" if not IS_DARK else "#3b82f6", width=2)
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans, sans-serif", color="#71717a" if not IS_DARK else "#a1a1aa", size=10),
            margin=dict(l=10, r=10, t=30, b=10), height=230,
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.5, 1.6]),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        
        # Editor da timeline
        with st.expander("✏️ Editar Linha do Tempo"):
            new_date = st.text_input("Data (AAAA-MM)", key="tl_date")
            new_event = st.text_input("Evento", key="tl_event")
            if st.button("Adicionar Evento") and new_date and new_event:
                timeline.append({"date": new_date, "event": new_event})
                timeline.sort(key=lambda x: x["date"])
                save_timeline(case_path, timeline)
                st.success("Evento adicionado!")
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

    with col_table:
        st.markdown("""<div class="chart-wrap">
            <div class="chart-title">Situação dos Corréus</div>
            <div class="chart-subtitle">Status prisional comparativo</div>""", unsafe_allow_html=True)
        
        rows = """
        <tr><td>Guilherme (218g)</td><td><span class="badge badge-green">Solto</span></td></tr>
        <tr><td>Rodrigo (Corréu)</td><td><span class="badge badge-green">Solto</span></td></tr>
        <tr><td>Corréu 3</td><td><span class="badge badge-green">Solto</span></td></tr>
        <tr><td>Corréu 4</td><td><span class="badge badge-green">Solto</span></td></tr>
        <tr><td>Corréu 5</td><td><span class="badge badge-green">Solto</span></td></tr>
        <tr><td><strong>Júlio Marcos</strong></td><td><span class="badge badge-red">Preso</span></td></tr>
        """
        st.markdown(f"""<table class="data-table">
            <thead><tr><th>Réu</th><th>Status</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # FEATURE 2: Detector de Contradições
    st.markdown("""<div class="chart-wrap">
        <div class="chart-title">🔍 Detector de Contradições (IA)</div>
        <div class="chart-subtitle">FEATURE 2: Varre depoimentos cruzando versões automaticamente</div>""", unsafe_allow_html=True)
    
    if st.button("Executar Análise de Contradições", key="btn_contradictions"):
        with st.spinner("DeepSeek analisando documentos em busca de contradições..."):
            try:
                from scripts.ai_engine import detect_contradictions
                result = detect_contradictions(case_path)
                st.markdown(result)
                # Salvar resultado
                os.makedirs(os.path.join(case_path, "analises"), exist_ok=True)
                with open(os.path.join(case_path, "analises", "Contradicoes_Detectadas.md"), "w", encoding="utf-8") as f:
                    f.write(result)
                st.success("Relatório salvo em analises/Contradicoes_Detectadas.md")
            except Exception as e:
                st.error(f"Erro: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

# ── TAB 2: TEIA INVESTIGATIVA ────────────────────────────────
with tab_teia:
    st.markdown("""<div class="chart-wrap">
        <div class="chart-title">Mapa Investigativo (PyVis)</div>
        <div class="chart-subtitle">Grafo interativo: passe o mouse sobre os nos para ver detalhes taticos. Arraste para reorganizar.</div>""", unsafe_allow_html=True)
    
    teia_path = os.path.join(case_path, "analises", "Teia_Tatica_Defesa.html")
    if os.path.exists(teia_path):
        with open(teia_path, "r", encoding="utf-8", errors="ignore") as f:
            components.html(f.read(), height=600, scrolling=False)
    else:
        st.info("Teia nao gerada ainda.")
    
    if st.button("🔄 Regenerar Teia Investigativa", key="btn_regen_teia"):
        with st.spinner("Reconstruindo grafo investigativo..."):
            try:
                from scripts.investigative_graphs import build_investigative_graph
                build_investigative_graph(case_path)
                st.success("Teia regenerada!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ── TAB 3: CHAT IA REAL ─────────────────────────────────────
with tab_chat:
    st.markdown("""<div class="chart-wrap">
        <div class="chart-title">Chat Investigativo (DeepSeek)</div>
        <div class="chart-subtitle">FEATURE 1: Responde com base nos documentos reais do caso</div>""", unsafe_allow_html=True)
    
    if not st.session_state.messages:
        st.session_state.messages = [{"role": "assistant", "content": f"Olá, Doutor. Estou conectado aos documentos do caso de **{client_display}**. O que deseja saber sobre os autos?"}]
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if prompt := st.chat_input("Pergunte algo sobre o caso..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Consultando documentos do caso via DeepSeek..."):
                try:
                    from scripts.ai_engine import chat_with_case
                    response = chat_with_case(prompt, case_path)
                except Exception as e:
                    response = f"Erro na conexão com DeepSeek: {e}"
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.markdown("</div>", unsafe_allow_html=True)

# ── TAB 4: GERADOR DE PEÇAS ─────────────────────────────────
with tab_pecas:
    st.markdown("""<div class="chart-wrap">
        <div class="chart-title">Gerador Automático de Peças Processuais</div>
        <div class="chart-subtitle">FEATURE 3: HC, Resposta à Acusação e Alegações Finais via DeepSeek</div>""", unsafe_allow_html=True)
    
    piece_type = st.selectbox("Tipo de Peça", ["Habeas Corpus", "Resposta à Acusação", "Alegações Finais"])
    facts_input = st.text_area("Fatos do Caso (complemente se necessário)", height=120,
                               placeholder="Descreva ou cole os fatos relevantes para a peça...", key="facts_piece")
    
    if st.button("⚡ Gerar Peça com DeepSeek", use_container_width=True, key="btn_gen_piece"):
        with st.spinner(f"DeepSeek redigindo {piece_type}... (pode levar 15-30 segundos)"):
            try:
                from scripts.ai_engine import generate_legal_piece
                piece = generate_legal_piece(piece_type, client_display, facts_input, case_path)
                st.markdown(piece)
                
                # Salvar
                filename = piece_type.replace(" ", "_").replace("à", "a") + ".md"
                os.makedirs(os.path.join(case_path, "pecas"), exist_ok=True)
                with open(os.path.join(case_path, "pecas", filename), "w", encoding="utf-8") as f:
                    f.write(piece)
                st.success(f"Peça salva em pecas/{filename}")
            except Exception as e:
                st.error(f"Erro: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ── TAB 5: DOCUMENTOS (Upload + Leitor PDF) ─────────────────
with tab_docs:
    col_upload, col_reader = st.columns(2)
    
    with col_upload:
        st.markdown("""<div class="chart-wrap">
            <div class="chart-title">Upload de Documentos</div>
            <div class="chart-subtitle">FEATURE 5: Arraste arquivos para a pasta do cliente</div>""", unsafe_allow_html=True)
        
        doc_type = st.selectbox("Destino", ["documentos_processo", "analises", "pecas"], key="doc_dest")
        uploaded = st.file_uploader("Arraste PDFs, áudios ou vídeos aqui", accept_multiple_files=True, key="uploader")
        
        if uploaded:
            dest_dir = os.path.join(case_path, doc_type)
            os.makedirs(dest_dir, exist_ok=True)
            for f in uploaded:
                filepath = os.path.join(dest_dir, f.name)
                with open(filepath, "wb") as out:
                    out.write(f.getbuffer())
                st.success(f"✅ {f.name} salvo em {doc_type}/")
        
        # Listar arquivos existentes
        st.markdown("**Arquivos na pasta:**")
        docs_dir = os.path.join(case_path, "documentos_processo")
        if os.path.exists(docs_dir):
            files = os.listdir(docs_dir)
            if files:
                for f in files[:20]:
                    ext = os.path.splitext(f)[1].lower()
                    icon = "📄" if ext == ".pdf" else "🎵" if ext in [".mp3",".mp4",".wav"] else "📎"
                    st.markdown(f"{icon} `{f}`")
            else:
                st.caption("Nenhum arquivo ainda.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_reader:
        st.markdown("""<div class="chart-wrap">
            <div class="chart-title">Leitor de PDF com IA</div>
            <div class="chart-subtitle">FEATURE 6: Extração automática de fatos-chave</div>""", unsafe_allow_html=True)
        
        pdf_file = st.file_uploader("Envie um PDF para análise", type=["pdf"], key="pdf_reader")
        
        if pdf_file:
            # Salvar temporariamente
            temp_path = os.path.join(case_path, "documentos_processo", pdf_file.name)
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            with open(temp_path, "wb") as out:
                out.write(pdf_file.getbuffer())
            
            if st.button("🔍 Extrair Fatos com DeepSeek", key="btn_extract"):
                with st.spinner("Lendo PDF e extraindo fatos-chave..."):
                    try:
                        from scripts.ai_engine import extract_pdf_facts
                        result = extract_pdf_facts(temp_path)
                        st.markdown(result)
                        
                        # Salvar resultado
                        result_path = os.path.join(case_path, "analises", f"Fatos_{pdf_file.name.replace('.pdf', '')}.md")
                        os.makedirs(os.path.dirname(result_path), exist_ok=True)
                        with open(result_path, "w", encoding="utf-8") as f:
                            f.write(result)
                        st.success("Fatos extraídos e salvos na pasta analises/")
                    except Exception as e:
                        st.error(f"Erro: {e}")
        
        st.markdown("</div>", unsafe_allow_html=True)

    # ── ATUALIZAÇÃO TJRJ (dentro da aba Documentos) ──
    st.markdown("""
    <div class="chart-wrap">
        <div class="chart-title">Atualização Eletrônica TJRJ</div>
        <div class="chart-subtitle">Importa movimentos processuais diretamente do TJRJ via Playwright</div>
    </div>
    """, unsafe_allow_html=True)

    process_number_tjrj = st.text_input("Número do Processo TJRJ", value=default_process_number, placeholder="Ex: 0011857-95.2021.8.19.0002", key="tjrj_process_number")
    if st.button("Abrir Extrator TJRJ", key="btn_open_tjrj"):
        if not process_number_tjrj.strip():
            st.warning("Informe o número do processo para abrir o extrator.")
        else:
            from scripts.tjrj_extractor import extract_tjrj
            try:
                save_dir = os.path.join(case_path, "documentos_processo")
                with st.spinner("Abrindo extrator TJRJ..."):
                    result = extract_tjrj(process_number_tjrj.strip(), save_dir)
                st.success("Extração finalizada.")
                st.text(result)
            except RuntimeError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Erro ao abrir extrator: {e}")

# ── TAB 6: PRAZOS PROCESSUAIS ────────────────────────────────
with tab_prazos:
    st.markdown("""<div class="chart-wrap">
        <div class="chart-title">Controle de Prazos Processuais</div>
        <div class="chart-subtitle">FEATURE 8: Alertas visuais quando faltar menos de 48h</div>""", unsafe_allow_html=True)
    
    deadlines = load_deadlines(case_path)
    
    # Exibir prazos existentes
    if deadlines:
        for i, dl in enumerate(deadlines):
            try:
                dt = datetime.datetime.strptime(dl["date"], "%Y-%m-%d")
                diff = (dt - datetime.datetime.now()).days
                if diff < 0:
                    badge = '<span class="badge badge-red">VENCIDO</span>'
                elif diff <= 2:
                    badge = '<span class="badge badge-red deadline-alert">⚠️ URGENTE</span>'
                elif diff <= 7:
                    badge = '<span class="badge badge-amber">PRÓXIMO</span>'
                else:
                    badge = '<span class="badge badge-green">OK</span>'
            except:
                badge = '<span class="badge badge-blue">—</span>'
                diff = "?"
            
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div class="metric-label">{dl.get('label', 'Prazo')}</div>
                    <div style="font-family: 'JetBrains Mono'; font-size: 0.9rem; color: var(--text);">{dl['date']}</div>
                </div>
                <div>{badge} &nbsp; <span style="color: var(--text-muted); font-size: 0.75rem;">{diff}d</span></div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("Nenhum prazo cadastrado.")
    
    # Adicionar prazo
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("➕ Adicionar Novo Prazo"):
        dl_label = st.text_input("Descrição do Prazo", placeholder="Ex: Prazo para Alegações Finais")
        dl_date = st.date_input("Data Limite")
        if st.button("Salvar Prazo", key="btn_save_dl"):
            deadlines.append({"label": dl_label, "date": dl_date.strftime("%Y-%m-%d")})
            deadlines.sort(key=lambda x: x["date"])
            save_deadlines(case_path, deadlines)
            st.success("Prazo salvo!")
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# ── TAB 7: PERFIL DO MAGISTRADO ──────────────────────────────
with tab_juiz:
    st.markdown("""<div class="chart-wrap">
        <div class="chart-title">Análise do Perfil do Magistrado</div>
        <div class="chart-subtitle">FEATURE 7: Análise tática via DeepSeek para ajustar a estratégia de defesa</div>""", unsafe_allow_html=True)
    
    judge_name = st.text_input("Nome do Juiz ou Desembargador", placeholder="Ex: Des. Fulano de Tal — 3ª Câmara Criminal TJRJ")
    
    if st.button("🔍 Analisar Perfil Tático", key="btn_judge") and judge_name:
        with st.spinner("DeepSeek analisando perfil do magistrado..."):
            try:
                from scripts.ai_engine import analyze_judge_profile
                profile = analyze_judge_profile(judge_name)
                st.markdown(profile)
                
                # Salvar
                os.makedirs(os.path.join(case_path, "analises"), exist_ok=True)
                with open(os.path.join(case_path, "analises", f"Perfil_Magistrado.md"), "w", encoding="utf-8") as f:
                    f.write(profile)
                st.success("Perfil salvo em analises/Perfil_Magistrado.md")
            except Exception as e:
                st.error(f"Erro: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ── TAB 8: EXPORTAR DOSSIÊ PDF ───────────────────────────────
with tab_export:
    st.markdown("""<div class="chart-wrap">
        <div class="chart-title">Exportar Dossiê Completo (PDF)</div>
        <div class="chart-subtitle">FEATURE 9: Compila análises + peças num PDF com capa profissional</div>""", unsafe_allow_html=True)
    
    st.markdown("""
    O sistema irá compilar automaticamente **todos os arquivos `.md` e `.txt`** das pastas 
    `analises/` e `pecas/` num único PDF formatado com capa profissional, pronto para 
    entregar ao Desembargador ou imprimir para o julgamento.
    """)
    
    if st.button("📄 Gerar Dossiê em PDF", use_container_width=True, key="btn_dossier"):
        with st.spinner("Compilando dossiê profissional..."):
            try:
                from scripts.pdf_export import generate_dossier
                output = generate_dossier(client_display, case_path)
                st.success(f"✅ Dossiê gerado: `{os.path.basename(output)}`")
                
                # Oferecer download
                with open(output, "rb") as pdf_file:
                    st.download_button(
                        "⬇️ Baixar Dossiê PDF",
                        data=pdf_file.read(),
                        file_name=os.path.basename(output),
                        mime="application/pdf",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Erro ao gerar PDF: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)
