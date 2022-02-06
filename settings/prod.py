import os
from settings.base import *

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ["eduzec.herokuapp.com", "*"]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'df8js9ntl7ah3r',
        'USER': 'pewifymilfrmue',
        'PASSWORD': '6d03f47bf30d15dff496e7995b339318490bd59e5883d9ed17f203759ef32bb5',
        'HOST': 'ec2-52-51-155-48.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}

STATIC_ROOT = "static/"
