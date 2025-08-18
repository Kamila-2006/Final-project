from io import BytesIO

from accounts.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image
from rest_framework.test import APITestCase

from store.models import Category


def generate_test_image():
    file = BytesIO()
    image = Image.new("RGB", (100, 100), "blue")  # просто синяя картинка
    image.save(file, "JPEG")
    file.seek(0)
    return SimpleUploadedFile("test.jpg", file.read(), content_type="image/jpeg")


class StoreAPITests(APITestCase):
    def setUp(self):
        self.parent_category = Category.objects.create(name="Техника")
        self.child_category = Category.objects.create(name="Смартфоны", parent=self.parent_category)

        self.user = User.objects.create_user(
            phone_number="998901112233", full_name="Test User", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

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

    def test_create_ad(self):
        url = reverse("ad_create")
        image = generate_test_image()

        data = {
            "name_uz": "telefon",
            "name_ru": "телефон",
            "category": self.child_category.id,
            "description_uz": "test uz desc",
            "description_ru": "test ru desc",
            "price": "2.02",
            "photos": [image],
        }

        response = self.client.post(url, data, format="multipart")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["name"], "телефон")
        self.assertEqual(response.data["data"]["seller"]["id"], self.user.id)
        self.assertEqual(response.data["data"]["seller"]["full_name"], "Test User")

    def test_get_ad_detail(self):
        create_url = reverse("ad_create")
        image = generate_test_image()
        ad_data = {
            "name_uz": "iPhone 11",
            "name_ru": "iPhone 11",
            "category": self.child_category.id,
            "description_uz": "test uz desc",
            "description_ru": "test description",
            "price": "21.45",
            "photos": [image],
        }
        create_response = self.client.post(create_url, ad_data, format="multipart")
        self.assertEqual(create_response.status_code, 201)

        slug = create_response.data["data"]["slug"]

        detail_url = reverse("ad_detail", kwargs={"slug": slug})
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["name"], "iPhone 11")
        self.assertEqual(response.data["data"]["category"]["name"], "Смартфоны")
        self.assertEqual(response.data["data"]["seller"]["id"], self.user.id)
