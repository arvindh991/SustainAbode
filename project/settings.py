import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else ['sustainabodeau-e2c9bec8e3hre8f0.australiasoutheast-01.azurewebsites.net', 'sustainabode.xyz', '127.0.0.1', 'http://20.70.176.88/']

CSRF_TRUSTED_ORIGINS = ['https://sustainabodeau-e2c9bec8e3hre8f0.australiasoutheast-01.azurewebsites.net', 'https://sustainabode.xyz', 'http://20.70.176.88/']

# Application definition

INSTALLED_APPS = [
    # my_apps
    'sustainScoreMap',
    'compareSuburbsMap',
    'lockdown',

    # default_apps
    "whitenoise.runserver_nostatic",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Use Azure Blob Storage for media files
DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'

# Azure Storage settings
# Storage account name
AZURE_ACCOUNT_NAME = os.getenv('AZURE_STORAGE_NAME')

# Storage account URL
AZURE_ACCOUNT_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net"

# Access key for the storage account
AZURE_ACCOUNT_KEY = os.getenv('AZURE_STORAGE_KEY')

# Container name
AZURE_CONTAINER = os.getenv('AZURE_STORAGE_CONTAINER')

# Custom domain for media
AZURE_CONTAINER_URL = f"{AZURE_ACCOUNT_URL}/{AZURE_CONTAINER}"  

# Fetch the Mapbox API key from environment variables
MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY')

# Enables lockdown globally
LOCKDOWN_ENABLED = True  

# Passwords that will allow access
LOCKDOWN_PASSWORDS = (os.getenv('LOCKDOWN_PASSWORD'),)

# The default form for password authentication
LOCKDOWN_FORM = 'lockdown.forms.LockdownForm'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Add whitenoise middleware after the security middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'lockdown.middleware.LockdownMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.media',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATICFILES_DIRS = (str(BASE_DIR.joinpath('static')),)
STATIC_URL = 'static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Media files (geoJSON)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# SECURITY SETTING
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = 'DENY'
# SECURE_HSTS_SECONDS = 31536000  # Enable HTTP Strict Transport Security (HSTS)
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
