from rest_framework import serializers
from .models import *


class HyphenatedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = HyphenatedFile
        fields = ('id', 'status', 'timestamp', 'filename_orig', 'filename_new', 'url_orig', 'url_new', 'status_text')
