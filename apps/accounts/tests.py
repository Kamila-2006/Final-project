# apps/accounts/tests.py
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from store.models import Category

User = get_user_model()


class AccountsEndpointsTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")

        self.approved_user = User.objects.create_user(
            full_name="Approved User",
            project_name="Project",
            category=self.category,
            phone_number="+998901234567",
            password="testpass123",
            status="approved",
        )

        self.pending_user = User.objects.create_user(
            full_name="Pending User",
            project_name="Project",
            category=self.category,
            phone_number="+998909876543",
            password="testpass123",
            status="pending",
        )

    def test_seller_registration(self):
        url = reverse("seller_registration")
        payload = {
            "full_name": "New Seller",
            "project_name": "Project X",
            "category": self.category.id,
            "phone_number": "+998900000000",
            "address": {"name": "Tashkent", "lat": 41.3111, "long": 69.2797},
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data.get("full_name"), payload["full_name"])
        self.assertTrue(User.objects.filter(phone_number=payload["phone_number"]).exists())

    def test_login_approved_user(self):
        url = reverse("token_obtain_pair")
        payload = {"phone_number": self.approved_user.phone_number, "password": "testpass123"}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

    def test_login_pending_user_fails(self):
        url = reverse("token_obtain_pair")
        payload = {"phone_number": self.pending_user.phone_number, "password": "testpass123"}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertTrue(any("not approved" in str(err).lower() for err in response.data.values()))

    def test_token_refresh(self):
        refresh = RefreshToken.for_user(self.approved_user)
        url = reverse("token_refresh")
        response = self.client.post(url, {"refresh": str(refresh)}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertIn("access", response.data)

    def test_token_verify_valid_and_invalid(self):
        refresh = RefreshToken.for_user(self.approved_user)
        access_token = str(refresh.access_token)
        url = reverse("token_verify")

        # valid
        response = self.client.post(url, {"token": access_token}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertTrue(response.data.get("valid", False))

        # invalid
        response_invalid = self.client.post(url, {"token": "invalidtoken"}, format="json")
        self.assertEqual(
            response_invalid.status_code, status.HTTP_401_UNAUTHORIZED, response_invalid.data
        )
        self.assertFalse(response_invalid.data.get("valid", True))

    def test_user_profile_view(self):
        self.client.force_authenticate(user=self.approved_user)
        url = reverse("user_profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data.get("full_name"), self.approved_user.full_name)

    def test_user_profile_edit(self):
        self.client.force_authenticate(user=self.approved_user)
        url = reverse("user_edit")
        payload = {
            "full_name": "Updated Name",
            "address": {"name": "New Address", "lat": 40.0, "long": 70.0},
        }
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.approved_user.refresh_from_db()
        self.assertEqual(self.approved_user.full_name, "Updated Name")
        self.assertEqual(self.approved_user.address.name, "New Address")
