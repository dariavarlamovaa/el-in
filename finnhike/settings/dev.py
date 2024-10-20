from .base import *

SECRET_KEY = 'key'

DEBUG = True

ALLOWED_HOSTS = ["*"]

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
#     }
# }

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
