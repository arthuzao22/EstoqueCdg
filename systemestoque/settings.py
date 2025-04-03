from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-essns=lr^jj^!!2w$&l12h5n*ec=!=3^o#^2h(ko^xdqwrug*b'

DEBUG = True 

#ALLOWED_HOSTS = ['.onrender.com', 'estoquecdg.onrender.com', 'localhost']
ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'empresa',
    'categoria',
    'formato',
    'produto',
    'movimentacoes',
    'usuarios',
    'home',
    'kanban',
]

LOGIN_URL = '/usuarios/login/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'systemestoque.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'systemestoque.wsgi.application'

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'estoquecdg',  # Nome do banco de dados
#        'USER': 'arthuzao',  # Usuário
#        'PASSWORD': '2CT.qtr@3FzUYU9',  # Senha
#        'HOST': 'mysql.uhserver.com',  # Hostname do servidor
#        'PORT': '3306',  # Porta do MySQL
#        'CONN_MAX_AGE': 600,  # Conexão persistente por 10 minutos
#        'OPTIONS': {
#            'ssl': {'ssl_disabled': True},
#        },
#    }
#}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'estoqueCdg',
        'USER': '3tmkk7',
        'PASSWORD': 'xau_6HBaJHK1YIIHXNseXdYoon1COlk8GGqv1',  # Pegando do .env
        'HOST': 'us-east-1.sql.xata.sh',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': str(BASE_DIR / 'db.sqlite3'),  # Convert Path to string
#    }
#}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = False

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

