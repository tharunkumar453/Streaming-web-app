from django.db import models
from django.utils import timezone
from datetime import timedelta


class Subscriptionplan(models.Model):

    plan_id = models.CharField(
            max_length=100,
            primary_key=True,
            unique=True
    )

    plan_name = models.CharField(max_length=100)

    price = models.PositiveIntegerField()

    duration = models.PositiveIntegerField()

    def __str__(self):
        return self.plan_name


class Payment(models.Model):

    STATUS = (
            ("CREATED", "CREATED"),
            ("VERIFIED", "VERIFIED"),
            ("SUCCESS", "SUCCESS"),
            ("FAILED", "FAILED"),
            ("REFUNDED", "REFUNDED"),
        )

    user_id = models.CharField(max_length=100)
    user_email = models.EmailField(max_length=100,default=None,null=True,blank=True)

    order_id = models.CharField(max_length=100,unique=True,db_index=True)

    plan_id = models.CharField(max_length=100)

    payment_id = models.CharField(max_length=100,blank=True,null=True)

    amount = models.PositiveIntegerField()

    status = models.CharField(max_length=20,choices=STATUS,default="CREATED")
        

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.order_id


class UserSubscription(models.Model):

    user_id = models.CharField(max_length=100)

    plan_id = models.CharField(max_length=100)

    start_date = models.DateTimeField()

    end_date = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user_id