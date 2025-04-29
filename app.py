import streamlit as st
from dotenv import load_dotenv
from src.helper import download_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from src.prompt import *

import os

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


embeddings = download_embeddings()
index_name = "medical-chatbot"
document_search = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)
retriever = document_search.as_retriever(search_type="similarity", search_kwargs={"k": 3})


llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0.0, max_output_tokens=512)
prompt = PromptTemplate(
    template="""
    You are a helpful assistant.
    You have access to a large amount of medical literature.
    You will be given a context and a question.
    Your task is to answer the question based on the context provided.
    If the context contains the answer, provide it in a concise manner.
    If the context does not contain the answer, say "I don't know".
    If the context is too long, summarize it before answering.
    If the context is too short, provide a detailed answer based on your knowledge.
    If the context is irrelevant, say "I don't know".
    
    {context}
    
    Question: {question}
    """,
    input_variables=['context', 'question']
)

def format_docs(retrieved_docs):
    return "\n\n".join(doc.page_content for doc in retrieved_docs)


parallel_chain = RunnableParallel({
    'question': RunnablePassthrough(),
    'context': retriever | RunnableLambda(format_docs)
})
parser = StrOutputParser()
final_chain = parallel_chain | prompt | llm | parser

st.set_page_config(page_title="Medical Chatbot", page_icon="🩺")
st.title("🩺 Medical Chatbot")
st.write("Ask any medical-related question and get AI-assisted responses based on medical literature.")

if "history" not in st.session_state:
    st.session_state.history = []


user_input = st.text_input("Your question:", key="input")

if user_input:
    with st.spinner("Thinking..."):
        response = final_chain.invoke(user_input)
   
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", response))

for speaker, msg in st.session_state.history:
    if speaker == "You":
        st.markdown(f"**🧑 {speaker}:** {msg}")
    else:
        st.markdown(f"**🤖 {speaker}:** {msg}")
