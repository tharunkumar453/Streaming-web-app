from azpype.commands.copy import Copy
from celery_app import celery_app_instance
import os
import logging
from dotenv import load_dotenv
load_dotenv()  

AZCOPY_AUTO_LOGIN_TYPE = os.getenv("AZCOPY_AUTO_LOGIN_TYPE")
AZCOPY_TENANT_ID= os.getenv("AZCOPY_TENANT_ID")
AZCOPY_SPA_APPLICATION_ID = os.getenv("AZCOPY_SPA_APPLICATION_ID")
AZCOPY_SPA_CLIENT_SECRET = os.getenv("AZCOPY_SPA_CLIENT_SECRET")
blob_upload_url = os.getenv("blob_upload_url")

def file_upload_to_blob(chunk_path,video_id):

    try:
        result_back=Copy(
            source=chunk_path,
            destination=blob_upload_url,
            recursive=True,
        ).execute()

        if(result_back.exit_code==0):
            logging.info(f"File uploaded successfully to {blob_upload_url}")

            url_=f"{chunk_path}/master.m3u8"
            
            try:
                r = celery_app_instance.send_task(
                    "db_update_task",
                    args=[video_id, url_],  

                    queue="db_update_queue"     
                )

                logging.info(f"Task sent to update DB with URL: {url_} with {r.id} task id")
            except Exception as e:
                logging.error(f"Error sending task to update DB --->Error: {str(e)}")
        else:
            logging.error(f"File upload failed to {blob_upload_url} with exit code: {result_back.exit_code}")
            return False
            
    except Exception as e:

        logging.error(f"Error uploading file to {blob_upload_url} --->Error: {str(e)}")
        return False

        