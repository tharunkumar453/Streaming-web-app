from rest_framework import serializers
from .models import Subscriptionplan

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptionplan
        fields = "__all__"