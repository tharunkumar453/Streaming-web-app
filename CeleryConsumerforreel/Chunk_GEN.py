import subprocess
import logging
def Chunk_generator(file_path,output_folder):
     logging.info(f"Starting HLSCHUNK generation for {file_path} into {output_folder}")
     try:

          cmd = f'''
          ffmpeg -i "{file_path}" \
          -vf "fps=1/5,scale=320:-1,tile=3x4" \
          -y "{output_folder}/thumbnail.jpg" && \
          ffmpeg -i "{file_path}" \
          -map 0:v -map 0:a? \
          -map 0:v -map 0:a? \
          -map 0:v -map 0:a? \
          -filter:v:0 scale=640:360 \
          -filter:v:1 scale=1280:720 \
          -filter:v:2 scale=1920:1080 \
          -c:v libx264 \
          -c:a aac \
          -preset veryfast \
          -b:v:0 800k \
          -b:v:1 2500k \
          -b:v:2 5000k \
          -var_stream_map "v:0,a:0,name:360p v:1,a:1,name:720p v:2,a:2,name:1080p" \
          -master_pl_name master.m3u8 \
          -f hls \
          -hls_time 6 \
          -hls_playlist_type vod \
          -hls_segment_filename "{output_folder}/%v/seg_%03d.ts" \
          "{output_folder}/%v/index.m3u8"
          '''

          result = subprocess.run(
          cmd,
          shell=True,
          capture_output=True,
          text=True
          )

          print(result.returncode)
          print(result.stdout)
          print(result.stderr)

     except Exception as e:
          logging.error(f"Error during HLS generation: {e}")
          return False
     logging.info(f"HLS generated succes in {output_folder}."  )
     return True
     
