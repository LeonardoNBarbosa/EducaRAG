import os
import streamlit as st
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.core import Settings
from llama_index.core import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.vector_stores.qdrant import QdrantVectorStore
import qdrant_client

# Configurações da página com streamlit
st.set_page_config(
    page_title="EducaRAG", 
    page_icon="🦉",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

st.title("🦉 EducaRAG")
st.info("O assistente irá ajuda-lo a gerar PEIs (Plano Educacional Individualizado) para seus alunos de forma rápida e eficiente.")

# Definição das chaves API
groq_chave = st.secrets["GROQ_CHAVE"]
qdrant_chave = st.secrets["QDRANT_CHAVE"]

# Cria o chat e o inicializa com uma mensagem
if "mensagens" not in st.session_state.keys():
    st.session_state.mensagens = [
        {"role": "assistant", "content": "Olá! Qual o plano para hoje?"}
    ]

def conectar_qdrant():
    client = qdrant_client.QdrantClient(
        url="https://ab974ce8-55d9-44d7-9250-eff6f00333e0.sa-east-1-0.aws.cloud.qdrant.io",
        api_key=qdrant_chave,
        check_compatibility=False,
    )
    return client

Settings.llm = Groq(
    model="llama-3.3-70b-versatile",
    api_key=groq_chave
)

Settings.embed_model = HuggingFaceEmbedding( 
    model_name="BAAI/bge-m3",
    device="cpu",
    embed_batch_size=10,
    model_kwargs={
        "trust_remote_code": True,
        "low_cpu_mem_usage": False
    }
)

Settings.node_parser = SentenceSplitter(
    chunk_size=512, 
    chunk_overlap=50
)

@st.cache_resource(show_spinner=False)
def inicializar_index():
    client = conectar_qdrant()
    COLLECTION_NAME = "EducaRAG-v2"

    # Verifica se a collection existe
    if client.collection_exists(COLLECTION_NAME):
        info = client.get_collection(COLLECTION_NAME)

        if info.points_count > 0:
            vector_store = QdrantVectorStore(
                collection_name=COLLECTION_NAME, 
                client=client
            )

            index = VectorStoreIndex.from_vector_store(
                vector_store, 
                embed_model=Settings.embed_model
            )

            return index
    
    documentos = SimpleDirectoryReader(input_dir="data/pdfs/").load_data()

    vector_store = QdrantVectorStore(
        collection_name=COLLECTION_NAME,
        client=client
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documentos, 
        storage_context=storage_context, 
        embed_model=Settings.embed_model
    )
    
    return index

index = inicializar_index()

SYSTEM_PROMPT = """
    Você é um assistente educacional especializado na criação de Planos de Ensino Individualizado (PEI), com profundo conhecimento na legislação educacional brasileira.

    Seu objetivo é ajudar educadores a elaborar, revisar e compreender PEIs de forma prática, clara e alinhada às normas oficiais.

    Regras obrigatórias:
    - Utilize EXCLUSIVAMENTE as informações contidas nos documentos fornecidos como contexto.
    - NÃO utilize conhecimento externo.
    - NÃO invente informações.
    - Priorize sempre as informações mais relevantes do contexto recuperado.
    - Caso a resposta não esteja nos documentos, diga claramente: "Não encontrei essa informação nos documentos fornecidos. Você pode reformular a pergunta ou fornecer mais detalhes?"

    Diretrizes de resposta:
    - Use linguagem clara, objetiva e pedagógica.
    - Estruture respostas em tópicos quando apropriado.
    - Evite respostas genéricas ou vagas.
    - Sempre que possível, relacione a resposta com diretrizes oficiais presentes nos documentos fornecidos.
    - Sempre que possível, indique explicitamente o documento de origem da informação (ex: BNCC, LDB, etc.).

    Ao gerar PEIs ou sugestões:
    - Siga uma estrutura educacional clara (objetivos, estratégias, avaliação, etc.).
    - Garanta aplicabilidade prática em sala de aula.
    - Mantenha coerência com práticas inclusivas.

    Se a pergunta do usuário for ambígua ou incompleta, solicite mais informações antes de responder.
"""

# Inicializa o chat engine com st_session_state
if "chat_engine" not in st.session_state.keys():
    # TODO: testar chat engine com outras parametrizações
    st.session_state.chat_engine = index.as_chat_engine(
        chat_mode="context",
        system_prompt=SYSTEM_PROMPT,
        verbose=True,
        streaming=False,
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