from pathlib import Path
import environ

env = environ.Env(
    DEBUG=(bool, False)  
)
environ.Env.read_env()

# Base Directories
BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = "accounts.CustomUser"
# CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',  # React default port = 3000
    'http://localhost:8000',  # Django default port = 8000
)

SECRET_KEY = env("SECRET_KEY", default='django-insecure-2fbi2x-cisq#-@4@uxn51-j1mwr#6@r3+wppa4-1xf%@1mj9z2')
DEBUG = env("DEBUG", default=True)

ALLOWED_HOSTS = ["*"]
LOGIN_URL = "http://localhost:5173/signin"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    "corsheaders",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth.registration",
    "accounts.apps.AccountsConfig",
    "cart.apps.CartConfig",
    "order.apps.OrderConfig",
    "flower.apps.FlowerConfig",
    "category.apps.CategoryConfig",
    'django_rest_passwordreset',
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'FlowerHaven.urls'
PASSWORD_RESET_TIMEOUT = 3600

ACCOUNT_EMAIL_VERIFICATION = 'optional'  # optional, or 'mandatory' if you prefer

CSRF_COOKIE_SECURE = False 
CSRF_TRUSTED_ORIGINS = ["http://localhost:5173"]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = 'FlowerHaven.wsgi.application'

# Email Backend Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_USE_TLS = True
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

# ssl commerce payment gateway
SSLCOMMERZ_STORE_ID = "flowe675ea7ca09c98"
SSLCOMMERZ_STORE_PASS = "flowe675ea7ca09c98@ssl"


SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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
CORS_ALLOW_ALL_ORIGINS = True 
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
