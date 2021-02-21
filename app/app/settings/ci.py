from .base import *  # noqa: F403,F401
import os

DEBUG = True
ALLOWED_HOSTS = ['*']

SECRET_KEY = '2+o5#_zrzp7*6b#o(uiw@99%(*w!!^%tr#m@3&p+g+2=qx(2lv'
# DEBUG = False
# TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'PORT': '5432',
    }
}
