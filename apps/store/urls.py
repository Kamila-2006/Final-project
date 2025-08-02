from django.urls import path
from . import views


urlpatterns = [
    path('categories/', views.CategoriesListView.as_view(), name='categories_list'),
    path('ads/', views.AdCreateView.as_view(), name='ad_create'),
    path('ads/<str:slug>/', views.AdDetailView.as_view(), name='ad_detail'),
    path('categories-with-children/', views.CategoryWithChildrenListView.as_view(), name='categories-with-children'),
    path('sub-category/', views.SubCategoryListView.as_view(), name='sub-category'),
    path('product-image-create/', views.ProductImageCreateView.as_view(), name='product-image-create'),

]