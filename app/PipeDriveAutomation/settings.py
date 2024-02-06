from pathlib import Path
import os
from dotenv import load_dotenv
from .utils import get_secret_dict
load_dotenv()

ENVIRONMENT = 'local'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SESSION_COOKIE_SECURE = False
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
# CORS_ORIGIN_ALLOW_ALL = True
SECRET_KEY = os.getenv('SECRET_KEY')

if ENVIRONMENT == 'local':
    DEBUG = True
    DOMAIN = 'https://42c9-2603-6081-1703-485c-c86d-93b3-2750-dac9.ngrok-free.app'
    FIELD_ENCRYPTION_KEY = 'u15DQDG0wd6tQBrhGiimvk1YFUxqPrk_ufwXIoeA6lg='
    ALLOWED_HOSTS = ['*']

else:
    DOMAIN = os.getenv('DOMAIN')
    ALLOWED_HOSTS = [DOMAIN]
    FIELD_ENCRYPTION_KEY = os.getenv('FIELD_ENCRYPTION_KEY')


SHARED_APPS = [
    'django_tenants',  # mandatory
    'corsheaders',
    'user_management',
    'django_celery_results',
    'tenant_schemas_celery',
    'encrypted_model_fields',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

]

TENANT_APPS = [
    'apps.pipedrive',
    'apps.core',
    'apps.google_drive',
]

INSTALLED_APPS = list(set(SHARED_APPS + TENANT_APPS))

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'PipeDriveAutomation.middleware.TenantMiddleware.CustomTenantMainMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PipeDriveAutomation.urls'

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

WSGI_APPLICATION = 'PipeDriveAutomation.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': '5432',
    }
}


DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

TENANT_DB_ALIAS = 'default'

TENANT_MODEL = "user_management.Company"

TENANT_DOMAIN_MODEL = "user_management.Domain"

# AUTH_USER_MODEL = 'user_management.CustomUser'

# LOG_ENTRY_MODEL = 'user_management.CustomUser'


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/static/'
MEDIA_URL = '/static/media/'

STATIC_ROOT = '/vol/web/static'
MEDIA_ROOT = '/vol/web/media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PIPEDRIVE_OAUTH_SETTINGS = {
    'client_id': os.getenv('PIPEDRIVE_CLIENT_ID'),
    'client_secret': os.getenv('PIPEDRIVE_CLIENT_SECRET'),
    'redirect_uri': f'{DOMAIN}/core/callback/',
    'authorization_url': 'https://oauth.pipedrive.com/oauth/authorize',
    'token_url': 'https://oauth.pipedrive.com/oauth/token',
}

GOOGLE_DRIVE_OAUTH_SETTINGS = {
    'client_id': os.getenv('GOOGLE_DRIVE_CLIENT_ID'),
    'client_secret': os.getenv('GOOGLE_DRIVE_CLIENT_SECRET'),
    'redirect_uri': f'{DOMAIN}/core/callback/',
    'authorization_url': 'https://accounts.google.com/o/oauth2/v2/auth?prompt=consent&access_type=offline',
    'token_url': 'https://oauth2.googleapis.com/token',
}

CSRF_TRUSTED_ORIGINS = [DOMAIN]
# settings.py
if ENVIRONMENT == 'local':

    BROKER_URL = 'redis://redis:6379/0'
    CELERY_BROKER_URL = 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

else:
    REDIS_HOST=os.getenv('REDIS_HOST_NAME')
    CELERY_BROKER_URL = f"redis://{REDIS_HOST}:6379/0"
    CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:6379/0"
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP=True


# Celery Configuration Options
CELERY_TIMEZONE = 'America/New_York'
CELERY_TASK_TIME_LIMIT = 30 * 60
TIMEZONE = 'America/New_York'