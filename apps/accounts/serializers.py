from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from .models import User, Address
from store.models import Category


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['name', 'lat', 'long']

class SellerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    address = AddressSerializer()
    category = PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = User
        fields = ('full_name', 'project_name', 'category', 'phone_number', 'password', 'address')

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
