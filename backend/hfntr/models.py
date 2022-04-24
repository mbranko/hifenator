import os
from django.db import models


PROCESS_STATUSES = [
    (0, 'непознат'),
    (1, 'нов'),
    (2, 'у обради'),
    (3, 'завршен'),
    (4, 'грешка')
]


def get_upload_path(instance, filename):
    return os.path.join(f'uploads/file-{instance.id}', filename)


class HyphenatedFile(models.Model):
    orig_file = models.FileField('original file', upload_to=get_upload_path)
    new_file = models.FileField('hyphenated file', upload_to=get_upload_path)
    status = models.IntegerField(choices=PROCESS_STATUSES, default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.orig_file.url

    def filename_orig(self):
        return os.path.basename(self.orig_file.name)

    def filename_new(self):
        return os.path.basename(self.new_file.name)

    def filepath_orig(self):
        return self.orig_file.path

    def filepath_new(self):
        return self.new_file.path if self.new_file else None

    def url_orig(self):
        return self.orig_file.url

    def url_new(self):
        return self.new_file.url if self.new_file else None

    def status_text(self):
        return PROCESS_STATUSES[self.status][1]

    class Meta:
        verbose_name = 'hyphenated file'
        verbose_name_plural = 'hyphenated files'
