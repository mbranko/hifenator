import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import HyphenatedFile


@receiver(post_delete, sender=HyphenatedFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    folder = None
    if instance.orig_file:
        if os.path.isfile(instance.orig_file.path):
            folder = os.path.dirname(instance.orig_file.path)
            os.remove(instance.orig_file.path)
    if instance.new_file:
        if os.path.isfile(instance.new_file.path):
            folder = os.path.dirname(instance.orig_file.path)
            os.remove(instance.new_file.path)
    if folder:
        os.rmdir(folder)
