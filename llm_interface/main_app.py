"""
This module sets up a Streamlit interface for a conversational AI bot that
uses LangChain and OpenAI to answer questions based on PDF content.
"""

import streamlit as sl

from langchain_openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS  # pylint: disable=no-name-in-module
from langchain.chains import ConversationalRetrievalChain  # pylint: disable=no-name-in-module disable=C0412
from langchain.chat_models import ChatOpenAI  # pylint: disable=no-name-in-module


def start_conversation(vector_embeddings):
    """
    Initializes a conversation chain with the given vector embeddings.
    
    Args:
        vector_embeddings: The vector embeddings to use for the retriever.

    Returns:
        A conversational retrieval chain instance.
    """
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )
    conversation = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_embeddings.as_retriever(),
        memory=memory
    )

    return conversation


def load_prompt():
    """
    Loads a chat prompt template for the conversation.
    
    Returns:
        A ChatPromptTemplate instance with the defined prompt.
    """
    prompt_text = """You need to answer the question from the pdf content.
    Make it as detailed as possible. Try to put every bit of detail from the book in your answer. 
    Given below is the context and question of the user.
    context = {context}
    question = {question}
    if the answer is not in the pdf, answer that "i do not know what you are asking about"."""

    prompt = ChatPromptTemplate.from_template(prompt_text)
    return prompt


def load_knowledge_base():
    """
    Loads the knowledge base from the local FAISS vector store.
    
    Returns:
        A FAISS instance with the loaded vector store.
    """
    embeddings = OpenAIEmbeddings(model='text-embedding-3-large')
    db_faiss_path = '../vector_store_creation/vector_store_books'
    db = FAISS.load_local(db_faiss_path, embeddings, allow_dangerous_deserialization=True)
    return db


def load_llm():
    """
    Loads the OpenAI language model.
    
    Returns:
        A ChatOpenAI instance with the specified model configuration.
    """
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    return llm


def format_docs(docs):
    """
    Formats the documents into a single string.
    
    Args:
        docs: A list of document objects.

    Returns:
        A string with the concatenated content of all documents.
    """
    return "\n\n".join(doc.page_content for doc in docs)


def main():
    """
    Main function to run the Streamlit application.
    """
    sl.header("Welcome to the 📝PDF bot")
    sl.write("🤖 You can chat by entering your queries")

    knowledge_base = load_knowledge_base()
    llm = load_llm()
    prompt = load_prompt()

    query = sl.text_input('Enter some text')

    if query:
        # Getting only the chunks that are similar to the query for the LLM to produce the output
        similar_embeddings = knowledge_base.similarity_search(query)
        similar_embeddings = FAISS.from_documents(documents=similar_embeddings,
                                                  embedding=OpenAIEmbeddings())

        # Creating the chain for integrating LLM, prompt, and output parser
        retriever = similar_embeddings.as_retriever()
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}  # pylint: disable=unsupported-binary-operation
            | prompt
            | llm
            | StrOutputParser()
        )

        response = rag_chain.invoke(query)
        sl.write(response)


if __name__ == "__main__":
    main()
