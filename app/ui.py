"""
Módulo de interface - CSS customizado, sidebar e componentes visuais.
"""

import streamlit as st

def injetar_css() -> None:
    """Injeta CSS customizado no app Streamlit."""
    st.markdown(
        """
        <style>
        /* ── Importação de fontes ── */
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=Inter:wght@300;400;500&display=swap');

        /* ── Variáveis de cor ── */
        :root {
            --azul-profundo:    #0D2856;
            --azul-medio:       #1A4299;
            --verde-ia:         #3CCEA5;
            --azul-claro:       #4A85E8;
            --ciano:            #22D3EE;
            --roxo-suave:       #818CF8;
            --fundo:            #F3F6FC;
            --branco:           #FFFFFF;

            --cor-borda:        #D1DCF0;
            --cor-texto:        #0D2856;
            --cor-texto-muted:  #5A7AAF;
            --cor-user-bg:      #E8F0FC;
            --radius:           12px;
            --sombra:           0 2px 16px rgba(13,40,86,0.09);
        }

        /* ── App geral ── */
        .stApp {
            background-color: var(--fundo) !important;
        }

        /* ── Centralizar conteúdo ──
           .block-container é o seletor mais compatível entre versões do Streamlit */
        .block-container {
            max-width: 780px !important;
            margin-left: auto !important;
            margin-right: auto !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            padding-top: 1rem !important;
        }

        /* ── Limitar largura do input ao mesmo tamanho do chat ── */
        [data-testid="stBottom"] {
            max-width: 1000px !important;
            margin-left: auto !important;
            margin-right: auto !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }

        /* ── Header ── */
        .edu-header {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 24px 0 10px 0;
            border-bottom: 2px solid var(--cor-borda);
            margin-bottom: 20px;
        }
        .edu-header .logo {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, var(--azul-profundo), var(--azul-medio));
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            box-shadow: 0 4px 14px rgba(26,66,153,0.30);
            flex-shrink: 0;
        }
        .edu-header h1 {
            font-family: 'Sora', sans-serif;
            font-size: 1.85rem;
            font-weight: 700;
            color: var(--azul-profundo);
            margin: 0;
            letter-spacing: -0.5px;
        }
        .edu-header p {
            font-size: 0.84rem;
            color: var(--cor-texto-muted);
            margin: 3px 0 0 0;
        }

        /* ── Badge de status ── */
        .badge-rag {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            background: linear-gradient(90deg, #E2F8F2, #E8F0FF);
            color: var(--azul-medio);
            border: 1px solid #B8D8F0;
            border-radius: 20px;
            padding: 5px 14px;
            font-size: 0.75rem;
            font-weight: 500;
            margin-bottom: 18px;
            letter-spacing: 0.01em;
        }
        .badge-dot {
            width: 7px;
            height: 7px;
            background: var(--verde-ia);
            border-radius: 50%;
            animation: pulsar 2s infinite;
        }
        @keyframes pulsar {
            0%, 100% { opacity: 1; transform: scale(1); }
            50%       { opacity: 0.5; transform: scale(1.35); }
        }

        /* ── Mensagem do assistente — esquerda, fundo branco ── */
        [data-testid="stChatMessage"] {
            border-radius: var(--radius) !important;
            padding: 4px 10px !important;
            margin-bottom: 6px !important;
            border: 1px solid var(--cor-borda) !important;
            background-color: var(--branco) !important;
            box-shadow: var(--sombra) !important;
            margin-right: 12% !important;
        }

        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] span,
        [data-testid="stChatMessage"] li,
        [data-testid="stChatMessage"] strong,
        [data-testid="stChatMessage"] em,
        [data-testid="stChatMessage"] h1,
        [data-testid="stChatMessage"] h2,
        [data-testid="stChatMessage"] h3 {
            color: var(--cor-texto) !important;
        }

        /* ── Mensagem do usuário — direita, fundo azul (HTML customizado) ── */
        .user-msg-row {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 10px;
            margin-left: 12%;
        }
        .user-msg-bubble {
            background-color: var(--azul-medio);
            color: #FFFFFF;
            border-radius: var(--radius);
            border-bottom-right-radius: 3px;
            padding: 10px 16px;
            font-size: 0.95rem;
            line-height: 1.55;
            max-width: 100%;
            word-break: break-word;
        }
        .user-msg-bubble p {
            margin: 0;
            color: #FFFFFF;
        }

        /* ── Input de chat ── */
        [data-testid="stChatInput"] {
            border-radius: 10px !important;
            border: 2px solid var(--cor-borda) !important;
            background-color: var(--azul-medio) !important;
            box-shadow: var(--sombra) !important;
            transition: border-color 0.2s;
        }
        [data-testid="stChatInput"]:focus-within {
            border-color: var(--azul-claro) !important;
        }

        /* ── Sidebar escura ── */
        [data-testid="stSidebar"] {
            background-color: var(--azul-profundo) !important;
            border-right: none !important;
        }
        [data-testid="stSidebar"] > div {
            background-color: var(--azul-profundo) !important;
        }
        [data-testid="stSidebar"] * {
            color: #CBD8F0 !important;
        }

        .sidebar-titulo {
            font-family: 'Sora', sans-serif;
            font-size: 1.30rem;
            font-weight: 700;
            color: var(--branco) !important;
            padding: 20px 0 16px 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .sidebar-secao {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: var(--radius);
            padding: 14px 16px;
            margin-bottom: 10px;
        }
        .sidebar-secao h4 {
            font-family: 'Sora', sans-serif;
            font-size: 0.80rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.10em;
            color: var(--verde-ia) !important;
            margin: 0 0 10px 0;
        }
        .sidebar-item {
            display: flex;
            align-items: flex-start;
            gap: 8px;
            font-size: 0.90rem;
            color: #A8C0E8 !important;
            padding: 4px 0;
            line-height: 1.45;
        }
        .sidebar-item span:first-child {
            font-size: 1rem;
            margin-top: 1px;
            flex-shrink: 0;
        }

        [data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.12) !important;
            margin: 10px 0;
        }

        /* ── Botão limpar ── */
        .stButton > button {
            width: 100%;
            background: rgba(255,255,255,0.06) !important;
            border: 1.5px solid rgba(255,255,255,0.15) !important;
            color: #A8C0E8 !important;
            border-radius: 10px;
            font-size: 0.82rem;
            padding: 7px 5px;
            transition: all 0.2s;
        }
        .stButton > button:hover {
            background: rgba(220,60,60,0.18) !important;
            border-color: rgba(220,80,80,0.45) !important;
            color: #FF9090 !important;
        }

        /* ── Spinner ── */
        .stSpinner > div {
            border-top-color: var(--azul-claro) !important;
        }

        /* ── Scrollbar ── */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: var(--cor-borda); border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--cor-texto-muted); }
        </style>
        """,
        unsafe_allow_html=True,
    )

def renderizar_header() -> None:
    """Renderiza o cabeçalho do app."""
    st.markdown(
        """
        <div class="edu-header">
            <div class="logo">📚</div>
            <div>
                <h1>EducaRAG</h1>
                <p>Assistente de Educação Inclusiva Brasileira</p>
            </div>
        </div>
        <div class="badge-rag">
            <span class="badge-dot"></span>
            Respostas baseadas em documentos oficiais · RAG ativo
        </div>
        """,
        unsafe_allow_html=True,
    )

def renderizar_sidebar() -> None:
    """Renderiza o conteúdo da sidebar."""
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-titulo">📚 EducaRAG</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="sidebar-secao">
                <h4>O que posso fazer</h4>
                <div class="sidebar-item"><span>📋</span><span>Gerar PEIs estruturados</span></div>
                <div class="sidebar-item"><span>⚖️</span><span>Explicar legislação educacional</span></div>
                <div class="sidebar-item"><span>💡</span><span>Sugestões pedagógicas inclusivas</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="sidebar-secao">
                <h4>Como funciona</h4>
                <div class="sidebar-item">
                    <span>🔍</span>
                    <span>Busca em documentos oficiais brasileiros via RAG</span>
                </div>
                <div class="sidebar-item">
                    <span>🚫</span>
                    <span>Não inventa informações — só usa o que está nos documentos</span>
                </div>
                <div class="sidebar-item">
                    <span>📌</span>
                    <span>Cita as fontes sempre que possível</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="sidebar-secao">
                <h4>Dicas de uso</h4>
                <div class="sidebar-item">
                    <span>✏️</span>
                    <span>Para PEIs, informe diagnóstico, série e dificuldades do aluno</span>
                </div>
                <div class="sidebar-item">
                    <span>📎</span>
                    <span>Quanto mais contexto você der, melhor a resposta</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        if st.button("🗑️ Limpar conversa"):
            st.session_state.pop("mensagens", None)
            st.session_state.pop("chat_engine", None)
            st.rerun()

        st.markdown(
            "<p style='font-size:0.72rem; color:#5A7AAF !important; "
            "text-align:center; margin-top:16px;'>"
            "EducaRAG · Educação Inclusiva BR<br>Powered by Leonardo"
            "</p>",
            unsafe_allow_html=True,
        )

def renderizar_mensagem_usuario(texto: str) -> None:
    """Renderiza mensagem do usuário alinhada à direita com fundo azul."""
    st.markdown(
        f'<div class="user-msg-row">'
        f'<div class="user-msg-bubble">{texto}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )