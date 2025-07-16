from .base import *

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
