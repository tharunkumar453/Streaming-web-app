import os
import shutil
import logging 
class FilePathDeleteclass:
    def delete_file_path(self, output_folder, local_folder):
        try:
            if os.path.exists(output_folder):
                shutil.rmtree(output_folder)
                logging.info(f"Output folder {output_folder} deleted successfully.")
            else:
                logging.warning(f"Output folder {output_folder} does not exist.")
        except Exception as e:
            logging.error(f"Error deleting output folder {output_folder} ===>Error: {str(e)}")  