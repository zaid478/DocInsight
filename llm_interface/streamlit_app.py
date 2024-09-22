import streamlit as sl
from utils.knowledge_base import load_knowledge_base
from utils.language_model import load_language_model
from prompt_templates import load_prompt_template
from utils.rag_chain import setup_rag_chain
from utils.memory_config import load_memory

def run_app():
    """
    Main function to run the Streamlit application.
    """
    sl.header("Welcome to the 📝 PDF Bot")
    sl.write("🤖 You can chat by entering your queries")

    knowledge_base = load_knowledge_base()
    llm = load_language_model()
    prompt_template = load_prompt_template()
    memory = load_memory()
    query = sl.text_input('Enter your query')

    if query:
        # Retrieve relevant documents
        similar_embeddings = knowledge_base.similarity_search(query)
        similar_embeddings = FAISS.from_documents(documents=similar_embeddings,
                                                  embedding=OpenAIEmbeddings())

        similar_embeddings = knowledge_base.similarity_search(query)
        # Set up the RAG chain
        rag_chain = setup_rag_chain(similar_embeddings, llm, prompt_template, memory)
        
        # Get the response
        response = rag_chain.invoke(query)
        print(response)
        
        # Invoke the chain and get the response
        response = rag_chain.invoke(query)
        sl.write(response)

if __name__ == "__main__":
    run_app()
