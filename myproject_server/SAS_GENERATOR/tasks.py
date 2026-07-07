from .models import Movies,MovieUrls,PREMIUM_USER
import uuid
from celery import shared_task
from myproject_server.celery import app

import logging

@shared_task(name="db_update_task", queue ="db_update_queue")
def Update_Movie_URL(movie_id, url_,url_for_preview=None):
    try:
    
          # Generate a unique movie name using UUID
        objMovie = Movies.objects.get(Movie_id=movie_id)
        if objMovie:
            movie_url, created = MovieUrls.objects.get_or_create(Movie=objMovie)
            movie_url.blob_url = url_
            movie_url.url_for_preview = url_for_preview
            logging.info(f"{objMovie.title} URL updated to: {url_}")
            movie_url.save()
        
            logging.info(f"{objMovie.title} updated with URL: {url_}")
            try:
                app.send_task(
                name="email_notify_task",
                args=[objMovie.uploader_id, objMovie.title, objMovie.Movie_id],
                queue="email_notify_queue"
                )
            except  Exception as e:
                logging.error(f"Error sending  to email_notify_queue for video_id: {movie_id} --->Error: {str(e)}")
        else:
            logging.error(f"Movie with ID {movie_id} does not exist.")
            return  

        logging.info(f"Movie '{objMovie.title}' updated with URL: {url_}")
    except Exception as e:
        logging.error(f"Error updating movie URL: {str(e)}")
@shared_task(name="update_premium_user_task", queue="premium_user_update_queue")
def update_premium_user(user_id,user_email, plan_name,is_premium, start_date=None, end_date=None):
    try:
        user, created = PREMIUM_USER.objects.get_or_create(user_id=user_id)
        user.user_email = user_email
        user.is_premium = is_premium
        user.premium_start_date = start_date
        user.premium_end_date = end_date
        user.save()
        logging.info(f"Premium user {user_id} updated successfully.")

        app.send_task(
            name="subscription_task",
            args=[user_id, user_email,plan_name, start_date, end_date],
            queue="subscription_queue"
        )
    except Exception as e:
        logging.error(f"Error updating premium user {user_id}: {str(e)}")