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
        self.assertTrue(
            any(page["title"] == self.page.title for page in response.data["data"]["results"])
        )

    def test_common_page_detail(self):
        url = reverse("common_page_detail", kwargs={"slug": self.page.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["title"], self.page.title)

    def test_common_page_detail_not_found(self):
        url = reverse("common_page_detail", kwargs={"slug": "non-existent"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data["success"])
        self.assertIn("errors", response.data)

    def test_regions_with_districts(self):
        url = reverse("regions_with_districts")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertTrue(
            any(region["name"] == self.region.name for region in response.data["data"]["results"])
        )

    def test_regions_with_districts_empty(self):
        Region.objects.all().delete()
        url = reverse("regions_with_districts")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(len(response.data["data"]["results"]), 0)

    def test_common_settings(self):
        url = reverse("common-settings")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])

        data = response.data["data"]
        if isinstance(data, dict) and "results" in data:
            items = data["results"]
        else:
            items = data

        self.assertTrue(any(setting["phone"] == self.setting.phone for setting in items))

    def test_common_settings_empty(self):
        Setting.objects.all().delete()
        url = reverse("common-settings")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])

        data = response.data["data"]
        if isinstance(data, dict) and "results" in data:
            items = data["results"]
        else:
            items = data

        self.assertEqual(len(items), 0)
