from django.urls import path
from . import views


urlpatterns = [
    path('pages/', views.CommonPagesView.as_view(), name='common_pages'),
    path('pages/<str:slug>/', views.PageDetailView.as_view(), name='common_page_detail'),
    path('regions-with-districts/', views.RegionsDistrictsView.as_view(), name='regions_with_districts'),
    path('settings/', views.CommonSettingsView.as_view(), name='common-settings'),
]