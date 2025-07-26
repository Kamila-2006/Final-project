from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10


class CommonPagePagination(CustomLimitOffsetPagination):
    pass


class RegionDistrictPagination(CustomLimitOffsetPagination):
    pass