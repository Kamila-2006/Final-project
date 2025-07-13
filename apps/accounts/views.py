from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from .serializers import SellerRegistrationSerializer, SellerRegistrationResponseSerializer, CustomTokenObtainPairSerializer
from .models import User


class SellerRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SellerRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_serializer = SellerRegistrationResponseSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer