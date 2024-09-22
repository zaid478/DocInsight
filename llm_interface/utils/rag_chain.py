from config.config import VECTOR_STORE_TYPE, EMBEDDINGS_MODEL_TYPE, OpenAIModels, HuggingFaceModels, VectorStoreType, EmbeddingsModelType
from langchain.embeddings import OpenAIEmbeddings, SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS, Chroma, Weaviate  # Import additional vector store classes if needed
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


def format_docs(docs):
    """
    Formats the documents into a single string.
    
    Args:
        docs: A list of document objects.

    Returns:
        A string with the concatenated content of all documents.
    """
    return "\n\n".join(doc.page_content for doc in docs)

def setup_rag_chain(similar_embeddings, llm, prompt_template, memory):
    """
    Sets up a RAG chain with memory and configurable vector store and embeddings.

    Args:
        similar_embeddings: A list of documents or embeddings.
        llm: The language model instance.
        prompt_template: The prompt template to use for the LLM.
        memory: The memory instance for storing conversation history.

    Returns:
        A configured RAG chain instance.
    """
    # Choose the vector store based on configuration
    if VECTOR_STORE_TYPE == VectorStoreType.FAISS:
        vector_store = FAISS
    elif VECTOR_STORE_TYPE == VectorStoreType.CHROMA:
        vector_store = Chroma
    elif VECTOR_STORE_TYPE == VectorStoreType.WEAVIATE:
        vector_store = Weaviate
    else:
        raise ValueError(f"Unsupported VECTOR_STORE_TYPE: {VECTOR_STORE_TYPE}")

    # Choose the embeddings model based on configuration
    if EMBEDDINGS_MODEL_TYPE == EmbeddingsModelType.OPENAI_EMBEDDINGS:
        embedding_model = OpenAIEmbeddings(model_name=OpenAIModels.TEXT_3_LARGE.value)
    elif EMBEDDINGS_MODEL_TYPE == EmbeddingsModelType.SENTENCE_TRANSFORMER_EMBEDDINGS:
        embedding_model = SentenceTransformerEmbeddings(model_name=HuggingFaceModels.GTR_T5_LARGE.value)
    else:
        raise ValueError(f"Unsupported EMBEDDINGS_MODEL_TYPE: {EMBEDDINGS_MODEL_TYPE}")

    # Initialize the retriever with the chosen vector store and embeddings model
    retriever = vector_store.from_documents(documents=similar_embeddings, embedding=embedding_model).as_retriever()

    context_handler = retriever | format_docs
    query_handler = RunnablePassthrough()  # Pass the query unchanged

    # Create the prompt with context and query
    prompt = prompt_template.format({"context": context_handler, "question": query_handler})

    # Set up the RAG chain
    rag_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,  # Add memory if needed
        prompt=prompt,
        output_parser=StrOutputParser()
    )

    return rag_chain
