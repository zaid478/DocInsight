"""
This module contains functions for processing text documents, including splitting them into chunks.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_documents(documents, chunk_size, chunk_overlap):
    """
    Splits the given list of documents into chunks based on the specified chunk size and overlap.

    Parameters:
        documents (list): A list of documents to be split.
        chunk_size (int): The maximum size of each chunk.
        chunk_overlap (int): The overlap between chunks.

    Returns:
        list: A list of documents where each document is split into chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                   chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)
