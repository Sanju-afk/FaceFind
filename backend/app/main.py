from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import faces

app = FastAPI(title="FaceFind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #this should be changed to react app url in production
    allow_methods=["*"],
    allow_credentials=True, 
    allow_headers=["*"],
)

app.include_router(faces.router)

@app.get("/")
def health_check():
    """"
        Used by Docker/Cloud providers
    """
    return {
        "status" : "online",
        "message": "FaceFind API is up and running!"
    }








































