from app.core.celery_app import celery_app
from app.services.face_service import face_service
from app.services.storage_service import upload_image  
from app.services.vector_service import add_embedding
import os

@celery_app.task
def process_and_index_face(temp_path : str, unique_filename : str):
    try:
        embedding = face_service.get_embedding(temp_path)
        if embedding is None:
            return {"status" : "failed", "error" : "No face detected in image"}
        
        public_url = upload_image(temp_path, unique_filename)

        add_embedding(public_url, embedding)
        return {"status": "success", "url" : public_url}
    
    except Exception as e:
        return {"status" : "failed", "error" : str(e)}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)











































