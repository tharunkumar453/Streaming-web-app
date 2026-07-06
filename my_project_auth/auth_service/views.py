from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUserModel
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .tasks import EmailNotificationTask
# Create your views here.

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
        email = request.data.get("email")  # Frontend sends as 'username'
        password = request.data.get("password")

        if not email or not password:
            return Response({"detail": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUserModel.objects.get(email=email)
            if not user.check_password(password):
                return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)
        except CustomUserModel.DoesNotExist:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
