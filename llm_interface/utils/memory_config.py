# memory_config.py

from langchain.memory import ConversationBufferMemory

def load_memory():
    """
    Creates and returns an instance of ConversationBufferMemory.

    Returns:
        ConversationBufferMemory: Configured memory instance.
    """
    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )
    return memory
