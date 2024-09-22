from enum import Enum, auto

class VectorStoreType(Enum):
    FAISS = 'faiss'
    CHROMA = 'chroma'
    WEAVIATE = 'weaviate'

class LLMModelType(Enum):
    CHAT_OPENAI = auto()
    SENTENCE_TRANSFORMER = auto()

class EmbeddingsModelType(Enum):
    OPENAI_EMBEDDINGS = auto()
    SENTENCE_TRANSFORMER_EMBEDDINGS = auto()

class OpenAIModels(Enum):
    """
    Enum class for OpenAI model names.
    """
    ADA_002 = 'text-embedding-ada-002'
    TEXT_3_LARGE = 'text-embedding-3-large'
    GPT_3_5_TURBO = 'gpt-3.5-turbo'


class HuggingFaceModels(Enum):
    """
    Enum class for Hugging Face model names.
    """
    ARABIC_TRIPLET_MATRYOSHKA = 'Omartificial-Intelligence-Space/Arabic-Triplet-Matryoshka-V2'
    ARABAIC_TEXT_STS = 'AbderrahmanSkiredj1/Arabic_text_embedding_for_sts'
    GTR_T5_LARGE = 'sentence-transformers/gtr-t5-large'

class PromptTemplateType(Enum):
    """
    Enum class for different prompt template types.
    """
    TEMPLATE_1 = 'template1'
    TEMPLATE_2 = 'template2'


# Specify the base directory for loading embeddings
BASE_DIR = '/home/saad/Documents/Code/DocInsight/vector_store_creation/embdeddings'

# BOOK_ID
BOOK_ID = 8183

# Configuration settings
VECTOR_STORE_TYPE = VectorStoreType.FAISS
LLM_MODEL_TYPE = LLMModelType.CHAT_OPENAI
EMBEDDINGS_MODEL_TYPE = EmbeddingsModelType.SENTENCE_TRANSFORMER_EMBEDDINGS
LLM_MODEL = OpenAIModels.GPT_3_5_TURBO
EMBEDDING_MODEL = HuggingFaceModels.GTR_T5_LARGE
PROMPT_TEMPLATE_TYPE = PromptTemplateType.TEMPLATE_1
