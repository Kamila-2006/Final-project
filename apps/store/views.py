from rest_framework import generics
from rest_framework.response import Response
from common.utils.custom_response_decorator import custom_response
from .models import Category, Ad, AdPhoto
from .serializers import CategorySerializer, CategoryWithChildrenSerializer, AdCreateSerializer, AdDetailSerializer, AdPhotoSerializer
from common.pagination import CategoryPagination


@custom_response
class CategoriesListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination

    def get_queryset(self):
        return Category.objects.filter(parent__isnull=True)


@custom_response
class CategoryWithChildrenListView(generics.ListAPIView):
    serializer_class = CategoryWithChildrenSerializer
    pagination_class = CategoryPagination

    def get_queryset(self):
        return Category.objects.filter(parent__isnull=True)


@custom_response
class SubCategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination

    def get_queryset(self):
        parent_id = self.request.query_params.get('parent')
        if parent_id is not None:
            return Category.objects.filter(parent_id=parent_id)
        return Category.objects.none()


@custom_response
class AdCreateView(generics.CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer
    pagination_class = CategoryPagination


@custom_response
class AdDetailView(generics.RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@custom_response
class ProductImageCreateView(generics.CreateAPIView):
    queryset = AdPhoto.objects.all()
    serializer_class = AdPhotoSerializer