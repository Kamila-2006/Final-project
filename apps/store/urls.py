from django.urls import path
from . import views
from .views import CategoryWithChildrenListView

urlpatterns = [
    path('categories/', views.CategoriesListView.as_view(), name='categories_list'),
    path('ads/', views.AdCreateView.as_view(), name='ad_create'),
    path('ads/<str:slug>/', views.AdDetailView.as_view(), name='ad_detail'),
    path('categories-with-children/', CategoryWithChildrenListView.as_view(), name='categories-with-children'),
]