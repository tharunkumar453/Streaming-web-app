from django.urls import path

from .views import (
    RegisterDeviceAPIView,
   
    Following_Follower_view,
    Follwed_by_me

)

urlpatterns = [

    path("api/devices/register/",RegisterDeviceAPIView.as_view()),
   
    path("follow/<int:channel_id>",Following_Follower_view.as_view()),
    path("following/",Follwed_by_me.as_view())

]