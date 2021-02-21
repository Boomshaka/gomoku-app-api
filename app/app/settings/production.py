from .base import *  # noqa: F403,F401
import os
import dj_database_url


DEBUG = True
# ALLOWED_HOSTS = ['gomoku-api.herokuapp.com']
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}
