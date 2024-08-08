import streamlit as sl
from PyPDF2 import PdfReader
from dotenv import load_dotenv

from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


from web_template import css, bot_template, user_template


def start_conversation(vector_embeddings):
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


#creating prompt template using langchain
def load_prompt():
        prompt = """You are an expert in arabic language and Islamic jurispudence. You need to answer the question from the pdf. Make it as detailed as possible. Try to put every bit of detail from the book in your answer. Do not put any thing which is irrelevant to the query.
        Given below is the context and question of the user.
        context = {context}
        question = {question}
        if the answer is not in the pdf, answer that "i do not know what you are asking about"
         """
        prompt = ChatPromptTemplate.from_template(prompt)
        return prompt



#function to load the vectordatabase
def load_knowledgeBase():
        embeddings=OpenAIEmbeddings(model = 'text-embedding-3-large')
        DB_FAISS_PATH = '../vector_store_creation/vector_store_books'
        db = FAISS.load_local(DB_FAISS_PATH, embeddings,allow_dangerous_deserialization = True)
        return db


#function to load the OPENAI LLM
def load_llm():
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        return llm


def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)


def main():
        sl.header("مساعد الوثائق -- Document Assistant")
        sl.write("🤖 You can chat by Entering your queries ")
        knowledgeBase=load_knowledgeBase()
        llm=load_llm()
        prompt=load_prompt()
        
        query=sl.text_input('Enter some text')
        
        
        if(query):
                #getting only the chunks that are similar to the query for llm to produce the output
                similar_embeddings=knowledgeBase.similarity_search(query,k=50)
                similar_embeddings=FAISS.from_documents(documents=similar_embeddings, embedding=OpenAIEmbeddings())
                
                #creating the chain for integrating llm,prompt,stroutputparser
                retriever = similar_embeddings.as_retriever()
                rag_chain = (
                        {"context": retriever | format_docs, "question": RunnablePassthrough()}
                        | prompt
                        | llm
                        | StrOutputParser()
                    )
                
                response=rag_chain.invoke(query)
                sl.write(response)


if __name__ == "__main__":
    main()