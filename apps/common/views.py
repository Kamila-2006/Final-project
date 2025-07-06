from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Page
from .serializers import PageSerializer
from .pagination import CustomPagination


class CommonPagesView(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination