from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Ad, AdPhoto


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'products_count']


class CategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class AdPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdPhoto
        fields = ['image']


class AdCreateSerializer(serializers.ModelSerializer):
    photos = serializers.ListField(child=serializers.URLField(), write_only=True)

    class Meta:
        model = Ad
        fields = ['name_uz', 'name_ru', 'category', 'description_uz', 'description_ru', 'price', 'photos']

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        photos_data = validated_data.pop('photos')
        ad = Ad.objects.create(seller=user, **validated_data)
        AdPhoto.objects.bulk_create([AdPhoto(ad=ad, image=url) for url in photos_data])
        return ad


class SellerShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'phone_number', 'profile_photo']


class AdResponseSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    seller = SellerShortSerializer()

    class Meta:
        model = Ad
        fields = [
            'id', 'name', 'slug', 'price',
            'photo', 'published_at', 'address',
            'seller', 'is_liked', 'updated_time'
        ]
        read_only_fields = fields

    def get_photo(self, obj):
        first_photo = obj.photos.first()
        return first_photo.image if first_photo else None

    def get_address(self, obj):
        seller_address = obj.seller.address
        return seller_address.name


class AdDetailSerializer(serializers.ModelSerializer):
    photos = AdPhotoSerializer(many=True, read_only=True)
    address = serializers.SerializerMethodField()
    seller = SellerShortSerializer()
    category = CategoryShortSerializer()
    # views_count = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = ['id', 'name', 'slug', 'description',
                  'price', 'photos', 'published_at',
                  'address', 'seller', 'category',
                  'is_liked', 'view_count', 'updated_time'
                  ]

        def get_address(self, obj):
            seller_address = obj.seller.address
            return seller_address.name