import base64
import json
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView,RetrieveAPIView
from dotenv import load_dotenv

import os
load_dotenv()  # Load environment variables from .env file




from SAS_GENERATOR.models import Movies, MovieUrls
from .serializer import MovieListSerializer,MovieDetailsSerializer 
from .pagination import MovieCursorPagination
from rest_framework.response import Response


class MovieListView(ListAPIView):
    permission_classes = [AllowAny] 
    queryset = Movies.objects.all().order_by("-uploaded_at")
    serializer_class = MovieListSerializer
    pagination_class = MovieCursorPagination


class MovieDetailsView(RetrieveAPIView):
    permission_classes = [AllowAny]
    def get(self, request, Movie_id):
        movie = Movies.objects.filter(Movie_id=Movie_id).first()
        if movie is None:
            return Response({"error": "Movie not found"},status=404)
        serializer = MovieDetailsSerializer(movie)
        print(serializer.data["files"][0]["url_for_preview"])
        response = Response({
            "movie": serializer.data,
            "preview_url": f"{cdn_domain}/{serializer.data['files'][0]['url_for_preview']}",
            "blob_url": f"{cdn_domain}/{serializer.data['files'][0]['blob_url']}"
        })
      
    
class ReelsListView(ListAPIView):
    permission_classes = [AllowAny] 
    queryset = Movies.objects.filter(reel=True).order_by("-uploaded_at")
    serializer_class = MovieListSerializer
    pagination_class = MovieCursorPagination

    
    