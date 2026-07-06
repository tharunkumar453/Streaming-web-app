from django.contrib import admin

# Register your models here.
from .models import CustomUserModel
admin.site.register(CustomUserModel)