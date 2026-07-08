from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas,BlobSasPermissions


from django.views.decorators.csrf import csrf_exempt
from myproject_server.settings import ACCOUNT_NAME, ACCOUNT_KEY, CONTAINER_NAME_VIDEOS, CONTAINER_NAME_REELS
from django.http import JsonResponse
import uuid 
CONTAINER_NAME_THUMBNAILS = "processedvideos"

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Movies,MovieUrls
@csrf_exempt


def Generate_SAS_for_Movie(movie_id,CONTAINER_NAME,is_thumbnail=False):

        if is_thumbnail:
            filename = f"{movie_id}_thumbnail.jpg"
        else:
            filename = f"{movie_id}.mp4"# make file name unique

        #generate sas token for the blob
        sas_token = generate_blob_sas(
            account_name=ACCOUNT_NAME,
            container_name=CONTAINER_NAME,
            blob_name=filename,
            account_key=ACCOUNT_KEY,
            permission=BlobSasPermissions(
                write=True,#allow write permission+overwrite also if file exists
                create=True,#create new blob if it does not exist
            ),
            expiry=datetime.utcnow() + timedelta(hours=1)#valid for 1 hour
        )

        #blob_url with sas token
        blob_url = (
        f"https://{ACCOUNT_NAME}.blob.core.windows.net/"
        f"{CONTAINER_NAME}/{filename}?{sas_token}"
        )

        # for debuggingss
        print("blob_url:", blob_url)

        return blob_url

class Upload_Movie(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        movie_title= request.data.get("movie_title")
        movie_description = request.data.get("movie_description")
        movie_cast = request.data.get("movie_cast")
        movie_zoner = request.data.get("movie_zoner")
        

        try:
            print("movie_title:", movie_title)
            movie = Movies.objects.create(
                uploader_id=request.user.id,
                title=movie_title,
                description=movie_description,
                cast=movie_cast,
                zoner=movie_zoner,
                reel=False,
                movie_url_thumbnail=None
            )
            print("hi")

            blob_url = Generate_SAS_for_Movie(movie.Movie_id,CONTAINER_NAME_VIDEOS)
            blob_url_thumbnail = Generate_SAS_for_Movie(movie.Movie_id,CONTAINER_NAME_THUMBNAILS,is_thumbnail=True)
            movie.blob_url_thumbnail = blob_url_thumbnail
            movie.save()
            return JsonResponse({"blob_url": blob_url,"blob_url_thumbnail": blob_url_thumbnail}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)  
class upload_Reel(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        reel_title= request.data.get("reel_title")

        try:
            print("reel_title:", reel_title)
            reel = Movies.objects.create(
                uploader_id=request.user.id,
                title=reel_title,
                reel=True,
                movie_url_thumbnail=None
            )
            print("hi")

            blob_url = Generate_SAS_for_Movie(reel.Movie_id,CONTAINER_NAME_REELS)
            return JsonResponse({"blob_url": blob_url}, status=200)

        except Exception as e:
            print({"error": f"{e}"})
            return JsonResponse({"error": str(e)}, status=400)
        
