import base64
import json
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView,RetrieveAPIView
from dotenv import load_dotenv
import os
load_dotenv()  # Load environment variables from .env file

KEY_PAIR_ID = os.getenv("KEY_PAIR_ID")


from SAS_GENERATOR.models import Movies, MovieUrls
from .serializer import MovieListSerializer,MovieDetailsSerializer 

from rest_framework.response import Response

from botocore.signers import CloudFrontSigner
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from datetime import datetime, timedelta, timezone
from django.http import JsonResponse

def rsa_signer(message):
    return private_key.sign(
        message,
        padding.PKCS1v15(),
        hashes.SHA1()
    )

with open("cloudfront_private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )
    
cloudfront_signer = CloudFrontSigner(
    KEY_PAIR_ID,
    rsa_signer
)
cdn_domain = os.getenv("cdn_domain")




def cf_b64(data: bytes):
    return (
        base64.b64encode(data)
        .decode()
        .replace("+", "-")
        .replace("=", "_")
        .replace("/", "~")
    )


def generate_cloudfront_cookies(resource):

    expire = datetime.now(timezone.utc) + timedelta(hours=3)

    policy = cloudfront_signer.build_policy(resource,expire).encode()

    signature = rsa_signer(policy)

    return {
        "CloudFront-Policy": cf_b64(policy),
        "CloudFront-Signature": cf_b64(signature),
        "CloudFront-Key-Pair-Id": KEY_PAIR_ID
    }



class MovieListView(ListAPIView):
    permission_classes = [AllowAny]  # Allow any user to access this view
    queryset = Movies.objects.all().order_by("-uploaded_at")

    serializer_class = MovieListSerializer


class MovieDetailsView(RetrieveAPIView):

    permission_classes = [AllowAny]

    def get(self, request, Movie_id):

        movie = Movies.objects.filter(Movie_id=Movie_id).first()

        if movie is None:
            return Response({"error": "Movie not found"},status=404)

        serializer = MovieDetailsSerializer(movie)

        cookies = generate_cloudfront_cookies(f"{cdn_domain}/*")

        response = Response({
            "movie": serializer.data,
            "preview_url": f"{cdn_domain}/{serializer.data['files'][0]['url_for_preview']}",
            "blob_url": f"{cdn_domain}/{serializer.data['files'][0]['blob_url']}"
        })
        print(serializer.data["files"][0]["url_for_preview"])
        for key, value in cookies.items():

            response.set_cookie(
                key=key,
                value=value,
                secure=True,
                httponly=True,
                samesite="None",
                path="/",
                domain=f"{cdn_domain}", 
            )

        return response