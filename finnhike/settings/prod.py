from .base import *

SECRET_KEY = os.getenv("SECRET_KEY_APP")

DEBUG = bool(int(os.getenv("DEBUG")))

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

DATABASES = {
    'default': {
        'ENGINE': f'{os.getenv("POSTGRES_ENGINE")}',
        'NAME': f'{os.getenv("POSTGRES_NAME")}',
        'USER': f'{os.getenv("POSTGRES_USER")}',
        'PASSWORD': f'{os.getenv("POSTGRES_PASSWORD")}',
        'PORT': f'{os.getenv("POSTGRES_PORT")}',
        'HOST': f'{os.getenv("POSTGRES_HOST")}',
    }
}

CSRF_TRUSTED_ORIGINS = ['https://finnhike.com', 'https://127.0.0.1']