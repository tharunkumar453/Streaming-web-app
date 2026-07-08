# serializers.py
from rest_framework import serializers
from SAS_GENERATOR.models import Movies,MovieUrls



class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movies
        fields = [
            "Movie_id",
            "title",
            "uploaded_at",
            "blob_url_thumbnail"
        ]

class VideoFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieUrls
        fields = [
            "Movie_url_id",
            "url_for_preview",
            "blob_url"  
        ]

class MovieDetailsSerializer(serializers.ModelSerializer):

    files = VideoFileSerializer(

        many=True,
        read_only=True
    )

    class Meta:
        model = Movies
        fields = [
            "Movie_id",
            "title",
            "description",
            "cast",
            "zoner",
            "uploaded_at",
            "files"
        ]

class ReelviewSerializer(serializers.ModelSerializer):

    files=VideoFileSerializer(many=True,read_only=True)
    class Meta:
        model=Movies
        fields=[
            "Movie_id",
            "title",
            "uploaded_at",
            "files"
        ]

