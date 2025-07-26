from rest_framework import serializers
from .models import Page, Region, District, Setting


class PagesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['slug', 'title']


class PageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['slug', 'title', 'content', 'created_time', 'updated_time']


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']


class RegionSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True)

    class Meta:
        model = Region
        fields = ['id', 'name', 'districts']


class CommonSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ['phone', 'support_email', 'working_hours', 'app_version', 'maintenance_code']