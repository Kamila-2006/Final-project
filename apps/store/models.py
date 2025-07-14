from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='category_icons/', null=True, blank=True)
    products_count = models.DecimalField(max_digits=10, decimal_places=3, default=0)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name