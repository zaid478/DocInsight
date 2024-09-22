from config.config import PROMPT_TEMPLATE_TYPE, PromptTemplateType
from .template1 import create_chat_prompt_template as template1


def load_prompt_template():
    if PROMPT_TEMPLATE_TYPE == PromptTemplateType.TEMPLATE_1:
        return template1()
    # Add additional conditions for other templates if needed
