from config.config import (
    VectorStoreType, 
    VECTOR_STORE_TYPE, 
    EMBEDDINGS_MODEL_TYPE, 
    EmbeddingsModelType, 
    EMBEDDING_MODEL
)
from utils.file_utils import create_embeddings_directory
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from sentence_transformers import SentenceTransformer

def load_knowledge_base():
    """
    Loads the knowledge base based on the configured vector store and embeddings model.
    
    Returns:
        A vector store instance with the loaded vector store.
    """
    embeddings_dir = create_embeddings_directory()
    if EMBEDDINGS_MODEL_TYPE == EmbeddingsModelType.OPENAI_EMBEDDINGS:
        embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL.value)
    elif EMBEDDINGS_MODEL_TYPE == EmbeddingsModelType.SENTENCE_TRANSFORMER_EMBEDDINGS:
        embeddings = SentenceTransformer(EMBEDDING_MODEL.value)

    if VECTOR_STORE_TYPE == VectorStoreType.FAISS:
        return FAISS.load_local(embeddings_dir, embeddings,
                                allow_dangerous_deserialization=True)
