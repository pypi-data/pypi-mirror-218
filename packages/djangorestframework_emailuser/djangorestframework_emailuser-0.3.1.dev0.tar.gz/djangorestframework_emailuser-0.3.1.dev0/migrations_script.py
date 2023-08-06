import django
from django.conf import settings
from django.core.management import call_command

settings.configure(
    DEBUG=True,
    INSTALLED_APPS = [
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'emailuser'
    ]
)
if __name__ == '__main__':
    django.setup()
    call_command('makemigrations', 'emailuser')