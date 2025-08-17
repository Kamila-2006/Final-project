from common.utils.custom_response_decorator import custom_response
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .openapi_schema import (
    edit_request,
    edit_response,
    login_request,
    login_response,
    me_response,
    seller_registration_request,
    seller_registration_response,
    token_refresh_request,
    token_refresh_response,
    token_verify_request,
    token_verify_response,
)
from .serializers import (
    CustomTokenObtainPairSerializer,
    SellerRegistrationSerializer,
    UserProfileSerializer,
)

User = get_user_model()


@swagger_auto_schema(
    request_body=seller_registration_request,
    responses={201: seller_registration_response},
    tags=["Accounts"],
)
@custom_response
class SellerRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all().select_related("category", "region", "district", "address")
    serializer_class = SellerRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_serializer = self.get_serializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    request_body=login_request,
    responses={200: login_response},
    tags=["Accounts"],
)
@custom_response
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@swagger_auto_schema(
    request_body=token_refresh_request,
    responses={200: token_refresh_response},
    tags=["Accounts"],
)
@custom_response
class CustomTokenRefreshView(TokenRefreshView):
    pass


@swagger_auto_schema(
    request_body=token_verify_request,
    responses={200: token_verify_response},
    tags=["Accounts"],
)
@custom_response
class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            token = UntypedToken(request.data["token"])
            user_id = token.payload.get("user_guid")

            return Response({"valid": True, "user_id": user_id}, status=status.HTTP_200_OK)
        except ValidationError:
            return Response(
                {"valid": False, "user_id": None},
                status=status.HTTP_401_UNAUTHORIZED,
            )


@swagger_auto_schema(
    responses={200: me_response},
    tags=["Accounts"],
)
@custom_response
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.select_related("address", "category", "region", "district").get(
            pk=self.request.user.pk
        )


@swagger_auto_schema(
    request_body=edit_request,
    responses={200: edit_response},
    tags=["Accounts"],
)
class UserEditView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.select_related("address", "category", "region", "district").get(
            pk=self.request.user.pk
        )
