from django.urls import path

from . import views

urlpatterns = [
    path("category/", views.CategoriesListView.as_view(), name="categories_list"),
    path("ads/", views.AdCreateView.as_view(), name="ad_create"),
    path("ads/<str:slug>/", views.AdDetailView.as_view(), name="ad_detail"),
    path(
        "categories-with-children/",
        views.CategoryWithChildrenListView.as_view(),
        name="categories-with-children",
    ),
    path(
        "sub-category/",
        views.SubCategoryListView.as_view(),
        name="sub-category",
    ),
    path(
        "product-image-create/",
        views.ProductImageCreateView.as_view(),
        name="product-image-create",
    ),
    path(
        "product-download/<str:slug>/",
        views.ProductDownloadView.as_view(),
        name="product-download",
    ),
    path(
        "favourite-product-create/",
        views.FavouriteProductCreateView.as_view(),
        name="favourite-product-create",
    ),
    path(
        "favourite-product-create-by-id/",
        views.FavouriteProductCreateByIDView.as_view(),
        name="favourite-product-create-by-id",
    ),
    path(
        "my-favourite-product/",
        views.FavouriteProductListView.as_view(),
        name="my-favourite-products",
    ),
    path(
        "my-favourite-product-by-id/",
        views.FavouriteProductByIDListView.as_view(),
        name="my-favourite-products-by-id",
    ),
    path(
        "favourite-product/<int:pk>/delete/",
        views.FavouriteProductDeleteView.as_view(),
        name="favourite-product-delete",
    ),
    path(
        "favourite-product-by-id/<int:pk>/delete/",
        views.FavouriteProductDeleteByIDView.as_view(),
        name="favourite-product-delete-by-id",
    ),
    path("my-ads/", views.MyAdsListView.as_view(), name="my-ads-list"),
    path("my-ads/<int:pk>/", views.MyAdDetailView.as_view(), name="my-ad"),
    path(
        "search/category-product/",
        views.CategoryProductSearchView.as_view(),
        name="category-product-search",
    ),
]
