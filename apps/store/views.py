from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Ad
from .serializers import CategorySerializer, AdCreateSerializer, AdResponseSerializer, AdDetailSerializer
from common.pagination import CustomPagination


class CategoriesListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPagination

class AdCreateView(generics.CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        ad = serializer.save()
        response_serializer = AdResponseSerializer(ad)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class AdDetailView(generics.RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    lookup_field = 'slug'