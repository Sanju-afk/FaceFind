from celery import Celery
import os

#by default docker will expose redis on localhost:6379
redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery("facefind_tasks", 
                    broker=redis_url,
                    backend=redis_url,
                    include = ["app.tasks.face_tasks"] #this file takes care of the actual face indexing and searching logic, we import it here so that celery can discover the tasks when it starts up

)














