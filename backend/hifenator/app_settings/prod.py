from asyncore import read
from .base import *
from .utils import read_or_get

DEBUG = False
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://*.hifenator.rs']
SECRET_KEY = read_or_get('/private/secrets', 'SECRET_KEY', '123456789012345678901234567890123456789')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.uns.ac.rs'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = read_or_get('/private/secrets', 'EMAIL_HOST_USER', '******')
EMAIL_HOST_PASSWORD = read_or_get('/private/secrets', 'EMAIL_HOST_PASSWORD', '**********')
ADMINS = eval(read_or_get('/private/secrets', 'ADMINS', '[]'))
