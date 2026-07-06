import os
import logging
import uuid
class FilePathCreator:
    def create_file_paths(self, video_id):
        try:

            file_name = f"{video_id}.mp4"
            local_folder = "temp_folder" #loacl folder name
            os.makedirs(local_folder, exist_ok=True) # folder creation 
            file_path = os.path.join(local_folder, file_name) #add to path
            
        except Exception as e:
            logging.error(f"Error creating fi video_id: {video_id} ===>Error: {str(e)}")

        try:
            output_folder= str(uuid.uuid4()) # output folder name
            os.makedirs(output_folder, exist_ok=True)# folder creation for output
        except Exception as e:
            logging.error(f"Error creating output folder for video_id: {video_id} ===>Error: {str(e)}")
        return file_path, output_folder,local_folder