from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from .models import Page, Region, Setting
from .openapi_schema import (
    page_detail_response,
    page_list_response,
    regions_with_districts_response,
    setting_response,
)
from .serializers import (
    CommonSettingsSerializer,
    PageDetailSerializer,
    PageListSerializer,
    RegionSerializer,
)
from .utils.custom_response_decorator import custom_response


@custom_response
class CommonPagesView(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageListSerializer

    @swagger_auto_schema(
        operation_summary="Get list of pages",
        responses={200: page_list_response},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class PageDetailView(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer
    lookup_field = "slug"

    @swagger_auto_schema(
        operation_summary="Get page detail",
        responses={200: page_detail_response},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class RegionsDistrictsView(generics.ListAPIView):
    queryset = Region.objects.all().prefetch_related("districts")
    serializer_class = RegionSerializer

    @swagger_auto_schema(
        operation_summary="Get regions with districts",
        responses={200: regions_with_districts_response},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class CommonSettingsView(generics.ListAPIView):
    queryset = Setting.objects.all()
    serializer_class = CommonSettingsSerializer

    @swagger_auto_schema(
        operation_summary="Get site settings",
        responses={200: setting_response},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
