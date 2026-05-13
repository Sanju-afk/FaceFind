from fastapi import APIRouter,UploadFile, File, HTTPException
import os
import shutil
import uuid
from app.services.vector_service import search_embedding
from app.services.face_service import face_service
from app.tasks.face_tasks import process_and_index_face



router = APIRouter(prefix = "/faces", tags = ["faces"])

TEMP_DIR = "/tmp/facefind"
os.makedirs(TEMP_DIR, exist_ok=True)

#now our API waits for celery using delay()
@router.post("/index")
def index_face(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    temp_path = os.path.join(TEMP_DIR, unique_filename)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    #Hand off to Celery for async processing
    process_and_index_face.delay(temp_path, unique_filename)

    return {
        "message" : "Image received and is being processed. Check back later for results.",
        "file" : unique_filename
    }

# search function is left synchrnonous 
# Security doors need an immediate "UNLOCK" response, so search shouldn't be queued!
@router.post("/search")
def search_face(file: UploadFile = File(...)):
    temp_filename = f"query_{uuid.uuid4()}.jpg"
    temp_path = os.path.join(TEMP_DIR, temp_filename)

    with open( temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        embedding = face_service.get_embedding(temp_path)
        if embedding is None:
            raise HTTPException(status_code=400, detail="No face detected in query")
        
        # Search the vector database using pgvector 
        # [cite: 138, 294]
        results = search_embedding(embedding)
        return {"matches": results}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed : {str(e)}")    
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

























































