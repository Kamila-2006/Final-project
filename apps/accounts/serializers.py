from rest_framework import serializers
from .models import User, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['name', 'lat', 'long']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    address = AddressSerializer(write_only=True)

    class Meta:
        model = User
        fields = ('full_name', 'phone_number', 'password', 'role', 'profile_photo', 'address')
        extra_kwargs = {
            'role': {'required': False},
            'profile_photo': {'required': False},
        }

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        user = User.objects.create_user(**validated_data)
        Address.objects.create(user=user, **address_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = User
        fields = ['id', 'full_name', 'phone_number', 'profile_photo', 'address', 'created_at']