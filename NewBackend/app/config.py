import os

class Config:
    ALLOWED_EXTENSIONS = {'csv'}
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    PROMPT_FILE = os.path.join(os.path.dirname(__file__), 'prompts.txt') 
    INDEX_FILE= os.path.join(os.path.dirname(__file__), "faiss_index.index")
    IDS_FILE = os.path.join(os.path.dirname(__file__), "ids_list.npy")
    STORE_NAME= os.path.join(os.path.dirname(__file__), "chroma_store")
    COLLECTION_NAME = "expectations_embeddings"
    OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
