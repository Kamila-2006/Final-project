from django.urls import path
from . import views


urlpatterns = [
    path('categories/', views.CategoriesListView.as_view(), name='categories_list'),
    path('ads/', views.AdCreateView.as_view(), name='ad_create'),
    path('ads/<str:slug>/', views.AdDetailView.as_view(), name='ad_detail'),
]