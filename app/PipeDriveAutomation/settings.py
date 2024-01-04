from pathlib import Path
import os
from dotenv import load_dotenv
from .utils import get_secret_dict
load_dotenv()

ENVIRONMENT = 'dev'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SESSION_COOKIE_SECURE = True
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
# CORS_ORIGIN_ALLOW_ALL = True


if ENVIRONMENT == 'local':

    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    FIELD_ENCRYPTION_KEY = 'u15DQDG0wd6tQBrhGiimvk1YFUxqPrk_ufwXIoeA6lg='
    ALLOWED_HOSTS = ['*']

else:
    django_secrets = get_secret_dict(f'{ENVIRONMENT}/django_secrets')
    DEBUG = django_secrets['DEBUG']
    SECRET_KEY = django_secrets['SECRET_KEY']
    FIELD_ENCRYPTION_KEY = django_secrets['FIELD_ENCRYPTION_KEY']
    ALLOWED_HOSTS = []
    ALLOWED_HOSTS.extend([host.strip() for host in django_secrets['ALLOWED_HOSTS'].split(',')])


SHARED_APPS = [
    'django_tenants',  # mandatory
    'corsheaders',
    'user_management',
    'django_celery_results',
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
    'apps.integrations'
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

if ENVIRONMENT == 'local':

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


else:
    secret_db_name = f'{ENVIRONMENT}/db/masteruser'
    db_secrets = get_secret_dict(secret_db_name)
    DATABASES = {
        'default': {
            'ENGINE': 'django_tenants.postgresql_backend',
            'NAME': db_secrets['DB_NAME'],
            'USER': db_secrets['DB_USER'],
            'PASSWORD': db_secrets['DB_PASSWORD'],
            'HOST': db_secrets['DB_HOST'],
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

# settings.py
if ENVIRONMENT == 'local':

    PIPEDRIVE_OAUTH_SETTINGS = {
        'client_id': os.getenv('PIPEDRIVE_CLIENT_ID'),
        'client_secret': os.getenv('PIPEDRIVE_CLIENT_SECRET'),
        'redirect_uri': os.getenv('PIPEDRIVE_REDIRECT_URI'),
        'authorization_url': 'https://oauth.pipedrive.com/oauth/authorize',
        'token_url': 'https://oauth.pipedrive.com/oauth/token',
    }

    ASANA_OAUTH_SETTINGS = {
        'client_id': os.getenv('ASANA_CLIENT_ID'),
        'client_secret': os.getenv('ASANA_CLIENT_SECRET'),
        'redirect_uri': os.getenv('ASANA_REDIRECT_URI'),
        'authorization_url': 'https://app.asana.com/-/oauth_authorize',
        'token_url': 'https://app.asana.com/-/oauth_token',
    }

    # CORS_ALLOWED_ORIGINS = [
    #             "https://0933-98-24-161-221.ngrok-free.app"
    #         ]
    CSRF_TRUSTED_ORIGINS = ["https://7b40-2603-8000-b640-5420-a0d6-5bc1-cd3d-61f0.ngrok-free.app"]

    CELERY_BROKER_URL = 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

else:
    pipedrive_secrets = get_secret_dict(f'{ENVIRONMENT}/pipedrive_secrets')
    PIPEDRIVE_OAUTH_SETTINGS = {
        'client_id': pipedrive_secrets['PIPEDRIVE_CLIENT_ID'],
        'client_secret': pipedrive_secrets['PIPEDRIVE_CLIENT_SECRET'],
        'redirect_uri': pipedrive_secrets['PIPEDRIVE_REDIRECT_URI'],
        'authorization_url': 'https://oauth.pipedrive.com/oauth/authorize',
        'token_url': 'https://oauth.pipedrive.com/oauth/token',
    }

    EC2_SECRETS = get_secret_dict(f'{ENVIRONMENT}/celery_secrets')
    CELERY_BROKER_URL = f"redis://{EC2_SECRETS['HOST_NAME']}:6379/0"
    CELERY_RESULT_BACKEND = f"redis://{EC2_SECRETS['HOST_NAME']}:6379/0"


# Celery Configuration Options
CELERY_TIMEZONE = 'America/New_York'
CELERY_TASK_TIME_LIMIT = 30 * 60
TIME_ZONE = 'America/New_York'
