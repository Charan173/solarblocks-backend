import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        'One-off fix: ensures an admin account exists with is_staff/is_superuser/'
        'is_active set correctly, and resets its password. Safe to run multiple '
        'times (idempotent) — reads credentials from env vars if set, otherwise '
        'falls back to the defaults below.'
    )

    def handle(self, *args, **options):
        User = get_user_model()
        email = os.environ.get('ADMIN_FIX_EMAIL', 'admin@solarblocks.com')
        password = os.environ.get('ADMIN_FIX_PASSWORD', 'Admin@123')

        user, created = User.objects.get_or_create(
            email=email,
            defaults={'name': 'Admin'},
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created superuser {email}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Fixed existing account {email}'))