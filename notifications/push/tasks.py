from celery import shared_task
from .models import DeviceNotification,Following_Follower
import logging
from firebase_admin import messaging

from django.template.loader import render_to_string

from pathlib import Path

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, get_connection
from django.core.mail import send_mail



def send_push_notification(device, fcm_token,video_title,video_id):
    logging.info(f"Preparing to send push notification to device {device.id} with FCM token: {fcm_token}")
    try:
        url=f"https://yourdomain.com/watch/{video_id}/"
        logging.info(f"Notification URL: {url}")
        message = messaging.Message(
            token=fcm_token,
            notification=messaging.Notification(
                title=video_title,
                body=f"New video uploaded: {video_title}",
                
            ),
            data={
                "url": url

            }

            
        )
        logging.info(f"Sending message: {message}")
        response=messaging.send(message)
        logging.info(f"Successfully sent message: {response}")
        
        logging.info(f"Notification sent to device {device.id} for video_id: {video_id}")

    except Exception as e:

        if "registration-token-not-registered" in str(e):

            device.active = False
            device.save()
            logging.info("Device deactivated due to invalid FCM token.")
        logging.error(f"Error sending notification to device: {str(e)}")





@shared_task(name="send_push_notification_task", queue="push_notification_queue")
def push_notification_task(user,video_title,video_id):
    logging.info(f"Sending push notification for user_id: {user}, video_title: {video_title}, video_id: {video_id}")
    try:
        logging.info(f"Fetching active devices for user_id: {user}")
        devices = DeviceNotification.objects.filter(
            user_id=user,
            active=True
        )
        logging.info(f"Found {devices.count()} active devices for user_id: {user}")
        logging.info(f"Active devices: {devices}")
        for device in devices:
            logging.info(f"Sending notification to device {device.id} with FCM token: {device.fcm_token}")  
            send_push_notification(device,device.fcm_token,video_title,video_id)
            logging.info(f"Notification sent to device {device.id} for video_id: {video_id}")

        logging.info("Notification sent successfully.")
    except Exception as e:
        logging.error("Error occurred while sending notification: %s", str(e))
    






@shared_task(
    name="email_notify_task",
    queue="email_notify_queue"
)
def email_notification_for_video_upload(
    user_id,
    video_title,

    video_id
):


    html_content = Path("/app/push/emails/new_video.html").read_text()

    html_content = (
        html_content
        .replace("{{TITLE}}", video_title)
        .replace("{{CHANNEL_ID}}", str(user_id))
        .replace(
            "{{VIDEO_URL}}",
            f"https://yourdomain.com/watch/{video_id}/"
        )
        )
     

    followers = Following_Follower.objects.filter(
        following_id=user_id
    )

    try:

        connection = get_connection(
            fail_silently=False
        )

        connection.open()

        messages = []

        for follower in followers:

            msg = EmailMultiAlternatives(
                subject=f"New Video: {video_title}",
                body=f"Watch now: https://yourdomain.com/watch/{video_id}/",
                from_email="noreply@yourdomain.com",
                to=[follower.follower_email],
                connection=connection,
            )

            msg.attach_alternative(
                html_content,
                "text/html"
            )

            messages.append(msg)

        connection.send_messages(messages)

        connection.close()

        logging.info(
            f"Successfully sent {len(messages)} emails"
        )

    except Exception as e:
        logging.error(
            f"Email notification error: {str(e)}"
        )
@shared_task(
    name="Registrationtask",
    queue="RegistrationQueue"
)
def Registrationtask(email):
    try:
        # Render the email template with context
        html_content = Path("/app/push/emails/welcome.html").read_text()
        html_content = (
        html_content
        .replace("{{EMAIL}}", email)
      
        )
        message = EmailMultiAlternatives(
            subject="Welcome to Our Platform",
            body="Thank you for registering with us.",
            from_email="noreply@yourdomain.com",
            to=[email],

          
        )
        message.attach_alternative(html_content, "text/html")
        message.send(fail_silently=False)
        logging.info(f"Registration email sent to {email}")
    except Exception as e:
        logging.error(f"Error sending registration email to {email}: {str(e)}") 

@shared_task(
    name="subscription_task",
    queue="subscription_queue"
)
def subscription_task(user_id, user_email, plan_name, start_date, end_date):
    try:
        # Render the email template with context
        html_content = Path("/app/push/emails/subscription.html").read_text()
        html_content = (
        html_content
        .replace("{{EMAIL}}", user_email)
        .replace("{{PLAN_NAME}}", plan_name)
        .replace("{{START_DATE}}", str(start_date))
        .replace("{{END_DATE}}", str(end_date))
      
        )
        message = EmailMultiAlternatives(
            subject="Subscription Activated",
            body=f"Your subscription to {plan_name} is now active from {start_date} to {end_date}.",
            from_email="noreply@yourdomain.com",
            to=[user_email],
        )
        message.attach_alternative(html_content, "text/html")
        message.send(fail_silently=False)
        logging.info(f"Subscription email sent to {user_email}")
    except Exception as e:
        logging.error(f"Error sending subscription email to {user_email}: {str(e)}")    
