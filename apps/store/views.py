from common.pagination import CategoryPagination, FavouriteProductPagination, MyAdsListPagination
from common.utils.custom_response_decorator import custom_response
from django.db.models import Count
from rest_framework import generics, permissions, serializers
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
    MyAdSerializer,
    MyAdsListSerializer,
)


class CategoriesListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination

    def get_queryset(self):
        return Category.objects.filter(parent__isnull=True).annotate(products_count=Count("ads"))


@custom_response
class CategoryWithChildrenListView(generics.ListAPIView):
    serializer_class = CategoryWithChildrenSerializer
    pagination_class = CategoryPagination

    def get_queryset(self):
        return Category.objects.filter(parent__isnull=True).prefetch_related("child")


@custom_response
class SubCategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination

    def get_queryset(self):
        parent_id = self.request.query_params.get("parent_id")
        if parent_id is not None:
            return Category.objects.filter(parent_id=parent_id).annotate(
                products_count=Count("ads")
            )
        return Category.objects.none()


@custom_response
class AdCreateView(generics.CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer
    pagination_class = CategoryPagination


@custom_response
class AdDetailView(generics.RetrieveAPIView):
    queryset = Ad.objects.select_related("seller__address", "category").prefetch_related(
        "photos", "favourites"
    )
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
    queryset = Ad.objects.select_related("seller__address", "category").prefetch_related(
        "photos", "favourites"
    )
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@custom_response
class FavouriteProductCreateByIDView(generics.CreateAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteProductSerializer

    def perform_create(self, serializer):
        device_id = self.request.data.get("device_id")
        if not device_id:
            raise serializers.ValidationError({"device_id": "Это поле обязательно."})
        serializer.save(device_id=device_id)


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
class FavouriteProductDeleteByIDView(generics.DestroyAPIView):
    serializer_class = FavouriteProductSerializer

    def get_queryset(self):
        device_id = self.request.query_params.get("device_id")
        if not device_id:
            raise serializers.ValidationError(
                {"device_id": "Это поле обязательно в query-параметрах."}
            )
        return FavouriteProduct.objects.filter(device_id=device_id)

    def get_object(self):
        product_id = self.kwargs["pk"]
        return self.get_queryset().get(product_id=product_id)


@custom_response
class FavouriteProductListView(generics.ListAPIView):
    serializer_class = FavouriteProductListSerializer
    pagination_class = FavouriteProductPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = (
            Ad.objects.filter(favourites__user=user)
            .select_related("seller", "seller__address", "category")
            .prefetch_related("photos", "favourites")
        )

        category_id = self.request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset


@custom_response
class FavouriteProductByIDListView(generics.ListAPIView):
    serializer_class = FavouriteProductListSerializer
    pagination_class = FavouriteProductPagination

    def get_queryset(self):
        device_id = self.request.query_params.get("device_id")
        if not device_id:
            raise serializers.ValidationError(
                {"device_id": "Это поле обязательно в query-параметрах."}
            )

        queryset = (
            Ad.objects.filter(favourites__device_id=device_id)
            .select_related("seller", "seller__address", "category")
            .prefetch_related("photos", "favourites")
        )

        category_id = self.request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["device_id"] = self.request.query_params.get("device_id")
        return context


@custom_response
class MyAdsListView(generics.ListAPIView):
    serializer_class = MyAdsListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MyAdsListPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Ad.objects.filter(seller=user).order_by("-published_at")

        status = self.request.query_params.get("status")
        if status in ["active", "inactive", "pending", "rejected"]:
            queryset = queryset.filter(status=status)

        return queryset


@custom_response
class MyAdDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MyAdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ad.objects.filter(seller=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=["view_count"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
