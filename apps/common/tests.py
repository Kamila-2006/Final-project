from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import District, Page, Region, Setting


class CommonEndpointsTests(APITestCase):
    def setUp(self):
        self.page = Page.objects.create(title="Test Page", content="This is a test page content")

        self.region = Region.objects.create(name="Test Region")
        self.district = District.objects.create(name="Test District", region=self.region)

        self.setting = Setting.objects.create(
            phone="+998900000000",
            support_email="support@test.com",
            working_hours="Mon-Fri 9:00-18:00",
            app_version="1.0.0",
            maintenance_code=False,
        )

    def test_common_pages_list(self):
        url = reverse("common_pages")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])

        # Проверяем, что данные — список или словарь с results
        data = response.data["data"]
        pages = data.get("results") if isinstance(data, dict) and "results" in data else data

        self.assertTrue(any(page["title"] == self.page.title for page in pages))

    def test_regions_with_districts(self):
        url = reverse("regions_with_districts")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])

        data = response.data["data"]
        regions = data.get("results") if isinstance(data, dict) and "results" in data else data

        self.assertTrue(any(region["name"] == self.region.name for region in regions))

    def test_regions_with_districts_empty(self):
        Region.objects.all().delete()
        url = reverse("regions_with_districts")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])

        data = response.data["data"]
        regions = data.get("results") if isinstance(data, dict) and "results" in data else data

        self.assertEqual(len(regions), 0)
