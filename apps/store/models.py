from django.db import models
from django.utils.text import slugify
from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='category_icons/', null=True, blank=True)
    products_count = models.DecimalField(max_digits=10, decimal_places=3, default=0)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Ad(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ads')
    description = models.TextField()
    price = models.DecimalField(max_digits=14, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    published_at = models.DateTimeField(auto_now_add=True)
    is_liked = models.BooleanField(default=False)
    updated_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class AdPhoto(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='photos')
    image = models.URLField()

    def __str__(self):
        return f"Photo for {self.ad.name}"