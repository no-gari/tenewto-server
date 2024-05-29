from rest_framework.pagination import PageNumberPagination
from django.utils.deconstruct import deconstructible
import datetime
import uuid
import os


@deconstructible
class FilenameChanger(object):
    def __init__(self, base_path):
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.base_path = f'{base_path}/{str(date)}'

    def __call__(self, instance, filename, *args, **kwargs):
        ext = filename.split('.')[-1].lower()
        filename = f'{uuid.uuid4()}.{ext}'
        path = os.path.join(self.base_path, filename)
        return path

    def __eq__(self, other):
        return self.base_path


class StandardResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 10
    page_size = 10
