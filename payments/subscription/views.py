from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import logging
from django.conf import settings
import razorpay
from .models import Subscriptionplan, Payment,UserSubscription
from payments.celery import app
import hmac
import hashlib
from .serializer import SubscriptionPlanSerializer
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
RAZORPAY_WEBHOOK_SECRET = settings.RAZORPAY_WEBHOOK_SECRET


client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)



class planList(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        plans = Subscriptionplan.objects.all()
        serializer = SubscriptionPlanSerializer(plans, many=True)
        return JsonResponse(serializer.data ,safe=False)

class CreateOrder(APIView):
    permission_classes = [AllowAny]

    def post(self, request,plan_id):

        if not Subscriptionplan.objects.filter(plan_id=plan_id).exists():
            return Response({"error": "Plan not found"}, status=404)
        try:
            plan_row = Subscriptionplan.objects.get(plan_id=plan_id)
            
            amount = plan_row.price * 100  # Convert to paise


            order = client.order.create({

                "amount": amount,

                "currency": "INR",

                "payment_capture": 1

            })
            Payment.objects.create(
                user_id="1",
                user_email="tharunkumarvana453@gmail.com",

                order_id=order["id"],
                plan_id=plan_id,

                amount=amount/100,

                status="CREATED"

            )



            return JsonResponse({

                "order_id": order["id"],

                "amount": amount/100,

                "key": settings.RAZORPAY_KEY_ID

        })
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        


class VerifyPayment(APIView):
    permission_classes = [AllowAny]

    def post(self,request):

        params = {

            "razorpay_order_id":
                request.data["razorpay_order_id"],

            "razorpay_payment_id":
                request.data["razorpay_payment_id"],

            "razorpay_signature":
                request.data["razorpay_signature"]

        }

        try:

            client.utility.verify_payment_signature(params)
            print(request.data)

            order_id = request.data["razorpay_order_id"]

            payment_id = request.data["razorpay_payment_id"]

            UpdatePayments(order_id,payment_id)
        except Exception as e:
            logging.error(f"Payment verification failed: {str(e)}")
            return Response({"status":"failed"},status=400)

        return Response({
            "status":"SUCCESS",
        })




@csrf_exempt
def razorpay_webhook(request):

    body = request.body

    received_signature = request.headers.get("X-Razorpay-Signature")

    generated_signature = hmac.new(
        settings.RAZORPAY_WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(received_signature,generated_signature):
        return HttpResponse(status=400)

    payload = json.loads(body)
    event = payload["event"]
    if event == "payment.captured": 
        payment = payload["payload"]["payment"]["entity"]

        order_id = payment["order_id"]
        payment_id = payment["id"]
        amount = payment["amount"]
        UpdatePayments(order_id, amount, payment_id,status="SUCCESS")

    elif event == "payment.failed":

        payment = payload["payload"]["payment"]["entity"]
        order_id = payment["order_id"]
        payment_id = payment["id"]
        UpdatePayments(order_id,0, payment_id,status="FAILED")



    return HttpResponse(status=200)


    

def UpdatePayments(order_id,payment_id):
    try:
        pay=Payment.objects.filter(order_id=order_id).first()
        if not pay :
            return
        if pay.status=="SUCCESS":
            return 
        pay.payment_id=payment_id
        pay.status="SUCCESS"
        pay.save()
        plan_row = Subscriptionplan.objects.get(plan_id=pay.plan_id)
        end_date=timezone.now() + timedelta(days=plan_row.duration)
        UserSubscription.objects.update_or_create(
            user_id=pay.user_id,
            plan_id=plan_row.plan_id,
            is_active=True,
            start_date=timezone.now(),
            end_date=end_date  # Assuming 30 days subscription
        )
        app.send_task(
            'update_premium_user_task',
            args=[pay.user_id, pay.user_email, plan_row.plan_name, True, timezone.now(), end_date],
            queue='premium_user_update_queue'
        )
    except Exception as e:
        logging.error(f"Failed to update payment status: {str(e)}")
        return Response({
            "status":"amount is miss consist or failed with order id"
        },status=400)