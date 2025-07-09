import uuid
from django.db import models
from django.utils.text import slugify


class Page(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Region(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100)
    name_uz = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class District(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100)
    name_uz = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Setting(models.Model):
    phone = models.CharField(max_length=14, unique=True)
    support_email = models.EmailField(unique=True)
    working_hours = models.TextField()
    app_version = models.CharField(max_length=10)
    maintenance_code = models.BooleanField(default=False)