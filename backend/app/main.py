from fastapi import FastAPI,UploadFile, File,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import shutil
import uuid

from app.services.face_service import face_service
from app.services.vector_service import add_embedding, search_embedding
from app.services.storage_service import upload_image

load_dotenv()

app = FastAPI(title = "FaceFind API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use a temporary directory for processing
TEMP_DIR = "tmp/facefind"   
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "FaceSeek Backend Cloud-Ready"}

@app.post("/index")
def index_face(file: UploadFile = File(...)):
    # 1. Generate unique filename and temp path
    ext = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    temp_path = os.path.join(TEMP_DIR, unique_filename)

    # 2. Save locally temporarily
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save temp file: {str(e)}")

    try:
        # 3. Extract embedding FIRST using local temp file
        embedding = face_service.get_embedding(temp_path)

        if embedding is None:
            raise HTTPException(status_code=400, detail="No face detected in image")

        # 4. Upload to Supabase Storage
        public_url = upload_image(temp_path, unique_filename)

        # 5. Insert into Supabase PostgreSQL (pgvector)
        # We pass the public_url as the 'filename' so the frontend can render it later
        add_embedding(public_url, embedding)

        return {
            "message": "Image indexed successfully",
            "url": public_url
        }

    finally:
        # 6. Cleanup: ALWAYS delete the local file
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/search")
def search_face(file: UploadFile = File(...)):
    # 1. Setup temp query image
    ext = file.filename.split(".")[-1]
    temp_filename = f"query_{uuid.uuid4()}.{ext}"
    temp_path = os.path.join(TEMP_DIR, temp_filename)

    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. Extract query embedding
        embedding = face_service.get_embedding(temp_path)
        
    finally:
        # 3. Cleanup query image immediately
        if os.path.exists(temp_path):
            os.remove(temp_path)

    if embedding is None:
        raise HTTPException(status_code=400, detail="No face detected in query image")

    # 4. Search Supabase via RPC
    results = search_embedding(embedding)

    return {
        "matches": results
    }



