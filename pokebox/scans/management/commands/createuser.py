from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model
import string
import random


class Command(BaseCommand):
    help = 'Create user with random password'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username', '-u',
            action='store',
            dest='username',
            default='admin',
            help='Choose username (default: admin)',
        )

        parser.add_argument(
            '--password', '-p',
            action='store',
            dest='password',
            help='Choose password, but not recommended. Leave empty to generate random and then change in profile',
        )

    def handle(self, *args, **options):
        u, created = get_user_model().objects.get_or_create(username=options['username'])
        u.is_staff = u.is_superuser = True
        pwd = options['password']
        if not pwd:
            pwd = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(20))
        u.set_password(pwd)
        u.save()

        self.stdout.write(
            '%s user %s with random password: %s' % (
                'Created' if created else 'Updated',
                options['username'],
                pwd,
            )
        )
