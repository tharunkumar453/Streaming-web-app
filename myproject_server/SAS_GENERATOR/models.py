from django.db import models
from django.conf import settings


class Movies(models.Model):
    Movie_id = models.AutoField(primary_key=True)
    uploader_id = models.BigIntegerField(blank=False,default=0)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    cast= models.TextField(null=True,blank=True)
    zoner = models.CharField(max_length=255,null=True,blank=True)
    reel = models.BooleanField(default=False)
    blob_url_thumbnail = models.URLField(max_length=2000, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.Movie_id) + " - " + self.title


class MovieUrls(models.Model):
    Movie_url_id = models.AutoField(primary_key=True)
    url_for_preview=models.URLField(max_length=2000, null=True, blank=True)
    is_have_plan=models.BooleanField(default=False)
    Movie = models.ForeignKey(
        Movies,
        on_delete=models.CASCADE,
        related_name="files"
    )
    blob_url = models.URLField(max_length=2000)
    
    def __str__(self):
        return f"File for {self.Movie.title}"

class PREMIUM_USER(models.Model):
    user_id = models.BigIntegerField(unique=True)
    user_email = models.EmailField(max_length=100,default=None,null=True,blank=True)
    is_premium = models.BooleanField(default=False)
    premium_start_date = models.DateTimeField(null=True, blank=True)
    premium_end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"User ID: {self.user_id} - Premium: {self.is_premium}"