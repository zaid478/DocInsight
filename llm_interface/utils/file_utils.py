import os
from config.config import BASE_DIR, BOOK_ID, EMBEDDING_MODEL, VECTOR_STORE_TYPE

def create_embeddings_directory():
    """
    Creates an embeddings directory based on the book_id, embedding_model, and vector_store.
    
    Args:
        book_id (str): Identifier for the book.
        embedding_model (str): The embedding model name.
        vector_store (str): The type of vector store.
    
    Returns:
        str: The path of the created directory.
    """
    vector_store = VECTOR_STORE_TYPE.value
    embedding_model = EMBEDDING_MODEL.name
    directory_name = f"{BOOK_ID}_{embedding_model}_{vector_store}"
    directory_path = os.path.join(BASE_DIR, directory_name)
    
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    
    return directory_path
