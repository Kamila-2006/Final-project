from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Ad, AdPhoto, Category, FavouriteProduct

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "icon", "products_count"]

    def get_products_count(self, obj):
        return obj.ads.count()


class ChildCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    icon = serializers.ImageField()


class CategoryWithChildrenSerializer(serializers.ModelSerializer):
    children = ChildCategorySerializer(many=True, source="child")

    class Meta:
        model = Category
        fields = ["id", "name", "icon", "children"]


class CategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class AdPhotoSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())

    class Meta:
        model = AdPhoto
        fields = ["id", "image", "is_main", "product_id", "created_at"]
        read_only_fields = ["id", "created_at"]


class SellerShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "phone_number", "profile_photo"]


class AdCreateSerializer(serializers.ModelSerializer):
    photos = serializers.ListField(child=serializers.ImageField(), write_only=True)
    photo = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    seller = SellerShortSerializer()
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

    def get_address(self, obj):
        seller_address = obj.seller.address
        return seller_address.name

    def get_is_liked(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return obj.favourites.filter(user=user).exists()


class AdDetailSerializer(serializers.ModelSerializer):
    photos = AdPhotoSerializer(many=True, read_only=True)
    address = serializers.SerializerMethodField()
    seller = SellerShortSerializer()
    category = CategoryShortSerializer()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "photos",
            "published_at",
            "address",
            "seller",
            "category",
            "is_liked",
            "view_count",
            "updated_time",
        ]

        def get_address(self, obj):
            seller_address = obj.seller.address
            return seller_address.name

        def get_is_liked(self, obj):
            user = self.context["request"].user
            if not user.is_authenticated:
                return False
            return obj.favourites.filter(user=user).exists()


class FavouriteProductSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())

    class Meta:
        model = FavouriteProduct
        fields = ["id", "product", "created_at"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        product = validated_data["product"]

        obj, created = FavouriteProduct.objects.get_or_create(user=user, product=product)
        return obj


class FavouriteProductListSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    seller = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "published_at",
            "address",
            "seller",
            "photo",
            "is_liked",
            "updated_time",
        ]

    def get_address(self, obj):
        seller_address = obj.seller.address
        return seller_address.name

    def get_seller(self, obj):
        return obj.seller.full_name

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
