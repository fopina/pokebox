STATIC_ROOT = '/var/app/static_temp'
SCANS_NMAP_COMMAND = ['nmap']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/var/dbdata/db.sqlite3',
    }
}