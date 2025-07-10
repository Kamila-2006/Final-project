from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Page, Region, Setting
from .serializers import PagesListSerializer, PageDetailSerializer, RegionSerializer, CommonSettingsSerializer
from .pagination import CustomPagination


class CommonPagesView(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PagesListSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

class PageDetailView(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer
    permission_classes = [AllowAny]

class RegionsDistrictsView(generics.ListAPIView):
    queryset = Region.objects.all().prefetch_related('districts')
    serializer_class = RegionSerializer
    pagination_class = CustomPagination

class CommonSettingsView(generics.RetrieveAPIView):
    queryset = Setting.objects.all()
    serializer_class = CommonSettingsSerializer