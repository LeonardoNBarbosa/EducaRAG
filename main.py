import os
import streamlit as st
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

# Configurações da página com streamlit
st.set_page_config(
    page_title="EducaRAG", 
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

# Cria o chat e o inicializa com uma mensagem
if "mensagens" not in st.session_state.keys():
    st.session_state.mensagens = [
        {"role": "assistant", "content": "Olá! Qual o plano para hoje?"}
    ]

# Usado apenas para indexar o primeiro carregamento
# Settings.embed_model = HuggingFaceEmbedding( 
#     model_name="BAAI/bge-m3"
# )


# def primeiro_carregamento():
#     documentos = SimpleDirectoryReader(input_dir="./data/pdfs/").load_data() # Verificar sobre quantidade de chunks

#     db = chromadb.PersistentClient(path="./data/chroma_db")
#     chroma_collection = db.get_or_create_collection("educa-rag")
#     vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
#     storage_context = StorageContext.from_defaults(vector_store=vector_store)

#     index = VectorStoreIndex.from_documents(
#         documentos,
#         storage_context=storage_context,
#         embed_model=Settings.embed_model
#     )

#     return index

# Buscando os dados no Qdrant, depois dos documentos já indexados
@st.cache_resource(show_spinner=False) # TODO: documentar o que faz
def carregamento_definitivo():

    vector_store = ChromaVectorStore(
        persist_dir="data/chroma_db"
    )

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    index = load_index_from_storage(storage_context)

    return index

index = carregamento_definitivo()

# TODO colocar sistema de prompts
Settings.llm = Groq(
    model="llama-3.3-70b-versatile",
    api_key=os.environ["GROQ_API_KEY"]
)

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