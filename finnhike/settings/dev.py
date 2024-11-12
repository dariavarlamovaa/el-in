from .base import *

SECRET_KEY = 'key'

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': f'{os.getenv("POSTGRES_ENGINE")}',
        'NAME': f'{os.getenv("POSTGRES_NAME_DEV")}',
        'USER': f'{os.getenv("POSTGRES_USER_DEV")}',
        'PASSWORD': f'{os.getenv("POSTGRES_PASSWORD_DEV")}',
        'PORT': f'{os.getenv("POSTGRES_PORT_DEV")}',
        'HOST': f'{os.getenv("POSTGRES_HOST_DEV")}',
    }
}