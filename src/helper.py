from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings



def load_documents_from_directory(data):
    loader = DirectoryLoader(data, 
                            glob = "*.pdf",
                            loader_cls=PyPDFLoader)
    
    documents = loader.load()
    
    return documents



def text_spliter(extracted__data_of_file):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 700,
        chunk_overlap = 50,
    )
    
    text_chunks = text_splitter.split_documents(extracted__data_of_file)
    return text_chunks


def download_embeddings():
    embedding = HuggingFaceEmbeddings(model_name= 'sentence-transformers/all-MiniLM-L6-v2')
    return embedding

