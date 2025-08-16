from accounts.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from store.models import Category


class StoreAPITests(APITestCase):
    def setUp(self):
        self.parent_category = Category.objects.create(name="Техника")
        self.child_category = Category.objects.create(name="Смартфоны", parent=self.parent_category)

        self.user = User.objects.create_user(
            phone_number="998901112233", full_name="Test User", password="testpass123"
        )

    def test_categories_list(self):
        url = reverse("categories_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["results"][0]["name"], "Техника")

    def test_categories_with_children(self):
        url = reverse("categories-with-children")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["results"][0]["children"][0]["name"], "Смартфоны")

    def test_sub_category(self):
        url = reverse("sub-category")
        response = self.client.get(url, {"parent_id": self.parent_category.id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["results"][0]["name"], "Смартфоны")
