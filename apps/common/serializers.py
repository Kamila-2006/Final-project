from rest_framework import serializers
from .models import Page


class PagesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['slug', 'title']

class PageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['slug', 'title', 'content', 'created_at', 'updated_at']