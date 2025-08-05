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
        "favourite-product/<int:pk>/delete/",
        views.FavouriteProductDeleteView.as_view(),
        name="favourite-product-delete",
    ),
    path(
        "my-favourite-product/",
        views.FavouriteProductListView.as_view(),
        name="my-favourite-products",
    ),
]
