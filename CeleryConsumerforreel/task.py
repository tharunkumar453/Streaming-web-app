import os
import shutil

import logging


from celery_app import celery_app_instance
from FilePathCreate import FilePathCreator
from FilePathDelete import FilePathDeleteclass

from Task_upload import file_upload_to_blob
from Task_download import download_video

from Chunk_GEN import Chunk_generator

@celery_app_instance.task(
    name="reels_processing_task",
    
    queue="reels_processing_queue",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries":3},
    acks_late=True,
)

def process_Reel(self, blob_url, movie_id):

    logging.info(f"Received {movie_id} for {blob_url}")
    

    file_path, output_folder, local_folder = FilePathCreator().create_file_paths(movie_id)

    
    if not file_path:
        logging.error("file path not created")
        return
    else:
        logging.info(f"file path created for video_id: {movie_id}")
   c
    
    chunk_gen_out = Chunk_generator(file_path, output_folder)

    if(not chunk_gen_out):
        logging.error(f"Failed to generate HLS for video_id: {movie_id}")

    else:
       
        file_upload_to_blob(output_folder,movie_id) #uploading the hls output to blob storage
        logging.info(f"File uploaded successfully to blob storage for video_id: {movie_id} from {output_folder}")
       


    try:
       FilePathDeleteclass().delete_file_path(output_folder, local_folder)    
    except Exception as e:
        logging.error(f"Failed to delete file path for video_id: {e}")


    
    
  









    