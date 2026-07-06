from django.urls import path
from .views import AddUserView, ResetPasswordView, LoginView
urlpatterns = [
    path("add-user/", AddUserView.as_view(), name="add_user"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    path("login/", LoginView.as_view(), name="login"),
]
