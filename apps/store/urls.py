from django.urls import path

from . import views

urlpatterns = [
    path("category/", views.CategoriesListView.as_view(), name="categories_list"),
    path("ads/", views.AdCreateView.as_view(), name="ad_create"),
    path("ads/list/", views.AdListView.as_view(), name="ads-list"),
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
    path("my-ads/", views.MyAdsListView.as_view(), name="my-ads"),
    path("my-ads/<int:pk>/", views.MyAdDetailView.as_view(), name="my-ad"),
    path(
        "search/category-product/",
        views.CategoryProductSearchView.as_view(),
        name="category-product-search",
    ),
    path("search/complete/", views.SearchCompleteView.as_view(), name="search-complete"),
    path(
        "search/count-increase/<int:product_id>/",
        views.SearchCountIncreaseView.as_view(),
        name="search-count",
    ),
    path("search/populars/", views.PopularsView.as_view(), name="popular-searches"),
    path("my-search/", views.MySearchCreateView.as_view(), name="my-search-create"),
    path("my-search/list/", views.MySearchListView.as_view(), name="my-search-list"),
    path("my-search/<int:pk>/delete/", views.MySearchDeleteView.as_view(), name="my-search-delete"),
]
