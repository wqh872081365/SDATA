"""
Django settings for SDATA project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pkdj^62xu+mckgc&#w=$&g$f_dug+lo3_eoa57!-5)8_650o(-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_rq",
    'app.video',
    'app.logs',
    'app.proxy',
    'app.utils',
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

ROOT_URLCONF = 'SDATA.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'SDATA.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "zh-Hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

SPIDER_TIMEOUT = 10

USER_ID = 1

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 2,
        'DEFAULT_TIMEOUT': 360,
    },
    'high': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 2,
        'DEFAULT_TIMEOUT': 86400,
    },
    'low': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 2,
        'DEFAULT_TIMEOUT': 60,
    },

    'add_spider': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 2,
        'DEFAULT_TIMEOUT': 86400,
    },
    'spider_pipeline': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 2,
        'DEFAULT_TIMEOUT': 360,
    },

    # scheduler
    'scheduler': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 2,
        'DEFAULT_TIMEOUT': 86400,
    },

    'spider_status': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 2,
        'DEFAULT_TIMEOUT': 86400,
    },
    'rq_worker_number_control': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 2,
        'DEFAULT_TIMEOUT': 360,
    },
    'proxy_valid': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 2,
        'DEFAULT_TIMEOUT': 86400,
    },
}

RQ_SHOW_ADMIN_LINK = True

try:
    from SDATA.local_settings import *
except ImportError as e:
    pass