from django.db import models
from django.utils.text import slugify
from .base_models import BaseModel


class Page(BaseModel):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100)
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Region(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class District(BaseModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Setting(models.Model):
    phone = models.CharField(max_length=14, unique=True)
    support_email = models.EmailField(unique=True)
    working_hours = models.TextField()
    app_version = models.CharField(max_length=10)
    maintenance_code = models.BooleanField(default=False)