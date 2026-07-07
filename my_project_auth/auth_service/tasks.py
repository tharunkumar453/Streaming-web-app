
from my_project_auth.celery import app
class EmailNotificationTask:
    def send_email_notification(self,email):
        try:
            app.send_task(
                name='Registrationtask',
                args=[email],
                queue='RegistrationQueue',

            )
        except Exception as e:
            print(f"Error sending email to  notification: {e}")