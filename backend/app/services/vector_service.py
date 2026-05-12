import os
import numpy as np
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def add_embedding(filename: str, embedding: np.ndarray):
    """
    Inserts filename and vector into the Supabase 'faces' table.
    """
    # Convert NumPy array to a standard Python list for Supabase
    vector_list = embedding.tolist()
    
    data = {
        "filename": filename,
        "embedding": vector_list
    }
    
    response = supabase.table("faces").insert(data).execute()
    return response

def search_embedding(query_embedding: np.ndarray, top_k: int = 5):
    """
    Calls the 'match_faces' RPC function you created in the Supabase SQL editor.
    """
    # Convert NumPy array to list
    vector_list = query_embedding.tolist()
    
    # RPC parameters must match your SQL function definition
    params = {
        "query_embedding": vector_list,
        "match_threshold": 0.5, # Lower is more similar for L2 distance
        "match_count": top_k
    }
    
    response = supabase.rpc("match_faces", params).execute()
    return response.data