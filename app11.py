from flask import Flask, render_template, request, jsonify
from src.helper import download_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
from src.prompt import *


app = Flask(__name__)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")    

embeddings = download_embeddings()

index_name = "medical-chatbot"

document_search = PineconeVectorStore.from_existing_index(
    index_name = index_name,
    embedding= embeddings)

retriver = document_search.as_retriever(search_type = "similarity",search_kwargs={"k": 3})

llm  = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0.0, max_output_tokens=512)

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
    input_variables = ['context', 'question']
)

def format_docs(retrieved_docs):
  context = "\n\n".join(doc.page_content for doc in retrieved_docs)
  return context

parallel_chain = RunnableParallel({
    'question': RunnablePassthrough(),
    'context': retriver | RunnableLambda(format_docs)
})

parser = StrOutputParser()
final_chain = parallel_chain | prompt | llm | parser


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get', methods=['GET', 'POST'])
def get_bot_response():
    user_input = request.form['msg']
    input = user_input
    print(input)
    response = final_chain.invoke({"question": user_input})
    print("Response:", response)
    return str(response["answer"])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port = 8080)