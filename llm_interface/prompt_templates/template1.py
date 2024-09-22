"""
Module for creating the 'Detailed Document Q&A' chat prompt template used in 
conversational AI for answering questions based on Document content.
"""

from langchain.prompts import ChatPromptTemplate

def create_chat_prompt_template():
    """
    Creates a 'Detailed Document Q&A' chat prompt template for answering Document-based 
    questions. Prompts the AI to provide detailed answers or state if the 
    information is not available.
    
    Returns:
        ChatPromptTemplate: The configured chat prompt template.
    """
    prompt_text = """
    You need to answer the question from the PDF content.
    Make it as detailed as possible. Try to include every relevant detail from the book in your answer. 
    Given below is the context and the question of the user.
    
    Context: {context}
    Question: {question}
    
    If the answer is not in the PDF, respond with "I do not know what you are asking about."
    """

    prompt = ChatPromptTemplate.from_template(prompt_text)
    
    return prompt
