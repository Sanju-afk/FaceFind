import logging
from typing import Optional,Dict,Any

import cv2
import numpy as np
from insightface.app import FaceAnalysis

#Logging config
logger = logging.getLogger(__name__)


#--------------------------
#Face Service
#------------------------
class FaceService:
    
    def __init__(self):
        logger.info("Initializing Insight Face Model....")

        try:
            self.model = FaceAnalysis(
                name = "buffalo_l",
                root = "models",
                providers = ["CPUExecutionProvider"]
            )
            self.model.prepare(ctx_id = 0)
            logger.info("Insight Face Model initialised successfully")

        except Exception as e:
            logger.exception("Failed to initialise face model")
            raise RuntimeError(f"Model initialisation failed : {e}")

    
    #Load Image
    def load_image(self, image_path : str) -> np.ndarray:
        image = cv2.imread(image_path)

        if image is None:
            raise ValueError(f"Could not read image : {image_path}")

        return image
    
    
    #Detect Faces
    def detect_faces(self, image : np.ndarray):
        try:
            faces = self.model.get(image)
            return faces
        except Exception as e:
            logger.exception("FaceTime detection failed")
            raise RuntimeError(f"FaceTime detection error : {e}")
    

    #Extract Embedding
    def get_embedding(self,image_path : str) -> Optional[np.ndarray]:
        try:
            image = self.load_image(image_path)
            faces = self.detect_faces(image)

            if len(faces) == 0:
                logger.warning(f"No faces detected in {image_path}")
                return None
            
            #largest face selection
            largest_face = max(
                faces,
                key = lambda face : ( 
                    (face.bbox[2] - face.bbox[0] )* (face.bbox[3] - face.bbox[1])                
                )
            )
            embedding = largest_face.normed_embedding
            
            if embedding is None:
                logger.warning("Embedding operation failed")
                return None

            return embedding.astype("float32")

        except Exception as e:
            logger.exception("Embedding extraction failed")
            raise RuntimeError(f"Embedding extraction error : {e}")
    

    #Extract Full Face Metadata
    def get_face_data(self, image_path : str) -> Optional[Dict[str, Any]]:
        try:
            image = self.load_image(image_path)
            faces = self.detect_faces(image)

            if len(faces) == 0:
                logger.warning(f"No faces detected in {image_path}")
                return None
            
            largest_face = max(
                faces,
                key = lambda face : (
                    (faces.bbox[2] - face.bbox[0]) * (face.bbox[3] - face.bbox[1])
                )
            )

            return {
                "embedding" : largest_face.embedding.astype("float32"),
                "bbox" : largest_face.bbox.tolist(),
                "confidence" : float(largest_face.det_score)
            }
        except Exception as e:
            logger.exception("Face metadata extraction failed")
            return None

#Singleton Instance
face_service = FaceService()











































