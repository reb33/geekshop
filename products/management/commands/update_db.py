from django.core.management import BaseCommand

from authapp.models import ShopUser, UserProfile


class Command(BaseCommand):

    def handle(self, *args, **options):
        users = ShopUser.objects.exclude(pk__in=(user_prof.user_id for user_prof in UserProfile.objects.all()))
        for user in users:
            UserProfile.objects.create(user=user)
