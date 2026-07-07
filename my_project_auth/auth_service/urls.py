from django.urls import path
from .views import AddUserView, ResetPasswordView, LoginView,RefreshCloudFrontCookieView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("add-user/", AddUserView.as_view(), name="add_user"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh-cloudfront-cookies/", RefreshCloudFrontCookieView.as_view(), name="refresh_cloudfront_cookies"),
]
    

urlpatterns += [
    path("api/token/refresh/", TokenRefreshView.as_view()),
]
