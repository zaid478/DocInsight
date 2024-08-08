```markdown
# Document Processing and Vector Store Creation

## Overview

This project processes text and PDF documents, generates embeddings, and creates a vector store index for efficient document retrieval. It utilizes various text loaders, embedding models, and vector stores to handle and index documents.

## Project Structure

- `document_loaders.py`: Contains classes for loading text and PDF documents.
- `models.py`: Defines the embedding models and provides a function to get the appropriate embedding model.
- `text_processing.py`: Contains functions for processing and chunking documents.
- `vector_stores.py`: Provides functions to create and manage vector stores.
- `config.py`: Configuration file for setting up parameters and model details.
- `create_embedding.py`: Entry point for processing documents and creating vector stores.

## Configuration

Edit the `config.py` file to set up parameters and model details. Example configuration:

```python
# config.py

BOOKS_DIRECTORY = "../book_scraper/books/8183"
FILE_TYPE = "txt"  # Options: "pdf", "txt"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "ARABIC_TRIPLET_MATRYOSHKA"  # Options: from OpenAI/Hugging Face enum
MODEL_TYPE = "huggingface"  # Options: "openai", "huggingface"
VECTOR_STORE = "faiss"  # Options: "faiss", "chroma", "weaviate"
HANDLE_METADATA = True  # Set to True to handle metadata
```

## Usage

Run the `create_embedding.py` script to process documents and create a vector store index:

```bash
python create_embedding.py
```

## Code Documentation

### `document_loaders.py`

Contains classes for loading documents from text and PDF files.

- `SimpleTextDocument`: Represents a text document with content and optional metadata.
- `SimpleTextLoader`: Loads text documents from a file.

### `models.py`

Defines embedding models and provides functionality to get the appropriate model based on type.

- `OpenAIModels`: Enum for OpenAI embedding models.
- `HuggingFaceModels`: Enum for Hugging Face sentence transformer models.
- `CustomArabicEmbeddings`: Custom class for Hugging Face embeddings.
- `get_embeddings_model`: Function to retrieve the appropriate embeddings model.

### `text_processing.py`

Processes and chunks documents.

- `process_documents`: Splits documents into chunks using the `RecursiveCharacterTextSplitter`.

### `vector_stores.py`

Handles creation and management of vector stores.

- `get_vector_store`: Function to retrieve the appropriate vector store based on name.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```