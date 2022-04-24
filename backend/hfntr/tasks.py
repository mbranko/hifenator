from datetime import timedelta
import logging
from django.conf import settings
from django.utils.timezone import now
from rest_framework.exceptions import NotFound
from .models import *
from .hyphenate import hyphenate_file

log = logging.getLogger(__name__)


def hyphenate_files(file_ids):
    for hf in HyphenatedFile.objects.filter(id__in=file_ids):
        if hf.status == 1:
            try:
                log.info(f'Converting file: {hf.orig_file.name}')
                hf.status = 2
                hf.save()
                src = settings.MEDIA_ROOT / hf.orig_file.name
                dest = settings.MEDIA_ROOT / hf.new_file.name
                hyphenate_file(src, dest)
                hf.status = 3
                hf.save()
                log.info(f'File: {hf.orig_file.name} done.')
            except Exception as ex:
                log.fatal(ex)
                hf.status = 4
                hf.save()
    delete_files_older_than_15_mins()


def delete_files_older_than_15_mins():
    old_files_cutoff = now() - timedelta(minutes=15)
    HyphenatedFile.objects.filter(timestamp__lt=old_files_cutoff).delete()
