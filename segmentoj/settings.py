"""
Django settings for segmentoj project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
    'sx!y=avrq(g1o+-7o2ef_4e*slekh5vtd-+6rs&c-nbfzw0*b^'  # CHANGE HERE ON PRODUCTION
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # CHANGE HERE TO 'False' ON PRODUCTION

ALLOWED_HOSTS = ['*']  # CHANGE HERE ON PRODUCTION

# Application definition

# DON'T CHANGE THIS unless you know what you are doing!
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # CORS
    'corsheaders',

    # API Framework
    'rest_framework',

    # SegmentOJ Apps
    'account',
    'problem',
    'status',
    'captcha',
    'judger',  # Judger API
]

MIDDLEWARE = [
    'segmentoj.middleware.DisableCSRFCheck',  # Disable CSRF check
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'segmentoj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/template'],
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

WSGI_APPLICATION = 'segmentoj.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# CHANGE HERE if want to change to MySQL or other Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

AUTH_USER_MODEL = 'account.Account'


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

# Time Zone, CHANGE HERE
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'  # DON'T CHANGE THIS
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Session ID
# SESSION_SAVE_EVERY_REQUEST = False
# SESSION_COOKIE_AGE = 1209600

# User uploads file placses
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads').replace('\\', '/')
MEDIA_URL = '/media/'  # DON'T CHANGE THIS

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',  # use throttle_scope = 'xxx'
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 1,
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get('BACKEND_EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('BACKEND_EMAIL_PORT')) if os.environ.get('BACKEND_EMAIL_PORT') else 25
EMAIL_HOST_USER = os.environ.get('BACKEND_EMAIL_USERNAME')
EMAIL_HOST_PASSWORD = os.environ.get('BACKEND_EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

VERIFY_EMAIL_TEMPLATE_TITLE = '[SegmentOJ] Email Verify'
VERIFY_EMAIL_TEMPLATE_CONTENT = """Hi, {username}<br/>
It seems that you have just requested an email verify!<br/>
<strong>Your code is:</strong> <code>{signature}</code><br/>
Please use it in 20 minutes.<br/>
"""
VERIFY_EMAIL_MAX_AGE = 20

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=3)
}

# CORS
CORS_ORIGIN_ALLOW_ALL = True

# Judger Port Connection
JUDGER_PORT = {
    # This base url for server to connect judger port.
    'base_url': 'http://127.0.0.1:3000',
    
    # Uncomment this if you wants to use password auth too.
    # This is suggested in production environment.
    # Note: you need to config the judger ports too.
    # 'password': 'your password',
}

# Captcha Configuration
CAPTCHA = {
    # The height of each captcha pic
    'picture_height': 26,

    # The width of each captcha pic
    'picture_width': 78,

    # The number of chars in each captcha pic
    'length': 4,

    # font size on captcha
    # you may change this if modified height/width
    # try it until you find the best value
    'font_size': 16,

    # the font file of font
    'font_family': os.path.join(BASE_DIR, 'captcha', 'FiraCode-Regular.ttf'),

    # The number of dots on the pic to interfare
    'dot_number': 100,

    # The number of lines on the pic to interfare
    'line_number': 2,

    # how long a captcha expire (minutes)
    'age': 5,
}