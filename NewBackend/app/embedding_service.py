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











import os
import logging
import pandas as pd
from time import sleep
from dotenv import load_dotenv
from flask import current_app
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from openai import AzureOpenAI

# Load environment variables
load_dotenv()
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_EMBEDDING_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL")

# Validate environment variables
def validate_env_vars(*vars):
    missing_vars = [var for var in vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

validate_env_vars(
    "AZURE_OPENAI_API_KEY",
    "AZURE_OPENAI_API_VERSION",
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_EMBEDDING_MODEL"
)

# Initialize OpenAI and ChromaDB clients
openai_client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

chroma_client = chromadb.PersistentClient(
    path=current_app.config["STORE_NAME"],
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Read and validate CSV file
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

# Preprocess a single row into a text string
def preprocess_row(row):
    return f"Document Name: {row['Document Name']}, Attribute: {row['Attribute']}, Title: {row['Title']}, Expectations: {row['Expectations']}"

# Generate embeddings with retry logic
def get_embeddings(text_chunks, batch_size=10, retries=3, delay=2):
    embeddings = []
    for i in range(0, len(text_chunks), batch_size):
        batch = text_chunks[i:i + batch_size]
        for attempt in range(retries):
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
                break  # Exit retry loop if successful
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed for batch starting at {i}: {e}")
                if attempt < retries - 1:
                    sleep(delay)
                else:
                    logging.error(f"Failed to generate embeddings after {retries} retries for batch starting at {i}.")
                    raise
    return embeddings

# Store embeddings and metadata in ChromaDB
def store_embeddings_in_chroma(embeddings, metadata_list):
    try:
        for idx, item in enumerate(embeddings):
            metadata = metadata_list[idx]
            collection.upsert(
                documents=[item['text']],
                embeddings=[item['embedding']],
                ids=[str(hash(item['text']))],
                metadatas=[metadata]  # Store the updated metadata (now includes 'Title')
            )
        return True
    except Exception as e:
        logging.error(f"Error storing embeddings: {e}")
        return False


# Main function to process CSV files and store embeddings
def create_and_store_embeddings_from_csv(csv_file_paths):
    global collection
    try:
        collection = chroma_client.get_or_create_collection(name=current_app.config["COLLECTION_NAME"])
    except Exception as e:
        logging.error(f"Error getting or creating collection: {e}")
        return "Failed to initialize ChromaDB collection."

    for csv_file_path in csv_file_paths:
        try:
            # Read and preprocess CSV data
            df = read_csv_file(csv_file_path)
            if df is None:
                logging.warning(f"Skipping file {csv_file_path} due to errors.")
                continue 

            df['processed_text'] = df.apply(preprocess_row, axis=1)
            text_chunks = df['processed_text'].tolist()

            # Prepare metadata
            metadata_list = df[['Title', 'Attribute']].to_dict(orient='records')

            # Generate embeddings
            embeddings = get_embeddings(text_chunks)

            # Store embeddings and metadata in ChromaDB
            if store_embeddings_in_chroma(embeddings, metadata_list):
                logging.info(f"Embeddings for {len(embeddings)} records from {csv_file_path} stored successfully.")
            else:
                logging.error(f"Failed to save embeddings for {csv_file_path}.")
        except Exception as e:
            logging.error(f"Error processing file {csv_file_path}: {e}")

 
def list_collections():
    
    # Retrieve and print the list of collections
    collections = chroma_client.list_collections()
    collection_data = [{'id': collection.id, 'name': collection.name} for collection in collections]

    return collection_data

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
