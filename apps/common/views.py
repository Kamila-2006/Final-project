from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Page, Region, Setting
from .serializers import PagesListSerializer, PageDetailSerializer, RegionSerializer, CommonSettingsSerializer
from .pagination import CommonPagePagination, RegionDistrictPagination
from .utils.custom_response_decorator import custom_response


@custom_response
class CommonPagesView(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PagesListSerializer
    permission_classes = [AllowAny]
    pagination_class = CommonPagePagination


@custom_response
class PageDetailView(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


@custom_response
class RegionsDistrictsView(generics.ListAPIView):
    queryset = Region.objects.all().prefetch_related('districts')
    serializer_class = RegionSerializer
    pagination_class = RegionDistrictPagination


@custom_response
class CommonSettingsView(generics.ListAPIView):
    queryset = Setting.objects.all()
    serializer_class = CommonSettingsSerializer
