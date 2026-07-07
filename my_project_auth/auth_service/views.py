from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUserModel
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .tasks import EmailNotificationTask
from rest_framework.permissions import IsAuthenticated
from botocore.signers import CloudFrontSigner
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from datetime import datetime, timedelta, timezone
from django.http import JsonResponse
import base64
import json
import os
from dotenv import load_dotenv
load_dotenv()
KEY_PAIR_ID = os.getenv("KEY_PAIR_ID")
CDN_DOMAIN = os.getenv("CDN_DOMAIN")

private_key= serialization.load_pem_private_key(
    os.getenv("PRIVATE_KEY").encode(),
    password=None,
)
def rsa_signer(message):
    return private_key.sign(
        message,
        padding.PKCS1v15(),
        hashes.SHA1())

cloudfront_signer = CloudFrontSigner(KEY_PAIR_ID,rsa_signer)



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



class AddUserView(APIView):

    def post(self, request):
        email = request.data.get("email")
        phoneNumber= request.data.get("phone")
        password = request.data.get("password")

        if not email or not password or not phoneNumber:
            return Response({"detail": "Email, password, and phone are required."}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUserModel.objects.filter(email=email).exists():
            return Response({"detail": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUserModel.objects.create_user(email=email, password=password, phone=phoneNumber)
        try:
            EmailNotificationTask().send_email_notification(email)
        except Exception as e:
            print(f"Error sending email notification: {e}")

            
        return Response({"detail": "User registered successfully."}, status=status.HTTP_201_CREATED)



class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not email or not old_password or not new_password:
            return Response({"detail": "Email, old password, and new password are required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUserModel.objects.get(email=email)
            if not user.check_password(old_password):
                return Response({"detail": "Invalid old password."}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password reset successfully."}, status=status.HTTP_200_OK)
        except CustomUserModel.DoesNotExist:
            return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)




class LoginView(APIView):

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"detail": "Email and password are required."},status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUserModel.objects.get(email=email)
            if not user.check_password(password):
                return Response({"detail": "Invalid credentials."},status=status.HTTP_401_UNAUTHORIZED)

            # Generate JWT Tokens
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            # Create response
            response = Response({
                "access": str(access),
                "refresh": str(refresh),
                },
                status=status.HTTP_200_OK,
            )

            # Generate CloudFront signed cookies
            cookies = generate_cloudfront_cookies(f"{CDN_DOMAIN}/*")

            for key, value in cookies.items():
                print(f"Setting cookie: {key}={value}")
                print()
                response.set_cookie(
                    key=key,
                    value=value,
                    secure=True,
                    httponly=True,
                    samesite="None",
                    path="/"
                )
            return response

        except CustomUserModel.DoesNotExist:
            return Response({"detail": "Invalid credentials."},status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token
            return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


class RefreshCloudFrontCookieView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        cookies = generate_cloudfront_cookies(f"{CDN_DOMAIN}/*")
        response = Response({ "message": "CloudFront cookies refreshed"}, status=status.HTTP_200_OK )  
        for key, value in cookies.items():
            response.set_cookie(
                key,
                value,
                secure=True,
                httponly=True,
                samesite="None",
                path="/"
            )
        return response