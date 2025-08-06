from common.utils.custom_response_decorator import custom_response
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView

from .serializers import (
    CustomTokenObtainPairSerializer,
    SellerRegistrationSerializer,
    UserProfileSerializer,
)

User = get_user_model()


@custom_response
class SellerRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SellerRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@custom_response
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


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


@custom_response
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@custom_response
class UserEditView(UserProfileView):
    pass
