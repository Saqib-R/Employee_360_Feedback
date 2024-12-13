import numpy as np
import pandas as pd
import os
import logging
from dotenv import load_dotenv
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from openai import AzureOpenAI
from flask import  current_app

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
        path=os.path.join(current_app.config['STORE_NAME']), 
        settings=Settings(),
        tenant=DEFAULT_TENANT,
        database=DEFAULT_DATABASE,
    )

collection = chroma_client.get_or_create_collection(name=current_app.config["COLLECTION_NAME"])



def get_query_embedding(query):
    try:
        response = openai_client.embeddings.create(
            input=query,
            model=AZURE_OPENAI_EMBEDDING_MODEL
        )
        return response.data[0].embedding
    except Exception as e:
        logging.error(f"Error getting embedding for query: {e}")
        return None

# def get_query_expectations(role, collecttion_name, top_k=30):
#     print(collecttion_name)

#     # Construct the query string
#     query_text = role
#     print(query_text)

#     # Get the embedding for the constructed query
#     query_embedding = get_query_embedding(query_text)
#     if query_embedding is None:
#         logging.error("Failed to get query embedding. Exiting query.")
#         return []

#     # Query the ChromaDB collection using the embedding
#     try:
#         results = collection.query(
#             query_embeddings=[query_embedding],
#             n_results=top_k
#         )
#         print(results)
#         # return [result for result in enumerate(results['documents'][0]) if role.lower() in result.lower()]
#         return results['documents'][0]
#     except Exception as e:
#         print((f"Error querying ChromaDB: {e}"))
#         logging.error(f"Error querying ChromaDB: {e}")
#         return []

# query_string = "Get all the expectations of leadership attribute of vice president"
# results = get_query_expectations("Managing Director")
# if results:
#     print("Query Results:")
#     for idx, document in enumerate(results):
#         print(f"{idx + 1}. {document}")
# else:
#     print("No results found.")


# NEW METHOD TRYING
def get_query_expectations(role, collection_name, top_k=40):
    query_text = role  # Using the role as the query text
    query_embedding = get_query_embedding(query_text)
    if query_embedding is None:
        logging.error("Failed to get query embedding. Exiting query.")
        return []

    try:
        results = collection.query(
            query_embeddings=[query_embedding], 
            n_results=top_k
        )

        # Assuming `results['metadatas']` contains metadata for each document
        filtered_results = []
        for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
            if 'Title' in metadata and role.lower() in metadata['Title'].lower():
                filtered_results.append(doc)

        print("\nResult", results,"\nFormatted result", filtered_results)


        return filtered_results
    except Exception as e:
        logging.error(f"Error querying ChromaDB: {e}")
        return []

# END








# import numpy as np
# import pandas as pd
# import os
# import logging
# from dotenv import load_dotenv
# import chromadb
# from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
# from openai import AzureOpenAI
# from flask import current_app

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

# def get_query_embedding(query):
#     try:
#         response = openai_client.embeddings.create(
#             input=query,
#             model=AZURE_OPENAI_EMBEDDING_MODEL
#         )
#         return response.data[0].embedding
#     except Exception as e:
#         logging.error(f"Error getting embedding for query: {e}")
#         return None

# def get_query_expectations(role, top_k=50):
        
#     # Query the ChromaDB collection using metadata filtering
#     try:
#         print(f"Searching for documents with role: {role}")
        
#         # Fetch documents that match the role in the metadata
#         # results = collection.get(
#         #     where={"role": role}  # Match the 'role' in metadata
#         # )
        
#         # if not results['documents']:
#         #     logging.info(f"No documents found for role: {role}")
#         #     return []
        
#         # If you want to use top_k and embeddings for additional filtering (optional):
#         # if top_k > 0:
#         # print("Using embeddings for additional filtering with top_k")
        
#         # Get the embedding for the constructed query (role)
#         query_embedding = get_query_embedding(role)
#         if query_embedding is None:
#             logging.error("Failed to get query embedding. Exiting query.")
#             return []
        
#         # Perform an embedding-based similarity query with top_k results
#         similarity_results = collection.query(
#             query_embeddings=[query_embedding],
#             n_results=top_k
#         )
#         print(similarity_results['documents'][0])
#         filtered_results = [
#             document for document in similarity_results['documents'][0]
#             if role.lower() in document.lower()  # Check if the role is in the document text
#         ]

#         return filtered_results
    
#     except Exception as e:
#         print(f"Error querying ChromaDB: {e}")
#         logging.error(f"Error querying ChromaDB: {e}")
#         return []

# # Example usage
# # role_to_search = "Vice President"
# # results = get_query_expectations(role_to_search)  # Set top_k=0 to disable similarity filtering
# # if results:
# #     print("Query Results:")
# #     for idx, document in enumerate(results):
# #         print(f"{idx + 1}. {document}")
# # else:
# #     print("No results found.")
