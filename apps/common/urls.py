from django.urls import path
from . import views


urlpatterns = [
    path('pages/', views.CommonPagesView.as_view(), name='common-pages'),
    path('pages/<str:slug>/', views.PageDetailView.as_view(), name='common-page-detail'),
]