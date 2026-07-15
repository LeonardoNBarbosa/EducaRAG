import streamlit as st
from app.config import get_secrets, MENSAGEM_INICIAL
from app.rag import inicializar_index, criar_chat_engine
from app.ui import injetar_css, renderizar_header, renderizar_sidebar, renderizar_mensagem_usuario

st.set_page_config(
    page_title="EducaRAG",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

injetar_css()
renderizar_sidebar()
renderizar_header()

secrets = get_secrets()

with st.spinner("Conectando à base de conhecimento..."):
    index = inicializar_index(
        groq_key=secrets["groq"],
        qdrant_key=secrets["qdrant"],
    )

if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {"role": "assistant", "content": MENSAGEM_INICIAL}
    ]

if "chat_engine" not in st.session_state:
    st.session_state.chat_engine = criar_chat_engine(index)

for mensagem in st.session_state.mensagens:
    if mensagem["role"] == "user":
        renderizar_mensagem_usuario(mensagem["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(mensagem["content"])

if prompt := st.chat_input("Pergunte sobre educação inclusiva, PEIs, legislação..."):
    st.session_state.mensagens.append({"role": "user", "content": prompt})
    renderizar_mensagem_usuario(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Buscando nos documentos oficiais..."):
            stream = st.session_state.chat_engine.stream_chat(prompt)
            resposta = st.write_stream(stream.response_gen)

    st.session_state.mensagens.append({"role": "assistant", "content": resposta})