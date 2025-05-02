import os

from typing import Union, Any
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.urls import reverse
from django.utils import timezone
from django.template.defaultfilters import slugify



import phonenumbers


class PaginatorPage(object):
    def __init__(self,
                 queryset: QuerySet,
                 page_number: int = 1,
                 limit: int = 20,
                 params: dict = {},
                 url: str = '') -> None:
        paginator = Paginator(queryset, limit)  # Show limit contacts per page.
        page_obj = paginator.get_page(page_number)
        paramsCopy = params.copy()
        _ = paramsCopy.pop('page', True)
        self.url_query = paramsCopy.urlencode()

        # couting page number for views
        limitPage = 2
        maxPage = paginator.num_pages + 1
        startPage = page_number - limitPage if page_number - limitPage > 0 else 1
        endPage = page_number + limitPage + 1 if page_number + limitPage + 1 < maxPage else maxPage
        pageNumberList = []
        for pageNumber in range(startPage, endPage):
             pageNumberList.append({ "pageNumber": pageNumber, "url": f'{reverse(url)}?page={pageNumber}&{self.url_query}' })
        
        self.objects = page_obj.object_list
        self.page_number = page_number
        self.pageNumberList = pageNumberList
        self.next = page_obj.next_page_number() if page_obj.has_next() else None
        self.previous = page_obj.previous_page_number() if page_obj.has_previous() else None
        self.previous_url = f'{reverse(url)}?page={self.previous}&{self.url_query}'
        self.next_url = f'{reverse(url)}?page={self.next}&{self.url_query}'


class FilenameForPathGenerator(object):
    """
    Utility class to handle generation of file name upload path
    """

    def __init__(self, prefix: str) -> None:
        self.prefix = prefix

    def __call__(self, instance: Any, filename: str) -> str:
        today = timezone.localtime(timezone.now()).date()

        filepath = os.path.basename(f'{filename}')
        filename, extension = os.path.splitext(filepath)
        filename = slugify(filename)

        path = "/".join([
            self.prefix,
            str(today.year),
            str(today.month),
            str(today.day),
            filename + extension
        ])
        return path

try:
    from django.utils.deconstruct import deconstructible
    FilenameForPathGenerator = deconstructible(FilenameForPathGenerator)  # type: ignore
except ImportError:
    pass


def normalize_phone(number: str) -> str:
    if number.startswith('0'):
        number = number[1:]
    elif number.startswith('62'):
        number = '+' + number
    parse_phone_number = phonenumbers.parse(number, settings.COUNTRY)
    phone_number = phonenumbers.format_number(
        parse_phone_number, phonenumbers.PhoneNumberFormat.E164)
    return phone_number
