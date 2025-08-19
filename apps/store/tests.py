from io import BytesIO

from accounts.models import User
from common.models import Region
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image
from rest_framework.test import APITestCase

from .models import Ad, Category, MySearch, SearchCount


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
        url = reverse("ads-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertIn("results", response.data["data"])  # <--- исправлено
        self.assertIsInstance(response.data["data"]["results"], list)

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

    def test_create_favourite_product_authenticated_user(self):
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

        url = reverse("favourite-product-create")
        data = {"product": product_id}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["product"], product_id)
        self.assertEqual(response.data["data"]["device_id"], None)

    def test_get_my_favourite_products_authenticated_user(self):
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
        ad_response = self.client.post(create_url, ad_data, format="multipart")
        self.assertEqual(ad_response.status_code, 201)
        product_id = ad_response.data["data"]["id"]

        fav_url = reverse("favourite-product-create")
        fav_response = self.client.post(fav_url, {"product": product_id}, format="json")
        self.assertEqual(fav_response.status_code, 201)

        list_url = reverse("my-favourite-products")
        response = self.client.get(list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["count"], 1)
        self.assertEqual(response.data["data"]["results"][0]["id"], product_id)
        self.assertEqual(response.data["data"]["results"][0]["name"], "iPhone 11")

    def test_delete_favourite_product_authenticated_user(self):
        create_url = reverse("ad_create")
        image = generate_test_image()
        ad_data = {
            "name_uz": "iPhone 11",
            "name_ru": "iPhone 11",
            "category": self.child_category.id,
            "description_uz": "uz desc",
            "description_ru": "test description",
            "price": "21.45",
            "photos": [image],
        }
        ad_response = self.client.post(create_url, ad_data, format="multipart")
        self.assertEqual(ad_response.status_code, 201)
        product_id = ad_response.data["data"]["id"]

        fav_url = reverse("favourite-product-create")
        fav_response = self.client.post(fav_url, {"product": product_id}, format="json")
        self.assertEqual(fav_response.status_code, 201)
        favourite_id = fav_response.data["data"]["id"]

        delete_url = reverse("favourite-product-delete", kwargs={"pk": favourite_id})
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 204)
        self.assertTrue(response.data["success"])
        self.assertIsNone(response.data["data"])

    def test_my_ads_list_authenticated_user(self):
        create_url = reverse("ad_create")

        image1 = generate_test_image()
        ad_data1 = {
            "name_uz": "Телефон",
            "name_ru": "телефон",
            "category": self.child_category.id,
            "description_uz": "uz desc",
            "description_ru": "test desc",
            "price": "2.02",
            "photos": [image1],
            "address": "Toshkent shahar, Mirobod tumani, Amir Temur ko'chasi 16-uy",
        }
        self.client.post(create_url, ad_data1, format="multipart")

        image2 = generate_test_image()
        ad_data2 = {
            "name_uz": "vivo 53s",
            "name_ru": "vivo 53s",
            "category": self.child_category.id,
            "description_uz": "uz desc",
            "description_ru": "desc ru",
            "price": "3000000.00",
            "photos": [image2],
            "address": "Toshkent shahar, Mirobod tumani, Amir Temur ko'chasi 16-uy",
        }
        self.client.post(create_url, ad_data2, format="multipart")

        url = reverse("my-ads")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.data["success"])
        self.assertIn("results", response.data["data"])

        results = response.data["data"]["results"]
        self.assertGreaterEqual(len(results), 2)

        for ad in results:
            self.assertIn("id", ad)
            self.assertIn("name", ad)
            self.assertIn("price", ad)
            self.assertIn("status", ad)

    def test_my_ad_detail_authenticated_user(self):
        create_url = reverse("ad_create")
        image = generate_test_image()
        ad_data = {
            "name_uz": "vivo 53s",
            "name_ru": "vivo 53s",
            "category": self.child_category.id,
            "description_uz": "uz desc",
            "description_ru": "Smartphone VIVO 53s",
            "price": "3000000.00",
            "photos": [image],
            "address": "Toshkent shahar, Mirobod tumani, Amir Temur ko'chasi 16-uy",
        }
        create_response = self.client.post(create_url, ad_data, format="multipart")
        self.assertEqual(create_response.status_code, 201)
        ad_id = create_response.data["data"]["id"]

        url = reverse("my-ad", kwargs={"pk": ad_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.data["success"])
        self.assertIn("id", response.data["data"])
        self.assertIn("name", response.data["data"])
        self.assertIn("description", response.data["data"])
        self.assertIn("category", response.data["data"])
        self.assertIn("price", response.data["data"])
        self.assertIn("photos", response.data["data"])
        self.assertIn("status", response.data["data"])
        self.assertIn("view_count", response.data["data"])

        self.assertEqual(response.data["data"]["id"], ad_id)

    def test_update_my_ad_put(self):
        ad = Ad.objects.create(
            name="Old Ad",
            category=self.parent_category,
            description="Old description",
            price=1000,
            seller=self.user,
        )

        new_image = generate_test_image()

        data = {
            "name": "iPhone 15 Pro Max 256GB Titanium (Yangilangan)",
            "category": self.parent_category.id,
            "description": "Yangilangan tavsif:"
            " iPhone 15 Pro Max, 256GB xotira,"
            " titanium rang. Kafolat bilan.",
            "price": 14500000,
            "new_photos": [new_image],
        }

        self.client.force_authenticate(user=self.user)

        url = reverse("my-ad", kwargs={"pk": ad.id})
        response = self.client.put(url, data, format="multipart")

        self.assertEqual(response.status_code, 200, f"Unexpected response: {response.content}")

        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["name"], data["name"])
        self.assertEqual(int(float(response.data["data"]["price"])), data["price"])

    def test_update_my_ad_patch(self):
        ad = Ad.objects.create(
            name="Old Ad",
            category=self.parent_category,
            description="Old description",
            price=1000,
            seller=self.user,
        )

        self.client.force_authenticate(user=self.user)

        data = {"price": 2000}

        url = reverse("my-ad", kwargs={"pk": ad.id})
        response = self.client.patch(url, data, format="multipart")

        self.assertEqual(response.status_code, 200, f"Unexpected response: {response.content}")

        self.assertTrue(response.data["success"])
        self.assertEqual(int(float(response.data["data"]["price"])), data["price"])
        self.assertEqual(response.data["data"]["name"], "Old Ad")

    def test_delete_my_ad(self):
        create_url = reverse("ad_create")
        image = generate_test_image()
        ad_data = {
            "name_uz": "Delete test",
            "name_ru": "Delete test",
            "category": self.child_category.id,
            "description_uz": "uz desc",
            "description_ru": "to be deleted",
            "price": "5000000.00",
            "photos": [image],
            "address": "Toshkent shahar, Mirobod tumani, Amir Temur ko'chasi 16-uy",
        }
        create_response = self.client.post(create_url, ad_data, format="multipart")
        self.assertEqual(create_response.status_code, 201)
        ad_id = create_response.data["data"]["id"]

        delete_url = reverse("my-ad", kwargs={"pk": ad_id})
        response = self.client.delete(delete_url)

        self.assertIn(response.status_code, [200, 204])
        self.assertTrue(response.data["success"])
        self.assertIsNone(response.data["data"])

    def test_product_download_by_slug(self):
        ad = Ad.objects.create(
            name="iPhone 11",
            category=self.child_category,
            description="test description",
            price=21.45,
            seller=self.user,
        )

        slug = ad.slug

        url = reverse("product-download", kwargs={"slug": slug})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.data["success"])
        data = response.data["data"]
        self.assertEqual(data["id"], ad.id)
        self.assertEqual(data["name"], ad.name)
        self.assertEqual(data["slug"], ad.slug)
        self.assertEqual(data["description"], ad.description)
        self.assertEqual(float(data["price"]), ad.price)
        self.assertEqual(data["category"]["id"], self.child_category.id)
        self.assertEqual(data["category"]["name"], self.child_category.name)
        self.assertEqual(data["seller"]["id"], self.user.id)
        self.assertEqual(data["seller"]["full_name"], self.user.full_name)

    def test_create_product_image(self):
        ad = Ad.objects.create(
            name="iPhone 11",
            category=self.child_category,
            description="test description",
            price=21.45,
            seller=self.user,
        )

        url = reverse("product-image-create")
        image = generate_test_image()
        data = {
            "image": image,
            "is_main": True,
            "product_id": ad.id,
        }

        response = self.client.post(url, data, format="multipart")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["success"])

        data_resp = response.data["data"]
        self.assertEqual(data_resp["product_id"], ad.id)
        self.assertEqual(data_resp["is_main"], True)
        self.assertIn("image", data_resp)
        self.assertIn("id", data_resp)
        self.assertIn("created_at", data_resp)

    def test_category_product_search_by_query(self):
        Category.objects.create(name="Техника")
        Category.objects.create(name="Смартфоны")

        url = reverse("category-product-search")
        response = self.client.get(url, {"q": "Техника"})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertIn("results", response.data["data"])
        self.assertEqual(len(response.data["data"]["results"]), 2)
        self.assertEqual(response.data["data"]["results"][0]["name"], "Техника")

    def test_complete_search_by_query(self):
        Ad.objects.create(
            name="vivo 53s",
            category=self.child_category,
            description="test description",
            price=3000000,
            seller=self.user,
        )
        Ad.objects.create(
            name="iPhone 11",
            category=self.child_category,
            description="test description",
            price=21000000,
            seller=self.user,
        )

        url = reverse("search-complete")
        response = self.client.get(url, {"q": "vivo"})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertIn("results", response.data["data"])
        self.assertEqual(len(response.data["data"]["results"]), 1)
        self.assertEqual(response.data["data"]["results"][0]["name"], "vivo 53s")

    def test_search_count_increase(self):
        ad = Ad.objects.create(
            name="vivo 53s",
            category=self.child_category,
            description="test description",
            price=3000000,
            seller=self.user,
        )

        search_count_obj = SearchCount.objects.create(product=ad, search_count=0)

        url = reverse("search-count", kwargs={"product_id": ad.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertIn("data", response.data)

        data = response.data["data"]
        self.assertEqual(data["id"], ad.id)
        self.assertEqual(data["category"], ad.category.id)
        self.assertEqual(data["search_count"], 1)
        self.assertIn("updated_at", data)

        search_count_obj.refresh_from_db()
        self.assertEqual(search_count_obj.search_count, 1)

    def test_search_populars(self):
        ad1 = Ad.objects.create(
            name="vivo 53s",
            category=self.child_category,
            description="desc",
            price=3000000,
            seller=self.user,
        )
        ad2 = Ad.objects.create(
            name="test ru name",
            category=self.child_category,
            description="desc",
            price=1500000,
            seller=self.user,
        )

        SearchCount.objects.create(product=ad1, search_count=4)
        SearchCount.objects.create(product=ad2, search_count=1)

        url = reverse("popular-searches")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertIn("data", response.data)
        self.assertIn("results", response.data["data"])
        self.assertIsInstance(response.data["data"]["results"], list)

        results = response.data["data"]["results"]
        self.assertGreaterEqual(len(results), 2)

        for item in results:
            self.assertIn("id", item)
            self.assertIn("name", item)
            self.assertIn("icon", item)
            self.assertIn("search_count", item)

        self.assertEqual(results[0]["search_count"], 4)
        self.assertEqual(results[1]["search_count"], 1)

    def test_create_my_search(self):
        category = Category.objects.create(name="Техника")

        from common.models import Region

        region = Region.objects.create(name="Tashkent")

        url = reverse("my-search-create")
        data = {
            "category": category.id,
            "search_query": "iPhone",
            "price_min": "1000000.00",
            "price_max": "20000000.00",
            "region_id": region.id,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["success"])

    def test_my_search_list(self):
        category = Category.objects.create(name="Смартфоны")
        from common.models import Region

        region = Region.objects.create(name="Tashkent")

        from store.models import MySearch

        my_search = MySearch.objects.create(
            user=self.user,
            category=category,
            search_query="iPhone",
            price_min=1000000,
            price_max=20000000,
            region_id=region,
        )

        url = reverse("my-search-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertIn("data", response.data)

        results = response.data["data"]
        self.assertEqual(len(results), 1)

        search_data = results[0]
        self.assertEqual(search_data["id"], my_search.id)
        self.assertEqual(search_data["category"]["id"], category.id)
        self.assertEqual(search_data["search_query"], "iPhone")
        self.assertEqual(float(search_data["price_min"]), 1000000)
        self.assertEqual(float(search_data["price_max"]), 20000000)
        self.assertEqual(search_data["region_id"], region.id)
        self.assertIn("created_at", search_data)

    def test_delete_my_search(self):
        category = Category.objects.create(name="Смартфоны")
        region = Region.objects.create(name="Tashkent")

        my_search = MySearch.objects.create(
            user=self.user,
            category=category,
            search_query="iPhone",
            price_min=1000000,
            price_max=20000000,
            region_id=region,
        )

        url = reverse("my-search-delete", kwargs={"pk": my_search.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertTrue(response.data["success"])
        self.assertIsNone(response.data["data"])

        self.assertFalse(MySearch.objects.filter(id=my_search.id).exists())
