import base64
import json
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView,RetrieveAPIView
from dotenv import load_dotenv

import os
load_dotenv()  # Load environment variables from .env file
CDN_DOMAIN = os.getenv("CDN_DOMAIN")

from SAS_GENERATOR.models import Movies, MovieUrls,PREMIUM_USER
from .serializer import MovieListSerializer,MovieDetailsSerializer ,ReelviewSerializer
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

        print(serializer.data)
        print(serializer.data["files"][0]["url_for_preview"])
        if(serializer.data["files"][0]["is_have_plan"] and not PREMIUM_USER.objects.filter(user_id=request.user.id).exists()):
            return Response({"error": "You need a premium subscription to access this content."}, status=403)

        else:
            response = Response({
                "movie": serializer.data,
                "blob_url": f"{CDN_DOMAIN}/{serializer.data['files'][0]['blob_url']}"
            })
            return response
      
    
class ReelsListView(ListAPIView):
    permission_classes = [AllowAny] 
    queryset = Movies.objects.filter(reel=True).order_by("-uploaded_at")
    serializer_class = ReelviewSerializer
    pagination_class = MovieCursorPagination

    
    