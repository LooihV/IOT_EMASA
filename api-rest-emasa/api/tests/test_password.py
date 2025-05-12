from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import CustomUser, CustomToken
from unittest.mock import patch

class PasswordTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="test", email="test@example.com", password="test")
        self.token = CustomToken.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.reset_url = reverse("Password_reset")
        self.change_url = reverse("Password_change")

    @patch("api.views.update_chirpstack_user_password")
    def test_password_reset(self, mock_reset):
        mock_reset.return_value = True
        response = self.client.post(self.reset_url, {"email": self.user.email})
        self.assertEqual(response.status_code, 200)

    @patch("api.views.update_chirpstack_user_password")
    def test_password_change(self, mock_change):
        self.user.set_password("temporal")
        self.user.save()
        mock_change.return_value = True
        response = self.client.post(self.change_url, {
            "old_password": "temporal",
            "new_password": "newpass123"
        })
        self.assertEqual(response.status_code, 200)