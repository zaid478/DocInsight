"""
This module defines various embedding models and provides functionality to retrieve 
the appropriate model based on the specified type and name.
"""

from enum import Enum
from sentence_transformers import SentenceTransformer
from langchain_openai import OpenAIEmbeddings

class OpenAIModels(Enum):
    """
    Enum class for OpenAI model names.
    """
    ADA_002 = 'text-embedding-ada-002'
    TEXT_3_LARGE = 'text-embedding-3-large'

class HuggingFaceModels(Enum):
    """
    Enum class for Hugging Face model names.
    """
    ARABIC_TRIPLET_MATRYOSHKA = 'Omartificial-Intelligence-Space/Arabic-Triplet-Matryoshka-V2'
    ARABAIC_TEXT_STS = 'AbderrahmanSkiredj1/Arabic_text_embedding_for_sts'
    GTR_T5_LARGE = 'sentence-transformers/gtr-t5-large'
    E5_MISTRAL_7B = 'intfloat/e5-mistral-7b-instruct'
    GTE_MULTILINGUAL = 'Alibaba-NLP/gte-multilingual-base'

class CustomArabicEmbeddings:
    """
    A class for handling Arabic embeddings using the SentenceTransformer model.
    """
    def __init__(self, model_name):
        """
        Initializes the CustomArabicEmbeddings with a specified model.

        Parameters:
            model_name (str): The name of the SentenceTransformer model.
        """
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        """
        Generates embeddings for a list of texts using the SentenceTransformer model.

        Parameters:
            texts (list): List of texts to embed.

        Returns:
            list: List of embeddings for the given texts.
        """
        return self.model.encode(texts)

def get_embeddings_model(model_name, model_type):
    """
    Retrieves the appropriate embeddings model based on the model type and name.

    Parameters:
        model_name (str): The name of the model.
        model_type (str): The type of the model ('huggingface' or 'openai').

    Returns:
        embedding_model: The corresponding embedding model.

    Raises:
        ValueError: If the model type or name is invalid.
    """
    if model_type == "huggingface":
        if not any(model_name == member.name for member in HuggingFaceModels):
            raise ValueError(f"Invalid Hugging Face model name: {model_name}")
        return CustomArabicEmbeddings(HuggingFaceModels[model_name].value)
    elif model_type == "openai":
        if not any(model_name == member.name for member in OpenAIModels):
            raise ValueError(f"Invalid OpenAI model name: {model_name}")
        return OpenAIEmbeddings(model=OpenAIModels[model_name].value)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
