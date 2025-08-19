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

    def test_ads_list(self):
        create_url = reverse("ad_create")
        for i in range(2):
            image = generate_test_image()
            data = {
                "name_uz": f"telefon{i}",
                "name_ru": f"телефон{i}",
                "category": self.child_category.id,
                "description_uz": "test uz desc",
                "description_ru": "test ru desc",
                "price": "1000.00",
                "photos": [image],
            }
            create_response = self.client.post(create_url, data, format="multipart")
            self.assertEqual(create_response.status_code, 201)

        list_url = reverse("ads-list")
        response = self.client.get(list_url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["seller"]["id"], self.user.id)
        self.assertEqual(response.data["results"][0]["seller"]["full_name"], "Test User")

    def test_create_favourite_product(self):
        create_url = reverse("ad_create")
        image = generate_test_image()
        ad_data = {
            "name_uz": "telefon",
            "name_ru": "телефон",
            "category": self.child_category.id,
            "description_uz": "test uz desc",
            "description_ru": "test ru desc",
            "price": "1000.00",
            "photos": [image],
        }
        ad_response = self.client.post(create_url, ad_data, format="multipart")
        self.assertEqual(ad_response.status_code, 201)
        product_id = ad_response.data["data"]["id"]

        self.client.force_authenticate(user=None)

        url = reverse("favourite-product-create-by-id")
        data = {"device_id": "1234567890testdevice", "product": product_id}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["product"], product_id)
        self.assertEqual(response.data["data"]["device_id"], "1234567890testdevice")

    def test_get_favourite_products_by_device_id(self):
        create_url = reverse("ad_create")
        image = generate_test_image()
        ad_data = {
            "name_uz": "iPhone",
            "name_ru": "Айфон",
            "category": self.child_category.id,
            "description_uz": "uz desc",
            "description_ru": "test description",
            "price": "21.45",
            "photos": [image],
        }
        ad_response = self.client.post(create_url, ad_data, format="multipart")
        product_id = ad_response.data["data"]["id"]

        self.client.force_authenticate(user=None)
        fav_url = reverse("favourite-product-create-by-id")
        self.client.post(
            fav_url, {"device_id": "1234567890testdevice", "product": product_id}, format="json"
        )

        list_url = reverse("my-favourite-products-by-id")
        response = self.client.get(list_url, {"device_id": "1234567890testdevice"})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["count"], 1)
        self.assertEqual(response.data["data"]["results"][0]["id"], product_id)
        self.assertEqual(response.data["data"]["results"][0]["name"], "Айфон")

    def test_delete_favourite_product(self):
        create_url = reverse("ad_create")
        image = generate_test_image()
        ad_data = {
            "name_uz": "telefon",
            "name_ru": "телефон",
            "category": self.child_category.id,
            "description_uz": "test uz desc",
            "description_ru": "test ru desc",
            "price": "1000.00",
            "photos": [image],
        }
        ad_response = self.client.post(create_url, ad_data, format="multipart")
        self.assertEqual(ad_response.status_code, 201)
        product_id = ad_response.data["data"]["id"]

        self.client.force_authenticate(user=None)

        fav_url = reverse("favourite-product-create-by-id")
        fav_data = {
            "device_id": "1234567890testdevice",
            "product": product_id,
        }
        fav_response = self.client.post(fav_url, fav_data, format="json")
        self.assertEqual(fav_response.status_code, 201)
        favourite_id = fav_response.data["data"]["id"]

        delete_url = reverse("favourite-product-delete-by-id", kwargs={"pk": favourite_id})
        delete_response = self.client.delete(f"{delete_url}?device_id=1234567890testdevice")

        self.assertEqual(delete_response.status_code, 204)
        self.assertTrue(delete_response.data["success"])
        self.assertIsNone(delete_response.data["data"])
