"""
This module contains functions for obtaining vector store instances
based on the specified store name. It supports different vector stores
for document indexing and retrieval.
"""

from langchain_community.vectorstores import FAISS, Chroma, Weaviate  # pylint: disable=no-name-in-module

def get_vector_store(store_name, documents, embeddings_model):
    """
    Retrieves the appropriate vector store based on the store name.

    Parameters:
        store_name (str): The name of the vector store ('faiss', 'chroma', or 'weaviate').
        documents (list): The list of documents to index in the vector store.
        embeddings_model: The embeddings model to use for vector store creation.

    Returns:
        vector_store: The corresponding vector store instance.

    Raises:
        ValueError: If the store name is unsupported.
    """
    if store_name == "faiss":
        return FAISS.from_documents(documents, embeddings_model)
    if store_name == "chroma":
        return Chroma.from_documents(documents, embeddings_model)
    if store_name == "weaviate":
        return Weaviate.from_documents(documents, embeddings_model)
    raise ValueError(f"Unsupported vector store: {store_name}")
