from django.urls import path
from .views import Upload_Movie, upload_Reel

urlpatterns = [
    path("upload-movie/", Upload_Movie.as_view(), name="upload_movie"),
    path("upload-reel/", upload_Reel.as_view(), name="upload_reel"),

]   