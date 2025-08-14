from common.models import BaseModel, District, Region
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from store.models import Category

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, BaseModel):

    ROLE_CHOICES = [
        ("super_admin", "Super Admin"),
        ("admin", "Admin"),
        ("seller", "Seller"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    full_name = models.CharField(max_length=100)
    project_name = models.CharField(max_length=50)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="sellers",
        null=True,
        blank=True,
    )
    phone_number = models.CharField(max_length=13, unique=True)
    profile_photo = models.ImageField(upload_to="profile-photos/", null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="seller")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="pending")
    region = models.ForeignKey(
        Region, on_delete=models.SET_NULL, related_name="users", null=True, blank=True
    )
    district = ChainedForeignKey(
        District,
        chained_field="region",
        chained_model_field="region",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.full_name


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="address")
    name = models.TextField()
    lat = models.FloatField()
    long = models.FloatField()

    def __str__(self):
        return self.name
