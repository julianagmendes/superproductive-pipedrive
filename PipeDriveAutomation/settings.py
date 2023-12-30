from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = 'local'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SESSION_COOKIE_SECURE = True
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
# CORS_ORIGIN_ALLOW_ALL = True
# SECURITY WARNING: don't run with debug turned on in production!
if ENVIRONMENT == 'local':

    DEBUG = os.getenv('DEBUG')
    SECRET_KEY = os.getenv('SECRET_KEY')
    FIELD_ENCRYPTION_KEY = 'u15DQDG0wd6tQBrhGiimvk1YFUxqPrk_ufwXIoeA6lg='

else:
    DEBUG = False

    #TODO: Add production settings to get parameters from Parameter store

ALLOWED_HOSTS = ['*']


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
    pass
    #TODO: Add production settings to get parameters from Parameter store

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

TENANT_DB_ALIAS = 'default'

TENANT_MODEL = "user_management.Company"

TENANT_DOMAIN_MODEL = "user_management.Domain"

AUTH_USER_MODEL = 'user_management.CustomUser'

LOG_ENTRY_MODEL = 'user_management.CustomUser'


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

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py
if ENVIRONMENT == 'local':

    PIPEDRIVE_OAUTH_SETTINGS = {
        'client_id': os.getenv('PIPEDRIVE_CLIENT_ID'),
        'client_secret': os.getenv('PIPEDRIVE_CLIENT_SECRET'),
        # 'redirect_uri': os.getenv('PIPEDRIVE_REDIRECT_URI'),  
        'redirect_uri': 'https://0933-98-24-161-221.ngrok-free.app/core/callback/',  # TODO: Change this to the actual redirect URI
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
    # CSRF_TRUSTED_ORIGINS = ["https://0933-98-24-161-221.ngrok-free.app"]

    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

else:
    pass

    #TODO: Add production settings to get parameters from Parameter store

# Celery Configuration Options
CELERY_TIMEZONE = 'America/New_York'
CELERY_TASK_TIME_LIMIT = 30 * 60
TIME_ZONE = 'America/New_York'
