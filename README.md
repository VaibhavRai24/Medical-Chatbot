# 🩺 Medical Chatbot (RAG-based)

A Retrieval-Augmented Generation (RAG) based medical chatbot designed to provide informative responses to medical queries. It leverages state-of-the-art natural language processing tools and frameworks like **LangChain**, **Hugging Face**, **Pinecone**, and **Google APIs**, with a user-friendly interface powered by **Streamlit**.

---

## 🚀 Features

- 🧠 RAG architecture for better factual accuracy  
- 🔍 Contextual retrieval using Pinecone vector store  
- 🧬 Hugging Face Transformer embeddings  
- 🌐 Google API integration for enhanced search  
- 🎯 Built using LangChain framework  
- 💬 Streamlit-based interactive UI  
- ☁️ Easy deployment on cloud or local systems  

---

## 🛠️ Tech Stack

| Component       | Tool/Framework            |
|----------------|---------------------------|
| Retrieval       | Pinecone                  |
| Embeddings      | Hugging Face Transformers |
| LLM Framework   | LangChain                 |
| External Search | Google API                |
| UI              | Streamlit                 |
| Deployment      | Streamlit Sharing / Cloud |

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/medical-chatbot-rag.git
   cd medical-chatbot-rag
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


GOOGLE_API_KEY=your_google_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=your_pinecone_environment
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
