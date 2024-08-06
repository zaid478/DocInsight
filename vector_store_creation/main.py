"""
This module processes PDF files in a given directory by splitting the text into chunks,
generating embeddings, and creating a FAISS index for document retrieval.
"""

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS  # pylint: disable=no-name-in-module
from langchain_community.document_loaders import PyPDFLoader  # pylint: disable=no-name-in-module

load_dotenv()

def create_chunks_embeddings(books_directory):
    """
    Processes each PDF file in the given directory, splits the text into chunks, 
    generates embeddings, and creates a FAISS index.

    Parameters:
        books_directory (str): The directory containing PDF files.
    """
    pdf_files = [f for f in os.listdir(books_directory) if f.lower().endswith('.pdf')]
    pdf_count = len(pdf_files)

    print(f"Found {pdf_count} PDF files in the directory '{books_directory}'.")
    all_documents = []
    for i, pdf_file in enumerate(pdf_files):
        pdf_path = os.path.join(books_directory, pdf_file)
        print(f"Processing PDF file {i + 1} out of {pdf_count}: {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        all_documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunked_documents = text_splitter.split_documents(all_documents)

    # Extract out embeddings and creating FAISS index
    faiss_index = FAISS.from_documents(chunked_documents,
                                       OpenAIEmbeddings(model='text-embedding-ada-002'))
    faiss_index.save_local("vector_store_books")

# Main entry point
if __name__ == "__main__":
    create_chunks_embeddings("../book_scraper/books/8183")
