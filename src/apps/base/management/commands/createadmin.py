import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()
lg = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'This command creates superuser'

    def handle(self, *_, **__) -> None:
        if not User.objects.exists():
            user = User.objects.create_superuser(
                username=settings.DEFAULT_ADMIN_NAME,
                email=settings.DEFAULT_ADMIN_EMAIL,
                password=settings.DEFAULT_ADMIN_PASSWORD,
            )
            lg.debug(f'Admin {user.username} was created.')
