from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10


class CategoryPagination(CustomLimitOffsetPagination):
    pass


class FavouriteProductPagination(PageNumberPagination):
    pass


class MyAdsListPagination(PageNumberPagination):
    pass
