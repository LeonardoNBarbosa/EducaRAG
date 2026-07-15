"""
Módulo RAG - Gerencia conexão com Qdrant, inicialização do índice e criação do chat engine.
"""

import streamlit as st
import qdrant_client
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    Settings,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.vector_stores.qdrant import QdrantVectorStore
from app.config import (
    LLM_MODEL,
    EMBED_MODEL,
    EMBED_BATCH_SIZE,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    QDRANT_URL,
    QDRANT_COLLECTION,
    DATA_DIR,
    SYSTEM_PROMPT,
    get_secrets,
)

# entender como funciona -> None e os parâmetors do embed_model
def configurar_settings(groq_key: str) -> None:
    Settings.llm = Groq(
        model=LLM_MODEL,
        api_key=groq_key
    )

    Settings.embed_model = HuggingFaceEmbedding(
        model_name=EMBED_MODEL,
        device="cpu",
        embed_batch_size=EMBED_BATCH_SIZE,
        model_kwargs={
            "trust_remote_code": True,
            "low_cpu_mem_usage": False
        },
    )

    Settings.node_parser = SentenceSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

# entender como funciona
def conectar_qdrant(api_key: str) -> qdrant_client.QdrantClient:
    return qdrant_client.QdrantClient(
        url=QDRANT_URL,
        api_key=api_key,
        check_compatibility=False,
    )

@st.cache_resource(show_spinner=False)
def inicializar_index(groq_key: str, qdrant_key: str) -> VectorStoreIndex:
    """
    Inicializa o índice vetorial.
    Reutiliza a collection existente no Qdrant se já estiver populada;
    caso contrário, processa os documentos locais e indexa.
    """
    configurar_settings(groq_key)
    client = conectar_qdrant(qdrant_key)

    vector_store = QdrantVectorStore(
        collection_name=QDRANT_COLLECTION,
        client=client,
    )

    collection_existe = client.collection_exists(QDRANT_COLLECTION)
    if collection_existe:
        info = client.get_collection(QDRANT_COLLECTION)
        if info.points_count > 0:
            return VectorStoreIndex.from_vector_store(
                vector_store,
                embed_model=Settings.embed_model,
            )

    # Indexação a partir dos PDFs locais
    documentos = SimpleDirectoryReader(input_dir=DATA_DIR).load_data()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex.from_documents(
        documentos,
        storage_context=storage_context,
        embed_model=Settings.embed_model,
    )

def criar_chat_engine(index: VectorStoreIndex):
    return index.as_chat_engine(
        chat_mode="context",
        system_prompt=SYSTEM_PROMPT,
        llm=Settings.llm,
        streaming=True,
        verbose=False,
    )