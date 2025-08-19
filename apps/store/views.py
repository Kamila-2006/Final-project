from common.pagination import (
    AdsListPagination,
    CategoryPagination,
    FavouriteProductPagination,
    MyAdsListPagination,
    SearchListPagination,
)
from common.utils.custom_response_decorator import custom_response
from django.db.models import Count, Prefetch, Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics, permissions, serializers
from rest_framework.response import Response

from .filters import AdFilter
from .models import Ad, AdPhoto, Category, FavouriteProduct, MySearch, SearchCount
from .openapi_schema import (
    ad_create_response,
    ad_detail_response,
    ad_list_filter_params,
    ad_list_response,
    categories_list_response,
    categories_with_children_response,
    category_product_search_response,
    favourite_create_response,
    favourite_list_response,
    my_ad_detail_response,
    my_ads_list_response,
    mysearch_create_response,
    mysearch_delete_response,
    mysearch_list_response,
    popular_search_response,
    product_download_response,
    product_image_create_response,
    search_complete_response,
    search_count_increase_response,
    subcategories_list_response,
)
from .serializers import (
    AdCreateSerializer,
    AdDetailSerializer,
    AdListSerializer,
    AdPhotoSerializer,
    CategorySerializer,
    CategoryWithChildrenSerializer,
    FavouriteProductListSerializer,
    FavouriteProductSerializer,
    MyAdSerializer,
    MyAdsListSerializer,
    MySearchCreateSerializer,
    MySearchListSerializer,
    PopularSearchSerializer,
    SearchCategorySerializer,
    SearchCompleteSerializer,
    SearchCountSerializer,
    SearchProductSerializer,
)


@custom_response
class CategoriesListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination

    def get_queryset(self):
        return Category.objects.filter(parent__isnull=True).annotate(products_count=Count("ads"))

    @swagger_auto_schema(responses={200: categories_list_response})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class CategoryWithChildrenListView(generics.ListAPIView):
    serializer_class = CategoryWithChildrenSerializer
    pagination_class = CategoryPagination

    def get_queryset(self):
        return Category.objects.filter(parent__isnull=True).prefetch_related("child")

    @swagger_auto_schema(responses={200: categories_with_children_response})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


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

    @swagger_auto_schema(responses={200: subcategories_list_response})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class AdCreateView(generics.CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer
    pagination_class = CategoryPagination

    @swagger_auto_schema(responses={201: ad_create_response})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@custom_response
class AdDetailView(generics.RetrieveAPIView):
    serializer_class = AdDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Ad.objects.select_related("seller__address", "category").prefetch_related(
            "photos",
            Prefetch(
                "favourites",
                queryset=FavouriteProduct.objects.only("user_id", "device_id", "product_id"),
            ),
        )

    @swagger_auto_schema(responses={200: ad_detail_response})
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=["view_count"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

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

    @swagger_auto_schema(responses={200: product_download_response})
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=["view_count"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

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

    @swagger_auto_schema(responses={201: product_image_create_response})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@custom_response
class FavouriteProductCreateView(generics.CreateAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={201: favourite_create_response})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@custom_response
class FavouriteProductCreateByIDView(generics.CreateAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteProductSerializer

    @swagger_auto_schema(responses={201: favourite_create_response})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

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
        if getattr(self, "swagger_fake_view", False):
            return FavouriteProduct.objects.none()  # пустой queryset, чисто для Swagger

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

    @swagger_auto_schema(responses={200: favourite_list_response})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = (
            Ad.objects.filter(favourites__user=user)
            .select_related("seller__address")
            .prefetch_related(
                "photos",
                Prefetch(
                    "favourites",
                    queryset=FavouriteProduct.objects.only("user_id", "device_id", "product_id"),
                ),
            )
        )

        category_id = self.request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset


@custom_response
class FavouriteProductByIDListView(generics.ListAPIView):
    serializer_class = FavouriteProductListSerializer
    pagination_class = FavouriteProductPagination

    @swagger_auto_schema(responses={200: favourite_list_response})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        device_id = self.request.query_params.get("device_id")
        if not device_id:
            raise serializers.ValidationError(
                {"device_id": "Это поле обязательно в query-параметрах."}
            )

        queryset = (
            Ad.objects.filter(favourites__device_id=device_id)
            .select_related("seller__address")
            .prefetch_related(
                "photos",
                Prefetch(
                    "favourites",
                    queryset=FavouriteProduct.objects.only("user_id", "device_id", "product_id"),
                ),
            )
        )
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

    @swagger_auto_schema(responses={200: my_ads_list_response})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = (
            Ad.objects.filter(seller=user)
            .select_related("seller__address")
            .prefetch_related("photos", "favourites")
            .order_by("-published_at")
        )

        status = self.request.query_params.get("status")
        if status in ["active", "inactive", "pending", "rejected"]:
            queryset = queryset.filter(status=status)

        return queryset


@custom_response
class MyAdDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MyAdSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={200: my_ad_detail_response, 204: "Deleted successfully"})
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: my_ad_detail_response})
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: my_ad_detail_response})
    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(responses={204: "Deleted successfully"})
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        return (
            Ad.objects.filter(seller=self.request.user)
            .select_related("seller__address", "category")
            .prefetch_related("photos", "favourites")
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=["view_count"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@custom_response
class CategoryProductSearchView(generics.ListAPIView):
    serializer_class = serializers.Serializer
    pagination_class = SearchListPagination

    @swagger_auto_schema(responses={200: category_product_search_response})
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        q = self.request.query_params.get("q", "")

        categories = list(Category.objects.filter(name__icontains=q))
        products = list(
            Ad.objects.filter(Q(name__icontains=q) | Q(description__icontains=q), status="active")
        )

        return categories + products

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            results = []
            for obj in page:
                if isinstance(obj, Category):
                    results.append(
                        SearchCategorySerializer(obj, context=self.get_serializer_context()).data
                    )
                else:
                    results.append(
                        SearchProductSerializer(obj, context=self.get_serializer_context()).data
                    )

            return self.get_paginated_response(results)

        results = []
        for obj in queryset:
            if isinstance(obj, Category):
                results.append(
                    SearchCategorySerializer(obj, context=self.get_serializer_context()).data
                )
            else:
                results.append(
                    SearchProductSerializer(obj, context=self.get_serializer_context()).data
                )

        return Response(results)


@custom_response
class SearchCompleteView(generics.ListAPIView):
    pagination_class = SearchListPagination
    serializer_class = SearchCompleteSerializer

    @swagger_auto_schema(responses={200: search_complete_response})
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        q = self.request.query_params.get("q", "")
        return Ad.objects.filter(
            Q(name__icontains=q) | Q(description__icontains=q), status="active"
        ).order_by("name")


@custom_response
class SearchCountIncreaseView(generics.RetrieveAPIView):
    serializer_class = SearchCountSerializer
    queryset = Ad.objects.all()

    @swagger_auto_schema(responses={200: search_count_increase_response})
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_object(self):
        product_id = self.kwargs["product_id"]
        product = get_object_or_404(Ad, id=product_id)

        search_count, created = SearchCount.objects.get_or_create(product=product)
        search_count.search_count += 1
        search_count.save()

        return search_count


@custom_response
class PopularsView(generics.ListAPIView):
    serializer_class = PopularSearchSerializer
    pagination_class = SearchListPagination

    @swagger_auto_schema(responses={200: popular_search_response})
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return SearchCount.objects.select_related("product").order_by("-search_count")


@custom_response
class MySearchCreateView(generics.CreateAPIView):
    queryset = MySearch.objects.all()
    serializer_class = MySearchCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={200: mysearch_create_response})
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@custom_response
class MySearchListView(generics.ListAPIView):
    queryset = MySearch.objects.all()
    serializer_class = MySearchListSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={200: mysearch_list_response})
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return MySearch.objects.filter(user=self.request.user).order_by("-created_at")


@custom_response
class MySearchDeleteView(generics.DestroyAPIView):
    queryset = MySearch.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={200: mysearch_delete_response})
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@custom_response
class AdListView(generics.ListAPIView):
    serializer_class = AdListSerializer
    pagination_class = AdsListPagination
    queryset = Ad.objects.all().select_related("seller")

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ["name", "slug", "description"]
    ordering_fields = ["price", "published_at", "updated_time"]
    filterset_class = AdFilter

    def get_queryset(self):
        qs = super().get_queryset()

        is_top = self.request.query_params.get("is_top")
        if is_top:
            qs = qs.filter(search_count_obj__search_count__gt=0).order_by(
                "-search_count_obj__search_count"
            )

        return qs

    @swagger_auto_schema(responses={200: ad_list_response}, manual_parameters=ad_list_filter_params)
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
