from django.contrib import admin
from .models import Subscriptionplan, Payment, UserSubscription

# Register your models here
admin.site.register(Subscriptionplan)
admin.site.register(Payment)
admin.site.register(UserSubscription)