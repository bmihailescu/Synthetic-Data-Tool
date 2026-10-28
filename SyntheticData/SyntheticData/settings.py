from socket import gethostname, gethostbyname 
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.abspath(os.path.join(__file__, '../..'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY','changeme')
HOSTNAME = os.environ.get('HOSTNAME')
# SECRET_KEY = '#)lr18%2+9wylu%7j-^9nks0-(_ry$%z!7s%3(kv+^d450o0k%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = bool(int(os.environ.get('DEBUG',0)))

ALLOWED_HOSTS = [
    "127.0.0.1", 
    "localhost", 
    gethostname(), 
    gethostbyname(gethostname()), 
    HOSTNAME,
    # Add production hosts
    "synthetic-data-tool.dseuk.io",
    # Add ECS/ALB internal hosts (more specific patterns)
    ".amazonaws.com",
    ".elb.amazonaws.com",
    ".compute.amazonaws.com",
    ".ec2.internal",
    # Add container internal hosts
    ".internal",
    ".local",
    # Add common ECS patterns
    "ip-*.eu-west-1.compute.internal",
    "*.eu-west-1.elb.amazonaws.com",
    "*.prod-powertools-applications.local",
]

# Remove None values from the list
ALLOWED_HOSTS = [host for host in ALLOWED_HOSTS if host is not None]

# Add wildcard for development/debugging (REMOVE IN PRODUCTION)
if DEBUG:
    ALLOWED_HOSTS.append('*')

ALLOWED_HOSTS_ENV = os.environ.get('ALLOWED_HOSTS')
if ALLOWED_HOSTS_ENV:
    ALLOWED_HOSTS.extend(ALLOWED_HOSTS_ENV.split(','))

print(f"DEBUG: ALLOWED_HOSTS = {ALLOWED_HOSTS}")  # Debug logging

# Trust headers from ALB/ELB
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
    # 'HdfsstatsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SyntheticData.urls'

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

WSGI_APPLICATION = 'SyntheticData.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR , 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'             # URL to use when referring to static files located in STATIC_ROOT.s
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
