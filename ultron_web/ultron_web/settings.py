"""
Django settings for ultron_web project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import sys
from pathlib import Path

from decouple import config
from celery.schedules import crontab


MULTISTAGE = config("MULTISTAGE", default="PROD")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Include apps dir in sys.path
APPS_DIR = os.path.normpath(os.path.join(BASE_DIR, '.', 'apps'))
sys.path.insert(0,  APPS_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if MULTISTAGE == "PROD" or MULTISTAGE == "STAG" else True

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=lambda v: {s.replace('*.','.') for s in v.split(" ")})


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # third-aprty libraries
    'django_extensions',
    'django_celery_beat',
    'rest_framework',
    'rest_framework.authtoken',
    'django_elasticsearch_dsl',

    # local apps
    'recortes.apps.RecortesConfig',
    'config.apps.ConfigConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ultron_web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ultron_web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(os.path.join(BASE_DIR, "db.sqlite3")),
    },
    'ultron': {
        "ENGINE": config("ULTRON_DB_ENGINE"),
        "NAME": config("ULTRON_DB_NAME"),
        "USER": config("ULTRON_DB_USER"),
        "PASSWORD": config("ULTRON_DB_PASSWORD"),
        "HOST": config("ULTRON_DB_HOST"),
        "PORT": config("ULTRON_DB_PORT"),
    }
}

DATABASE_APPS_MAPPING = {
    'recortes': 'ultron',
    'config': 'default',
}

DATABASE_ROUTERS = ['ultron_web.database_router.DatabaseAppRouter',]

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# Celery settings
CELERY_BROKER_URL = "amqp://{user}:{passw}@rabbitmq:5672/".format(
    user=config('RABBITMQ_USERNAME'),
    passw=config('RABBITMQ_PASSWORD')
)
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

CELERY_BEAT_SCHEDULE = {
    'get_recortes_from_db_task': {
        'task': 'recortes.tasks.get_recortes_from_db_task',
        'schedule': 20,
        #'args': (3,)
    },
}

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': "elasticsearch:{port}".format(port=config('ELASTICSEARCH_PORT'))
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'entities.authentication.UltronAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

TOKEN_EXPIRED_TIME = config('TOKEN_EXPIRED_TIME', default=60, cast=int)
