from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from common.utils.custom_response_decorator import custom_response
from .models import Category, Ad
from .serializers import CategorySerializer, AdCreateSerializer, AdResponseSerializer, AdDetailSerializer
from .pagination import CategoryPagination


@custom_response
class CategoriesListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination


@custom_response
class AdCreateView(generics.CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer
    pagination_class = CategoryPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        ad = serializer.save()
        response_serializer = AdResponseSerializer(ad)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@custom_response
class AdDetailView(generics.RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    lookup_field = 'slug'