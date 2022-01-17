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
        'NAME': 'd6778krnp5ooid',
        'USER': 'yedofkcgxmxyxq',
        'PASSWORD': '2aa6181fb4e9db9b4d321ea0b624e727003a2097c23edcdfd9a8c8228007cfad',
        'HOST': 'ec2-54-247-96-153.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}

STATIC_ROOT = "static/"
