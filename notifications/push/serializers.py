from rest_framework import serializers

from .models import DeviceNotification, Following_Follower


class DeviceNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceNotification

        fields = ["fcm_token"]
    
class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Following_Follower

        fields=["following_id"]