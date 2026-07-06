import logging
import json
import azure.functions as func
from celery import Celery
REDIS_URL="redis://:0RMNBgSGiCe5HVRzIHmv9eP52W-KqVdjrAZCABZ8ruA=@azredis.malaysiawest.redis.azure.net:10000/0"




celery_client = Celery(
    "producer",
    broker=REDIS_URL
)

app = func.FunctionApp()

@app.event_grid_trigger(arg_name="azeventgrid")
def OriginalVideosContainer(azeventgrid: func.EventGridEvent):
    logging.info('Python EventGrid trigger processed an event')
 
    logging.info("HEY --> Event received!")

    try:
        data = azeventgrid.get_json()

        logging.info(f"Event ID: {azeventgrid.id}")
        logging.info(f"Event Data: {data}")

        blob_url = data.get("url")

        if blob_url:

        

            celery_client.send_task(
                "video_processing_task",
                args=[blob_url, blob_url.split("/")[-1].split(".")[0]],
                queue="video_processing_queue"
                )


            logging.info(f"Blob URL pushed to Redis: {blob_url}")

        else:
            logging.warning("No blob URL found in event")

    except Exception as e:
        logging.error(f"Error: {str(e)}")

    logging.info("Function completed successfully")
