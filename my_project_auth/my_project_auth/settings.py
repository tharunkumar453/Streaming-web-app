from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definit

INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "auth_service",
]
AUTH_USER_MODEL = "auth_service.CustomUserModel"

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://esparx2k26.me",
]

CORS_ALLOW_CREDENTIALS = True


CSRF_TRUSTED_ORIGINS = [
    "https://esparx2k26.me",
    "http://localhost:3000",
]
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    "SIGNING_KEY": os.getenv("SIGNING_KEY"),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

ROOT_URLCONF = "my_project_auth.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "my_project_auth.wsgi.application"


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES_NAME= os.getenv("DATABASES_NAME")
DATABASES_USER= os.getenv("DATABASES_USER")
DATABASES_PASSWORD= os.getenv("DATABASES_PASSWORD")
PRIMARY_DATABASES_HOST= os.getenv("PRIMARY_DATABASES_HOST")
REPLICA1_DATABASES_HOST= os.getenv("REPLICA1_DATABASES_HOST")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": DATABASES_NAME,
        "USER": DATABASES_USER,
        "PASSWORD": DATABASES_PASSWORD,
        "HOST": PRIMARY_DATABASES_HOST,
        "PORT": "3306",
        "CONN_MAX_AGE": 600,
    },
    "replica": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": DATABASES_NAME,
        "USER": DATABASES_USER,
        "PASSWORD": DATABASES_PASSWORD,
        "HOST": REPLICA1_DATABASES_HOST,
        "PORT": "3306",
        "CONN_MAX_AGE": 600,
    },  
    
}
DATABASES_ROUTERS = ['my_project_auth.db_router.PrimaryReplicaRouter']

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = "static/"

CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL")





CELERY_ACCEPT_CONTENT = ["json"]

CELERY_TASK_SERIALIZER = "json"

CELERY_RESULT_SERIALIZER = "json"