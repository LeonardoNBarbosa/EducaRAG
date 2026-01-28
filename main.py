import os
import streamlit as st
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
# import google.generativeai as genai
# from llama_index.llms.google_genai import GoogleGenAI
# from llama_index.vector_stores.qdrant import QdrantVectorStore
# import qdrant_client

# Configurações da página com streamlit
st.set_page_config(
    page_title="EducaRAG", # HELPei / PEIeduca / EducaRAG / PEInsina 
    page_icon="🦉",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

st.title("EducaRAG")
st.info("O assistente irá ajuda-lo a gerar PEIs (Plano de Ensino Individualizado) para seus alunos de forma rápida e eficiente.")

# Definição das chaves API
groq_chave = st.secrets["GROQ_CHAVE"]
os.environ["GROQ_API_KEY"] = groq_chave
# gemini_chave = st.secrets["GEMINI_CHAVE"]
# os.environ["GOOGLE_API_KEY"] = gemini_chave
# qdrant_chave = st.secrets["QDRANT_CHAVE"]

# Cria o chat e o inicializa com uma mensagem
if "mensagens" not in st.session_state.keys():
    st.session_state.mensagens = [
        {"role": "assistant", "content": "Olá! Qual o plano para hoje?"}
    ]

# # Conexão ao Qdrant
# def conectar_qdrant():
#     client = qdrant_client.QdrantClient(
#         url="https://8835eb45-4030-4fe5-a813-76dd1889393e.us-east4-0.gcp.cloud.qdrant.io:6333",
#         api_key=qdrant_chave
#     )
#     return client

Settings.llm = Groq(
    model="llama-3.3-70b-versatile",
    api_key=os.environ["GROQ_API_KEY"]
)

Settings.embed_model = HuggingFaceEmbedding( 
    model_name="BAAI/bge-m3"
)

def primeiro_carregamento():
    documentos = SimpleDirectoryReader(input_dir="./data/pdfs/").load_data() # Verificar sobre quantidade de chunks
    
    # client = conectar_qdrant()

    # # Definindo o vector store para armazenar os dados indexados
    # vector_store = QdrantVectorStore(client=client, collection_name='chatbot-pei')

    # storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # # Carregando e fazendo indexação dos documentos pela primeira vez e armazenando no vector store do Qdrant
    # index = VectorStoreIndex.from_documents(documentos, storage_context=storage_context, embed_model=Settings.embed_model)
    # return index

    db = chromadb.PersistentClient(path="./data/chroma_db")
    chroma_collection = db.get_or_create_collection("educa-rag")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documentos,
        storage_context=storage_context,
        embed_model=Settings.embed_model
    )

    return index

# Buscando os dados no Qdrant, depois dos documentos já indexados
@st.cache_resource(show_spinner=False) # TODO: documentar o que faz
def carregamento_definitivo():
    # client = conectar_qdrant()

    # Alteração dos modelos de LLM e embedding do llama-index
    # TODO: Testar outras LLMs e embed models para verificar melhora nas respotas
    # TODO: Verificar temperatura e max tokens
    # Settings.llm = GoogleGenAI(
    #     model="gemini-2.0-flash",
    #     #system_prompt="" # TODO colocar sistema de prompts
    # )

    # vector_store = QdrantVectorStore(client=client, collection_name='chatbot-pei')

    # index = VectorStoreIndex.from_vector_store(vector_store, embed_model=Settings.embed_model)
    # return index

    db2 = chromadb.PersistentClient(path="./data/chroma_db")
    chroma_collection = db2.get_or_create_collection("educa-rag")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    index = VectorStoreIndex.from_vector_store(
        vector_store, 
        embed_model=Settings.embed_model
    )

    return index

index = carregamento_definitivo()
# index = carregamento_definitivo()

# Inicializa o chat engine com st_session_state
if "chat_engine" not in st.session_state.keys():
    # TODO: testar chat engine com outras parametrizações
    st.session_state.chat_engine = index.as_chat_engine(
        chat_mode="condense_question", 
        verbose=True,
        streaming=True,
        llm=Settings.llm
    )

# Prompt para inserção do usuário e salva no histórico
if prompt := st.chat_input(
    "Digite aqui"
): 
    st.session_state.mensagens.append({"role": "user", "content": prompt})

for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["role"]):
        st.write(mensagem["content"])

# Se a última mensagem não for do assistente, gere uma nova resposta
if st.session_state.mensagens[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            resposta_stream = st.session_state.chat_engine.stream_chat(prompt)

            st.write_stream(resposta_stream.response_gen)

            mensagem = {"role": "assistant", "content": resposta_stream.response}

            st.session_state.mensagens.append(mensagem)
else:
    pass