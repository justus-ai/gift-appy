import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from profiles.models import Item, UserProfile


class Command(BaseCommand):
    help = 'Re-uploads local media files to Cloudinary and updates DB records'

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT

        # Upload Item images
        items = Item.objects.exclude(image='').exclude(image=None)
        self.stdout.write(f'Found {items.count()} wish items with images')
        for item in items:
            local_path = os.path.join(media_root, str(item.image))
            if os.path.isfile(local_path):
                with open(local_path, 'rb') as f:
                    filename = os.path.basename(local_path)
                    item.image.save(filename, File(f), save=True)
                    self.stdout.write(self.style.SUCCESS(f'  Uploaded item #{item.id}: {filename}'))
            else:
                self.stdout.write(self.style.WARNING(f'  Skipped item #{item.id}: file not found at {local_path}'))

        # Upload UserProfile images
        profiles = UserProfile.objects.exclude(image='').exclude(image=None)
        self.stdout.write(f'Found {profiles.count()} user profiles with images')
        for profile in profiles:
            local_path = os.path.join(media_root, str(profile.image))
            if os.path.isfile(local_path):
                with open(local_path, 'rb') as f:
                    filename = os.path.basename(local_path)
                    profile.image.save(filename, File(f), save=True)
                    self.stdout.write(self.style.SUCCESS(f'  Uploaded profile: {profile.user.username} - {filename}'))
            else:
                self.stdout.write(self.style.WARNING(f'  Skipped profile: {profile.user.username}: file not found at {local_path}'))

        self.stdout.write(self.style.SUCCESS('Done!'))
