import logging
from django.core.files.base import ContentFile
from django_q.tasks import async_task
from rest_framework.decorators import api_view, parser_classes
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import HyphenatedFile
from .serializers import HyphenatedFileSerializer
from .tasks import hyphenate_files

log = logging.getLogger(__name__)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def upload_file(request):
    file_ids = []
    for item in request.FILES:
        file = request.FILES[item]
        hf = HyphenatedFile.objects.create(status=1)
        hf.orig_file = file
        hf.save()
        orig_name = hf.filename_orig()
        last_dot_pos = orig_name.rfind('.')
        if last_dot_pos == -1:
            new_name = orig_name + '-hf.docx'
        else:
            new_name = orig_name[:last_dot_pos] + '-hf' + orig_name[last_dot_pos:]
        print(new_name)
        hf.new_file.save(new_name, ContentFile(''))
        hf.save()
        log.info(f'Added file: {hf.filename_orig()} -> {hf.filename_new()}')
        file_ids.append(hf.id)
    async_task(hyphenate_files, file_ids)
    return Response(file_ids, status=HTTP_201_CREATED)


@api_view(['GET'])
def file_status(request, file_id):
    try:
        hf = HyphenatedFile.objects.get(id=file_id)
        return Response(hf.status, status=HTTP_200_OK)
    except HyphenatedFile.DoesNotExist:
        raise NotFound(detail='File not found')


@api_view(['GET'])
def download_file_url(request, file_id):
    try:
        hf = HyphenatedFile.objects.get(id=file_id)
        return Response(hf.new_file.url, status=HTTP_200_OK)
    except HyphenatedFile.DoesNotExist:
        raise NotFound(detail='File not found')


class HyphenatedFileList(generics.ListAPIView):
    queryset = HyphenatedFile.objects.all()
    serializer_class = HyphenatedFileSerializer
    filterset_fields = {'id': ['exact', 'in']}


class HyphenatedFileDetail(generics.RetrieveAPIView):
    queryset = HyphenatedFile.objects.all()
    serializer_class = HyphenatedFileSerializer


