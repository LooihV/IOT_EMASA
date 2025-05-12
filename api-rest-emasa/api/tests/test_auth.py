from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import CustomUser, CustomToken

class AuthTokenTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="test", email="test@example.com", password="test")
        self.url = reverse("Custom-token")

    def test_obtain_token_success(self):
        response = self.client.post(self.url, {"username": "test", "password": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_obtain_token_invalid(self):
        response = self.client.post(self.url, {"username": "test", "password": "wrongpass"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)