"""
This module contains configuration settings for processing documents,
generating embeddings, and creating vector stores.
"""

# Directory containing text or PDF files
BOOKS_DIRECTORY = "../book_scraper/books/8183"

# File type to process ('pdf' or 'txt')
FILE_TYPE = "txt"

# Size of each chunk
CHUNK_SIZE = 1000

# Overlap between chunks
CHUNK_OVERLAP = 200

# Embedding model to use
EMBEDDING_MODEL = "ARABIC_TRIPLET_MATRYOSHKA"

# Type of embedding model ('openai' or 'huggingface')
MODEL_TYPE = "huggingface"

# Vector store to use ('faiss', 'chroma', 'weaviate')
VECTOR_STORE = "faiss"

# Whether to handle metadata or not
HANDLE_METADATA = True
