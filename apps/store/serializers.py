from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Ad, AdPhoto, Category, FavouriteProduct

User = get_user_model()


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    icon = serializers.ImageField()


class ChildCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    icon = serializers.ImageField()


class CategoryWithChildrenSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    icon = serializers.ImageField()
    children = ChildCategorySerializer(many=True, source="child")


class CategoryShortSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class AdPhotoSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())

    class Meta:
        model = AdPhoto
        fields = ["id", "image", "is_main", "product_id", "created_at"]
        read_only_fields = ["id", "created_at"]


class SellerShortSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    phone_number = serializers.CharField()
    profile_photo = serializers.ImageField()


class AdCreateSerializer(serializers.ModelSerializer):
    photos = serializers.ListField(child=serializers.ImageField(), write_only=True)
    photo = serializers.SerializerMethodField()
    address = serializers.CharField(source="seller.address.name", read_only=True)
    seller = SellerShortSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = [
            "id",
            "name",
            "name_uz",
            "name_ru",
            "slug",
            "category",
            "description_uz",
            "description_ru",
            "price",
            "photos",
            "photo",
            "published_at",
            "address",
            "seller",
            "is_liked",
            "updated_time",
        ]
        extra_kwargs = {
            "name_uz": {"write_only": True},
            "name_ru": {"write_only": True},
            "category": {"write_only": True},
            "description_uz": {"write_only": True},
            "description_ru": {"write_only": True},
            "photos": {"write_only": True},
        }
        read_only_fields = [
            "id",
            "name",
            "slug",
            "photo",
            "published_at",
            "address",
            "seller",
            "is_liked",
            "updated_time",
        ]

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        photos_data = validated_data.pop("photos")
        ad = Ad.objects.create(seller=user, **validated_data)
        AdPhoto.objects.bulk_create([AdPhoto(ad=ad, image=url) for url in photos_data])
        return ad

    def get_photo(self, obj):
        main_photo = obj.photos.filter(is_main=True).first()
        if main_photo:
            return main_photo.image.url

        first_photo = obj.photos.first()
        if first_photo:
            return first_photo.image.url

        return None

    def get_is_liked(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return obj.favourites.filter(user=user).exists()


class AdDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=14, decimal_places=2)
    photos = AdPhotoSerializer(many=True, read_only=True)
    published_at = serializers.DateTimeField()
    address = serializers.CharField(source="seller.address.name")
    seller = SellerShortSerializer()
    category = CategoryShortSerializer()
    is_liked = serializers.SerializerMethodField()
    view_count = serializers.IntegerField()
    updated_time = serializers.DateTimeField()

    def get_is_liked(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return obj.favourites.filter(user=user).exists()


class FavouriteProductSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())

    class Meta:
        model = FavouriteProduct
        fields = ["id", "product", "device_id", "created_at"]
        read_only_fields = ["id", "created_at"]
        extra_kwargs = {
            "device_id": {"required": False},
        }

    def validate(self, attrs):
        user = self.context["request"].user
        device_id = attrs.get("device_id")

        if not user.is_authenticated and not device_id:
            raise serializers.ValidationError("Anonymous users must provide a device_id.")

        return attrs

    def create(self, validated_data):
        user = (
            self.context["request"].user if self.context["request"].user.is_authenticated else None
        )
        device_id = validated_data.get("device_id")
        product = validated_data["product"]

        if user:
            obj, _ = FavouriteProduct.objects.get_or_create(user=user, product=product)
        else:
            obj, _ = FavouriteProduct.objects.get_or_create(device_id=device_id, product=product)

        return obj


class FavouriteProductListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=14, decimal_places=2)
    published_at = serializers.DateTimeField()
    address = serializers.CharField(source="seller.address.name")
    seller = serializers.CharField(source="seller.full_name")
    photo = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    updated_time = serializers.DateTimeField()

    def get_photo(self, obj):
        main_photo = obj.photos.filter(is_main=True).first()
        if main_photo:
            return main_photo.image.url

        first_photo = obj.photos.first()
        if first_photo:
            return first_photo.image.url

        return None

    def get_is_liked(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.favourites.filter(user=user).exists()

        device_id = self.context.get("device_id")
        if device_id:
            return obj.favourites.filter(device_id=device_id).exists()

        return False


class MyAdsListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()
    price = serializers.DecimalField(max_digits=14, decimal_places=2)
    photo = serializers.SerializerMethodField()
    published_at = serializers.DateTimeField()
    address = serializers.CharField(source="seller.address.name")
    status = serializers.CharField()
    view_count = serializers.IntegerField()
    is_liked = serializers.SerializerMethodField()
    updated_time = serializers.DateTimeField()

    def get_photo(self, obj):
        main_photo = obj.photos.filter(is_main=True).first()
        if main_photo:
            return main_photo.image.url

        first_photo = obj.photos.first()
        if first_photo:
            return first_photo.image.url

        return None

    def get_is_liked(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return obj.favourites.filter(user=user).exists()


class MyAdSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.filter(parent=None))
    photos = AdPhotoSerializer(many=True, read_only=True)
    new_photos = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Ad
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "category",
            "price",
            "photos",
            "new_photos",
            "published_at",
            "status",
            "view_count",
            "updated_time",
        ]
        read_only_fields = ["id", "slug", "published_at", "status", "view_count", "updated_time"]

    def update(self, instance, validated_data):
        new_photos = validated_data.pop("new_photos", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if new_photos:
            instance.photos.all().delete()

            for photo_file in new_photos:
                AdPhoto.objects.create(ad=instance, image=photo_file)

        return instance
