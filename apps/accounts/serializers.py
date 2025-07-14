from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.relations import PrimaryKeyRelatedField
from .models import User, Address
from store.models import Category


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['name', 'lat', 'long']

class SellerRegistrationSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    category = PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = User
        fields = ('full_name', 'project_name', 'category', 'phone_number', 'address')

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        user = User.objects.create_user(**validated_data)
        Address.objects.create(user=user, **address_data)
        return user

class SellerRegistrationResponseSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='category.id')
    address = serializers.CharField(source='address.name')

    class Meta:
        model = User
        fields = ['id', 'full_name', 'project_name', 'category_id', 'phone_number', 'address', 'status']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD

    def validate(self, attrs):
        attrs['username'] = attrs.get('phone_number')
        data = super().validate(attrs)

        user = self.user

        response_data = {
            'access_token': data['access'],
            'refresh_token': data['refresh'],
            'user': {
                'id': user.id,
                'full_name': user.full_name,
                'phone_number': user.phone_number,
            }
        }

        return response_data

    def to_internal_value(self, data):
        if 'phone_number' in data:
            data['username'] = data['phone_number']
        return super().to_internal_value(data)