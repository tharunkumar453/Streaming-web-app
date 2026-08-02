from celery import Celery
import os
from dotenv import load_dotenv
load_dotenv()

REDIS_URL=os.getenv("REDIS_URL")



celery_app_instance = Celery(
    "video_worker",
    broker=REDIS_URL
)
  

celery_app_instance.conf.update(
    task_serializer="json", 
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,

    task_acks_late=True,
    worker_prefetch_multiplier=3,
    task_reject_on_worker_lost=True,
    soft_time_limit=1800,  # 30 min
    time_limit=1900   
)


celery_app_instance.autodiscover_tasks()