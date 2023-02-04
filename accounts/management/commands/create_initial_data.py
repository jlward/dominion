from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from players.models import Player


class Command(BaseCommand):
    help = 'Create the initial stuff needed to make the app work'

    def create_user(self, email, handle):
        is_superuser = False
        is_staff = False
        if handle is None:
            is_superuser = True
            is_staff = True

        User = get_user_model()
        user = User.objects.create(
            email=email,
            is_superuser=is_superuser,
            is_staff=is_staff,
        )
        user.set_password('pw')
        user.save()
        if handle:
            Player.objects.create(
                handle=handle,
                user=user,
            )

    def handle(self, *args, **options):
        User = get_user_model()
        users = [
            ['staff@playdominion.com', None],
            ['jason.louard.ward@gmail.com', 'Ward'],
            ['derekjamerson@gmail.com', 'Probably D'],
        ]
        for email, handle in users:
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                self.create_user(email=email, handle=handle)
