# import pandas as pd
# import os
# import logging
# from dotenv import load_dotenv
# import chromadb
# from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
# from openai import AzureOpenAI
# from time import sleep

# load_dotenv()
# AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
# AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
# AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
# AZURE_OPENAI_EMBEDDING_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL")

# if not all([AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_EMBEDDING_MODEL]):
#     raise ValueError("Azure OpenAI credentials are not properly set in the environment variables.")

# openai_client = AzureOpenAI(
#     api_key=AZURE_OPENAI_API_KEY,
#     api_version=AZURE_OPENAI_API_VERSION,
#     azure_endpoint=AZURE_OPENAI_ENDPOINT
# )

# chroma_client = chromadb.PersistentClient(
#     path="chroma_store",
#     settings=Settings(),
#     tenant=DEFAULT_TENANT,
#     database=DEFAULT_DATABASE,
# )

# collection = chroma_client.get_or_create_collection(name="expectations_embeddings")

# logging.basicConfig(level=logging.INFO)

# def read_csv_file(csv_file_path):
#     try:
#         df = pd.read_csv(csv_file_path)
#         required_columns = ['Document Name', 'Attribute', 'Title', 'Expectations']
#         if not all(col in df.columns for col in required_columns):
#             raise ValueError(f"Missing required columns in {csv_file_path}")
#         return df
#     except Exception as e:
#         logging.error(f"Error reading file {csv_file_path}: {e}")
#         return None

# def preprocess_row(row):
#     return f"Document Name: {row['Document Name']}, Attribute: {row['Attribute']}, Title: {row['Title']}, Expectations: {row['Expectations']}"

# def get_embeddings(text_chunks, batch_size=5):
#     embeddings = []
#     for i in range(0, len(text_chunks), batch_size):
#         batch = text_chunks[i:i + batch_size]
#         try:
#             response = openai_client.embeddings.create(
#                 input=[chunk.strip() for chunk in batch],  
#                 model=AZURE_OPENAI_EMBEDDING_MODEL
#             )
#             for idx, chunk in enumerate(batch):
#                 embeddings.append({
#                     "text": chunk.strip(),
#                     "embedding": response.data[idx].embedding
#                 })
#         except Exception as e:
#             logging.error(f"Error getting embeddings for batch starting at {i}: {e}")
#             sleep(1)
#     return embeddings

# def store_embeddings_in_chroma(embeddings):
#     try:
#         for item in embeddings:
#             collection.upsert(
#                 documents=[item['text']],
#                 embeddings=[item['embedding']],
#                 ids=[str(hash(item['text']))]
#             )
#     except Exception as e:
#         logging.error(f"Error storing embeddings: {e}")

# def create_and_store_embeddings_from_csv(csv_file_paths):
#     for csv_file_path in csv_file_paths:
#         df = read_csv_file(csv_file_path)
#         if df is None:
#             continue 

#         df['processed_text'] = df.apply(preprocess_row, axis=1)
#         text_chunks = df['processed_text'].tolist()

#         embeddings = get_embeddings(text_chunks)

#         store_embeddings_in_chroma(embeddings)
        
#         logging.info(f"Embeddings for {len(embeddings)} records from {csv_file_path} stored successfully in ChromaDB.")


# csv_file_paths = [
#     os.path.join('expectations', 'Sheet1.csv'),
#     os.path.join('expectations', 'Sheet2.csv'),
#     os.path.join('expectations', 'Sheet3.csv'),
#     os.path.join('expectations', 'Sheet4.csv'),
#     os.path.join('expectations', 'Sheet5.csv'),
#     os.path.join('expectations', 'Sheet6.csv'),
#     os.path.join('expectations', 'Sheet7.csv'),
#     os.path.join('expectations', 'Sheet8.csv'),    
# ]

# create_and_store_embeddings_from_csv(csv_file_paths)











import pandas as pd
import os
import logging
from dotenv import load_dotenv
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from openai import AzureOpenAI
from time import sleep

load_dotenv()
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_EMBEDDING_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL")

if not all([AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_EMBEDDING_MODEL]):
    raise ValueError("Azure OpenAI credentials are not properly set in the environment variables.")

openai_client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

chroma_client = chromadb.PersistentClient(
    path="chroma_store",
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

collection = chroma_client.get_or_create_collection(name="expectations_embeddings")

logging.basicConfig(level=logging.INFO)

def read_csv_file(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path)
        required_columns = ['Document Name', 'Attribute', 'Title', 'Expectations']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Missing required columns in {csv_file_path}")
        return df
    except Exception as e:
        logging.error(f"Error reading file {csv_file_path}: {e}")
        return None

def preprocess_row(row):
    return f"Document Name: {row['Document Name']}, Attribute: {row['Attribute']}, Title: {row['Title']}, Expectations: {row['Expectations']}"

def get_embeddings(text_chunks, batch_size=5):
    embeddings = []
    for i in range(0, len(text_chunks), batch_size):
        batch = text_chunks[i:i + batch_size]
        try:
            response = openai_client.embeddings.create(
                input=[chunk.strip() for chunk in batch],  
                model=AZURE_OPENAI_EMBEDDING_MODEL
            )
            for idx, chunk in enumerate(batch):
                embeddings.append({
                    "text": chunk.strip(),
                    "embedding": response.data[idx].embedding
                })
        except Exception as e:
            logging.error(f"Error getting embeddings for batch starting at {i}: {e}")
            sleep(1)
    return embeddings

def store_embeddings_in_chroma(embeddings, metadata_list):
    try:
        for idx, item in enumerate(embeddings):
            metadata = metadata_list[idx]
            collection.upsert(
                documents=[item['text']],
                embeddings=[item['embedding']],
                ids=[str(hash(item['text']))],
                metadatas=[metadata]  # Add metadata here
            )
    except Exception as e:
        logging.error(f"Error storing embeddings: {e}")

def create_and_store_embeddings_from_csv(csv_file_paths):
    for csv_file_path in csv_file_paths:
        df = read_csv_file(csv_file_path)
        if df is None:
            continue 

        df['processed_text'] = df.apply(preprocess_row, axis=1)
        text_chunks = df['processed_text'].tolist()

        # Prepare metadata list
        metadata_list = df[['Attribute']].to_dict(orient='records')

        embeddings = get_embeddings(text_chunks)

        # Store embeddings with metadata
        store_embeddings_in_chroma(embeddings, metadata_list)
        
        logging.info(f"Embeddings for {len(embeddings)} records from {csv_file_path} stored successfully in ChromaDB.")

csv_file_paths = [
    os.path.join('expectations', 'Sheet1.csv'),
    os.path.join('expectations', 'Sheet2.csv'),
    os.path.join('expectations', 'Sheet3.csv'),
    os.path.join('expectations', 'Sheet4.csv'),
    os.path.join('expectations', 'Sheet5.csv'),
    os.path.join('expectations', 'Sheet6.csv'),
    os.path.join('expectations', 'Sheet7.csv'),
    os.path.join('expectations', 'Sheet8.csv'),    
]

create_and_store_embeddings_from_csv(csv_file_paths)
