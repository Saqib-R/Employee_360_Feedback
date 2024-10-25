# import pandas as pd
# import os
# import logging
# from dotenv import load_dotenv
# from openai import AzureOpenAI
# import numpy as np
# import faiss
# from time import sleep

# # Load environment variables
# load_dotenv()
# AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
# AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
# AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
# AZURE_OPENAI_EMBEDDING_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL")

# if not all([AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_EMBEDDING_MODEL]):
#     raise ValueError("Azure OpenAI credentials are not properly set in the environment variables.")

# # Initialize OpenAI client
# openai_client = AzureOpenAI(
#     api_key=AZURE_OPENAI_API_KEY,
#     api_version=AZURE_OPENAI_API_VERSION,
#     azure_endpoint=AZURE_OPENAI_ENDPOINT
# )

# # Setup logging
# logging.basicConfig(level=logging.INFO)

# # FAISS index initialization
# embedding_dimension = 1536  # Adjust based on the embedding model used
# faiss_index = faiss.IndexFlatL2(embedding_dimension)  # Create a FAISS index for L2 distance
# ids = []  # List to hold the unique ids for each document

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

# def store_embeddings_in_faiss(embeddings):
#     global ids
#     try:
#         for item in embeddings:
#             vector = np.array(item['embedding']).astype('float32').reshape(1, -1)
#             faiss_index.add(vector)  # Add the embedding to the FAISS index
#             ids.append(item['text'])  # Store the unique id for the text
#     except Exception as e:
#         logging.error(f"Error storing embeddings in FAISS: {e}")

# def create_and_store_embeddings_from_csv(csv_file_paths):
#     for csv_file_path in csv_file_paths:
#         df = pd.read_csv(csv_file_path)
#         text_chunks = df['Expectations'].tolist()  # Assuming 'Expectations' is the column with text
#         embeddings = get_embeddings(text_chunks)
#         store_embeddings_in_faiss(embeddings)

# # File paths for CSV files
# # File paths for CSV files
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

# # Create and store embeddings
# create_and_store_embeddings_from_csv(csv_file_paths)

# # Logging to confirm embeddings stored
# logging.info(f"Total embeddings stored in FAISS: {faiss_index.ntotal}")

# def query_faiss(query_text, top_k=5):
#     """Query the FAISS index with a text query and return the top_k closest documents."""
#     query_embedding = get_embeddings([query_text])[0]['embedding']  # Generate embedding for the query
#     vector = np.array(query_embedding).astype('float32').reshape(1, -1)  # Reshape for FAISS

#     # Step 2: Perform the search in the FAISS index
#     distances, indices = faiss_index.search(vector, top_k)

#     # Step 3: Retrieve the corresponding documents
#     results = []
#     for i in range(top_k):
#         if indices[0][i] >= 0:  # Check for valid index
#             results.append({
#                 'text': ids[indices[0][i]],  # Retrieve the text based on the stored ID
#                 'distance': distances[0][i]  # Distance from the query
#             })
#     return results

# # Example query
# query_string = "Get all the expectations of leadership attribute of vice president"
# results = query_faiss(query_string, top_k=5)  # Adjust top_k as needed

# if results:
#     print("Query Results:")
#     for idx, result in enumerate(results):
#         print(f"{idx + 1}. Text: {result['text']} | Distance: {result['distance']}")
# else:
#     print("No results found.")




import pandas as pd
import os
import logging
from dotenv import load_dotenv
from openai import AzureOpenAI
import numpy as np
import faiss
from time import sleep
from flask import  current_app

# Load environment variables
load_dotenv()
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_EMBEDDING_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL")

if not all([AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_EMBEDDING_MODEL]):
    raise ValueError("Azure OpenAI credentials are not properly set in the environment variables.")

# Initialize OpenAI client
openai_client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

# Setup logging
logging.basicConfig(level=logging.INFO)

# FAISS index initialization
embedding_dimension = 1536  # Adjust based on the embedding model used
faiss_index = faiss.IndexFlatL2(embedding_dimension)  # Create a FAISS index for L2 distance
ids = []  # List to hold the unique ids for each document


# File name for saving/loading the FAISS index
faiss_index_file =current_app.config['INDEX_FILE']
ids_file = current_app.config['IDS_FILE']

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

def store_embeddings_in_faiss(embeddings):
    global ids
    try:
        for item in embeddings:
            vector = np.array(item['embedding']).astype('float32').reshape(1, -1)
            faiss_index.add(vector)  # Add the embedding to the FAISS index
            ids.append(item['text'])  # Store the unique id for the text
    except Exception as e:
        logging.error(f"Error storing embeddings in FAISS: {e}")

def create_and_store_embeddings_from_csv(csv_file_paths):
    for csv_file_path in csv_file_paths:
        df = pd.read_csv(csv_file_path)

        df['processed_text'] = df.apply(preprocess_row, axis=1)
        text_chunks = df['processed_text'].tolist()

        # text_chunks = df['Expectations'].tolist()  # Assuming 'Expectations' is the column with text
        embeddings = get_embeddings(text_chunks)
        store_embeddings_in_faiss(embeddings)

# Function to save FAISS index and ids to disk
def save_faiss_index(index, index_file, ids_list, ids_file):
    faiss.write_index(index, index_file)  # Save FAISS index to a file
    np.save(ids_file, np.array(ids_list))  # Save ids list to a separate file
    logging.info(f"FAISS index and ids saved to {index_file} and {ids_file}.")

# Function to load FAISS index and ids from disk
def load_faiss_index(index_file, ids_file):
    global faiss_index, ids
    if os.path.exists(index_file) and os.path.exists(ids_file):
        faiss_index = faiss.read_index(index_file)  # Load FAISS index from a file
        ids = np.load(ids_file).tolist()  # Load ids from the file
        logging.info(f"FAISS index and ids loaded from {index_file} and {ids_file}.")
    else:
        logging.error(f"Index or ids file not found. Please ensure the files exist.")

# File paths for CSV files
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

# Create and store embeddings if needed, and then save FAISS index
# create_and_store_embeddings_from_csv(csv_file_paths)
# save_faiss_index(faiss_index, faiss_index_file, ids, ids_file)

# Logging to confirm embeddings stored
# logging.info(f"Total embeddings stored in FAISS: {faiss_index.ntotal}")

# Before querying, ensure you load the FAISS index from the file
load_faiss_index(faiss_index_file, ids_file)


def query_faiss(role, top_k=50):
    """Query the FAISS index with a text query and return the top_k closest documents."""
    query_embedding = get_embeddings([role])[0]['embedding']  # Generate embedding for the query
    vector = np.array(query_embedding).astype('float32').reshape(1, -1)  # Reshape for FAISS

    # Step 2: Perform the search in the FAISS index
    distances, indices = faiss_index.search(vector, top_k)

    # Step 3: Retrieve the corresponding documents
    results = []
    for i in range(top_k):
        if indices[0][i] >= 0:  # Check for valid index
            results.append({
                'text': ids[indices[0][i]],  # Retrieve the text based on the stored ID
            })
    return [result for result in results if role.lower() in result['text'].lower()]


# Example query
# query_string = "managing director Challenge the status quo"


# Now query the index
# results = query_faiss(query_string, top_k=30)  # Adjust top_k as needed

# if results:
#     print("Query Results:")
#     for idx, result in enumerate(results):
#         print(f"{idx + 1}. Text: {result['text']}")
# else:
#     print("No results found.")
