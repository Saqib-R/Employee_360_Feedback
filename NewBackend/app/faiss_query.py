import pandas as pd
import os
import logging
from dotenv import load_dotenv
from openai import AzureOpenAI
import numpy as np
import faiss
from time import sleep

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


def query_faiss(query_text, top_k=5):
    """Query the FAISS index with a text query and return the top_k closest documents."""
    # Step 1: Get embedding for the query
    query_embedding = get_embeddings([query_text])[0]['embedding']  # Generate embedding for the query
    vector = np.array(query_embedding).astype('float32').reshape(1, -1)  # Reshape for FAISS

    # Step 2: Perform the search in the FAISS index
    distances, indices = faiss_index.search(vector, top_k)

    # Step 3: Retrieve the corresponding documents
    results = []
    for i in range(top_k):
        if indices[0][i] >= 0:  # Check for valid index
            results.append({
                'text': ids[indices[0][i]],  # Retrieve the text based on the stored ID
                'distance': distances[0][i]  # Distance from the query
            })
    print(distances,indices)
    return results


query_string = "Get all the expectations of leadership attribute of vice president"
results = query_faiss(query_string, top_k=5)  # Adjust top_k as needed

if results:
    print("Query Results:")
    for idx, result in enumerate(results):
        print(f"{idx + 1}. Text: {result['text']} | Distance: {result['distance']}")
else:
    print("No results found.")
