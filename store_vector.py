from src.helper import text_spliter, download_embeddings, load_documents_from_directory
from pinecone.grpc import PineconeGRPC as pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from  dotenv import load_dotenv
load_dotenv()   
import os

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

extracted_data_of_file = load_documents_from_directory(data=r"C:\Users\VAIBHAVRAI\OneDrive\Desktop\LangchainProjects\INTIALIZER\MedicalChatbot\data")
text_chunks = text_spliter(extracted_data_of_file)
embeddings = download_embeddings()


from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import os

pc = Pinecone(api_key= PINECONE_API_KEY)

index_name = "medical-chatbot"
pc.create_index(
    name=index_name,
    dimension=384,
    metric="cosine",
    spec = ServerlessSpec(
        cloud="aws",
        region="us-east-1",
        )
)


search = PineconeVectorStore.from_documents(
    documents=text_chunks,
    embedding=embeddings,
    index_name = index_name
)
