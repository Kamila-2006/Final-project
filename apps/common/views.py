from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Page
from .serializers import PagesListSerializer, PageDetailSerializer
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