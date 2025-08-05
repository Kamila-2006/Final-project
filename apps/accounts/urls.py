from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path(
        "seller/registration/",
        views.SellerRegistrationView.as_view(),
        name="seller_registration",
    ),
    path("login/", views.CustomLoginView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "token/verify/",
        views.CustomTokenVerifyView.as_view(),
        name="token_verify",
    ),
    path("me/", views.UserProfileView.as_view(), name="user_profile"),
    path("edit/", views.UserEditView.as_view(), name="user_edit"),
]
