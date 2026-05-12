import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
BUCKET_NAME = "face-images"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_image(local_path: str, filename: str):
    """
    Uploads file to Supabase Storage and returns the public URL.
    """
    with open(local_path, "rb") as f:
        supabase.storage.from_(BUCKET_NAME).upload(
            path=filename,
            file=f,
            file_options={"content-type": "image/jpeg"}
        )
    
    # Return the URL so the frontend can display it
    return supabase.storage.from_(BUCKET_NAME).get_public_url(filename)