from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Following_Follower
from .serializers import FollowingSerializer


from .models import DeviceNotification

class RegisterDeviceAPIView(CreateAPIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.user.id

        fcm_token = request.data.get( "registration_id")

        platform = request.data.get("type","web")

        if not fcm_token:
            return Response({"error":"fcm_token required"},status=400)

        DeviceNotification.objects.update_or_create(
            fcm_token=fcm_token,
            defaults={
                "user_id": user_id,
                "platform": platform,
                "active": True
            }
        )
        logging.info("device added")

class Following_Follower_view(CreateAPIView):
    def post(self,request,channel_id):
        try:
            Following_Follower.Create(
                following_id=channel_id,
                follower_id=request.user.id,
                follower_email=request.user.email

            )
            return Response("you Followinif this channel")
        except Exception as e :
            logging.error(f"{e}")


    


class Follwed_by_me(ListAPIView):
    def get(self,request):
        permission_classes=[IsAuthenticated]
        serializer_class=FollowingSerializer
        queryset=Following_Follower.objects.get(follower_id=request.user.id).order_by("-uploaded_at")
