"""
This module processes text or PDF files in a given directory by splitting the text into chunks,
generating embeddings, and creating a vector store index for document retrieval.
"""

import os
from dotenv import load_dotenv
from document_loaders import SimpleTextLoader
from langchain_community.document_loaders import PyPDFLoader  # pylint: disable=no-name-in-module
from models import get_embeddings_model
from vector_stores import get_vector_store
from text_processing import process_documents
import config as cfg

load_dotenv()

def create_chunks_embeddings():
    """
    Processes files in the given directory, splits the text into chunks, generates embeddings,
    and creates a vector store index using configuration from config.py.
    """
    books_directory = cfg.BOOKS_DIRECTORY
    file_type = cfg.FILE_TYPE
    chunk_size = cfg.CHUNK_SIZE
    chunk_overlap = cfg.CHUNK_OVERLAP
    embedding_model = cfg.EMBEDDING_MODEL
    model_type = cfg.MODEL_TYPE
    vector_store = cfg.VECTOR_STORE
    handle_metadata = cfg.HANDLE_METADATA

    if file_type == 'pdf':
        files = [f for f in os.listdir(books_directory) if f.lower().endswith('.pdf')]
        loader_class = PyPDFLoader
    elif file_type == 'txt':
        files = [f for f in os.listdir(books_directory) if f.lower().endswith('.txt')]
        loader_class = SimpleTextLoader
    else:
        raise ValueError("Unsupported file type. Choose 'pdf' or 'txt'.")

    file_count = len(files)
    print(f"Found {file_count} {file_type.upper()} files in the directory '{books_directory}'.")

    all_documents = []
    for i, file in enumerate(files):
        file_path = os.path.join(books_directory, file)
        print(f"Processing {file_type.upper()} file {i + 1} out of {file_count}: {file_path}")
        loader = loader_class(file_path)
        documents = loader.load()

        if handle_metadata:
            for doc in documents:
                doc.metadata.update({
                    "source": file,
                    "file_path": file_path
                })

        all_documents.extend(documents)

    chunked_documents = process_documents(all_documents, chunk_size, chunk_overlap)

    embeddings_model = get_embeddings_model(embedding_model, model_type)
    vector_store_index = get_vector_store(vector_store, chunked_documents, embeddings_model)
    last_folder_name = os.path.basename(os.path.normpath(books_directory))
    vector_store_index.save_local(f"{last_folder_name}_{vector_store}_index_books")

if __name__ == "__main__":
    create_chunks_embeddings()
