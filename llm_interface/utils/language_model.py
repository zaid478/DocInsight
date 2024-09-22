from config.config import LLMModelType, LLM_MODEL_TYPE, LLM_MODEL
from langchain.chat_models import ChatOpenAI
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_language_model():
    """
    Loads the language model based on the configured LLM model type.
    
    Returns:
        A language model instance.
    """
    if LLM_MODEL_TYPE == LLMModelType.CHAT_OPENAI:
        return ChatOpenAI(model_name=LLM_MODEL.value, temperature=0)
    elif LLM_MODEL_TYPE == LLMModelType.SENTENCE_TRANSFORMER:
        return SentenceTransformer(LLM_MODEL.value)
