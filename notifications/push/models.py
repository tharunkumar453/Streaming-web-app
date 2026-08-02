from django.db import models


class DeviceNotification(models.Model):

    user_id = models.BigIntegerField(db_index=True)

    fcm_token = models.CharField(max_length=255, unique=True, null=False, default=" ")

    platform = models.CharField(max_length=20,default="web")

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id) + " - " + str(self.platform) + " - " + str(self.active)

class Following_Follower(models.Model):
    follower_id = models.BigIntegerField(default=None)
    follower_email = models.EmailField(default=None)

    following_id = models.BigIntegerField(default=None)
    uploaded_at=models.DateTimeField(auto_now_add=True)



    
    