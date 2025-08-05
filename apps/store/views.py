from common.pagination import CategoryPagination, FavouriteProductPagination
from common.utils.custom_response_decorator import custom_response
from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Ad, AdPhoto, Category, FavouriteProduct
from .serializers import (
    AdCreateSerializer,
    AdDetailSerializer,
    AdPhotoSerializer,
    CategorySerializer,
    CategoryWithChildrenSerializer,
    FavouriteProductListSerializer,
    FavouriteProductSerializer,
)


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
        parent_id = self.request.query_params.get("parent")
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
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=["view_count"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@custom_response
class ProductDownloadView(generics.RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=["view_count"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@custom_response
class ProductImageCreateView(generics.CreateAPIView):
    queryset = AdPhoto.objects.all()
    serializer_class = AdPhotoSerializer


@custom_response
class FavouriteProductCreateView(generics.CreateAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteProductSerializer
    permission_classes = [permissions.IsAuthenticated]


@custom_response
class FavouriteProductDeleteView(generics.DestroyAPIView):
    serializer_class = FavouriteProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavouriteProduct.objects.filter(user=self.request.user)

    def get_object(self):
        product_id = self.kwargs["pk"]
        return self.get_queryset().get(product_id=product_id)


@custom_response
class FavouriteProductListView(generics.ListAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteProductListSerializer
    pagination_class = FavouriteProductPagination
    permission_classes = [permissions.IsAuthenticated]
