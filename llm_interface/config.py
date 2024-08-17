"""
This module contains configuration settings for RAG Application.
"""

# Directory containing text or PDF files
EMBEDDINGS_DIRECTORY = "../book_scraper/books/8183"

# Embedding model to use
EMBEDDING_MODEL = "ARABIC_TRIPLET_MATRYOSHKA"

# Type of embedding model ('openai' or 'huggingface')
MODEL_TYPE = "huggingface"

# Vector store to use ('faiss', 'chroma', 'weaviate')
VECTOR_STORE = "faiss"
