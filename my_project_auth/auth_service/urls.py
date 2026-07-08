from django.urls import path
from .views import AddUserView, ResetPasswordView, LoginView,RefreshjwtView


urlpatterns = [
    path("add-user/", AddUserView.as_view(), name="add_user"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh-jwt/", RefreshjwtView.as_view(), name="refresh_jwt"),
]

