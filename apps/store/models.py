from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='category_icons/')
    products_count = models.DecimalField(max_digits=10, decimal_places=3)