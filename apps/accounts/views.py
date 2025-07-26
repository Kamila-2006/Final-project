from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from common.utils.custom_response_decorator import custom_response
from .serializers import SellerRegistrationSerializer, SellerRegistrationResponseSerializer, \
    CustomTokenObtainPairSerializer, UserProfileSerializer
from .models import User


@custom_response
class SellerRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SellerRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_serializer = SellerRegistrationResponseSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@custom_response
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@custom_response
class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            token = UntypedToken(request.data['token'])
            user_id = token.payload.get('user_guid')

            return Response({
                "valid": True,
                "user_id": user_id
            }, status=status.HTTP_200_OK)
        except ValidationError:
            return Response({
                "valid": False,
                "user_id": None
            }, status=status.HTTP_401_UNAUTHORIZED)


@custom_response
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


@custom_response
class UserEditView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user