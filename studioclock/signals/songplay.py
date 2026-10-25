from django.db.models.signals import post_save
from django.dispatch import receiver

from studioclock.models import Song
from studioclock.services.now_playing import lookup_artwork


@receiver(post_save, sender=Song)
def obtain_artwork_url(sender, instance, created, **kwargs):
    if instance.artwork_url:
        return

    artwork_url = lookup_artwork(instance.artist, instance.title)

    if artwork_url:
        instance.artwork_url = artwork_url
        instance.save(update_fields=["artwork_url"])
