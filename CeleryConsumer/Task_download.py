import os
import logging
import uuid
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
AZCOPY_AUTO_LOGIN_TYPE = os.getenv("AZCOPY_AUTO_LOGIN_TYPE")
AZCOPY_TENANT_ID= os.getenv("AZCOPY_TENANT_ID")
AZCOPY_SPA_APPLICATION_ID = os.getenv("AZCOPY_SPA_APPLICATION_ID")

AZCOPY_SPA_CLIENT_SECRET = os.getenv("AZCOPY_SPA_CLIENT_SECRET")



from azpype.commands.copy import Copy

def download_video(blob_url,file_path):

    logging.info(f"Starting video ddownload")

    try:

        Copy(
        source=blob_url,
        destination=file_path,
        recursive=True,
       
        ).execute()

        return file_path
    except Exception as e:
        logging.error(f"Error processing video ===>Error: {str(e)}")
        return
        