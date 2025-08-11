from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Category

from .models import Address

User = get_user_model()


class SellerRegistrationTest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Test Category")

        self.approved_user = User.objects.create_user(
            full_name="Abdurahmanova Kamila",
            project_name="Test Project",
            category=self.category,
            phone_number="998994053129",
            status="approved",
            password="secretpassword",
        )

        self.pending_user = User.objects.create_user(
            full_name="Pending User",
            project_name="Test Project",
            category=self.category,
            phone_number="998900000000",
            status="pending",
            password="secretpassword",
        )

        login_url = reverse("token_obtain_pair")
        login_data = {"phone_number": "998994053129", "password": "secretpassword"}
        login_response = self.client.post(login_url, login_data, format="json")
        self.access_token = login_response.data["data"]["access_token"]

        self.user = self.approved_user

        Address.objects.create(
            user=self.approved_user,
            name="Initial address",
            lat=41.0,
            long=69.0,
        )

    def test_seller_registration(self):
        url = reverse("seller_registration")
        data = {
            "full_name": "Karimov Akmal Rustamovich",
            "project_name": "TechnoMart Online Do'koni",
            "category": self.category.id,
            "phone_number": "+998971234558",
            "address": {
                "name": "Toshkent shahar, Mirobod tumani, Amir Temur ko'chasi 15-uy",
                "lat": 41.299496,
                "long": 69.240073,
            },
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(response.data["success"])

        self.assertEqual(response.data["data"]["full_name"], data["full_name"])
        self.assertEqual(response.data["data"]["project_name"], data["project_name"])
        self.assertEqual(response.data["data"]["category"], self.category.id)
        self.assertEqual(response.data["data"]["phone_number"], data["phone_number"])
        self.assertEqual(response.data["data"]["status"], "pending")

        self.assertIn("id", response.data["data"])

    def test_login_approved_user(self):
        url = reverse("token_obtain_pair")
        data = {"phone_number": "998994053129", "password": "secretpassword"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertIn("access_token", response.data["data"])
        self.assertIn("refresh_token", response.data["data"])
        self.assertEqual(response.data["data"]["user"]["full_name"], "Abdurahmanova Kamila")
        self.assertEqual(response.data["data"]["user"]["phone_number"], "998994053129")

    def test_login_pending_user_fails(self):
        url = reverse("token_obtain_pair")
        data = {"phone_number": "998900000000", "password": "secretpassword"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])

        self.assertTrue(
            any(
                "Your account is not approved yet." in err.get("message", [])
                for err in response.data.get("errors", [])
            )
        )

    def test_token_refresh(self):
        login_url = reverse("token_obtain_pair")
        login_data = {"phone_number": "998994053129", "password": "secretpassword"}
        login_response = self.client.post(login_url, login_data, format="json")
        refresh_token = login_response.data["data"]["refresh_token"]

        refresh_url = reverse("token_refresh")
        response = self.client.post(refresh_url, {"refresh": refresh_token}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_token_verify_valid(self):
        url = reverse("token_verify")
        response = self.client.post(url, {"token": self.access_token}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertTrue(response.data["data"]["valid"])
        self.assertEqual(response.data["data"]["user_id"], str(self.approved_user.guid))

    def test_token_verify_invalid(self):
        url = reverse("token_verify")
        response = None
        try:
            response = self.client.post(url, {"token": "invalidtoken"}, format="json")
        except Exception as e:
            self.assertIn("Token is invalid", str(e))

        if response:
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertFalse(response.data["success"])
            self.assertFalse(response.data["data"]["valid"])

    def test_get_current_user(self):
        login_url = reverse("token_obtain_pair")
        login_data = {"phone_number": "998994053129", "password": "secretpassword"}
        login_response = self.client.post(login_url, login_data, format="json")
        access_token = login_response.data["data"]["access_token"]

        url = reverse("user_profile")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["id"], self.approved_user.id)
        self.assertEqual(response.data["data"]["full_name"], self.approved_user.full_name)
        self.assertEqual(response.data["data"]["phone_number"], self.approved_user.phone_number)
        self.assertIn("profile_photo", response.data["data"])
        self.assertIn("address", response.data["data"])

    def test_put_edit_account(self):
        login_url = reverse("token_obtain_pair")
        login_data = {"phone_number": "998994053129", "password": "secretpassword"}
        login_response = self.client.post(login_url, login_data, format="json")
        access_token = login_response.data["data"]["access_token"]

        url = reverse("user_edit")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        put_data = {
            "full_name": "Karimov Rustam Akmalovich",
            "phone_number": "+998971234568",
            "address": {
                "name": "Toshkent shahar, Mirobod tumani, Amir Temur ko'chasi 16-uy",
                "lat": 41.299436,
                "long": 69.240072,
            },
        }
        response = self.client.put(url, put_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["full_name"], put_data["full_name"])
        self.assertEqual(response.data["data"]["phone_number"], put_data["phone_number"])
        self.assertEqual(response.data["data"]["address"]["name"], put_data["address"]["name"])
        self.assertEqual(response.data["data"]["address"]["lat"], put_data["address"]["lat"])
        self.assertEqual(response.data["data"]["address"]["long"], put_data["address"]["long"])

    def test_patch_edit_account(self):
        login_url = reverse("token_obtain_pair")
        login_data = {"phone_number": "998994053129", "password": "secretpassword"}
        login_response = self.client.post(login_url, login_data, format="json")
        access_token = login_response.data["data"]["access_token"]

        url = reverse("user_edit")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        patch_data = {"full_name": "Karimov Akmal Rustamovich"}
        response = self.client.patch(url, patch_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["full_name"], patch_data["full_name"])

        self.assertIn("phone_number", response.data["data"])
        self.assertIn("address", response.data["data"])
