from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from api.models import CustomUser, CustomToken
from unittest.mock import patch

class PasswordTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username="tempuser", email="temp@example.com", password="temporal123")
        self.token = CustomToken.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.reset_url = reverse("Password_reset")
        self.change_url = reverse("Password_change")

    @patch("api.chirpstack_api.get_chirpstack_user_id", return_value="mock-id-123")
    @patch("api.chirpstack_api.update_chirpstack_user_password")
    def test_password_reset(self, mock_update, mock_get_id):
        mock_update.return_value = None
        response = self.client.post(self.reset_url, {"email": self.user.email})
        self.assertEqual(response.status_code, 200)

    @patch("api.chirpstack_api.get_chirpstack_user_id", return_value="mock-id-123")
    @patch("api.chirpstack_api.update_chirpstack_user_password")
    def test_password_change(self, mock_update, mock_get_id):
        mock_update.return_value = None
        response = self.client.post(self.change_url, {
            "old_password": "temporal123",
            "new_password": "newpass123"
        })
        self.assertEqual(response.status_code, 200)