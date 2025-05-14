from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from api.models import CustomUser, CustomToken
from unittest.mock import patch

class PasswordTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="tempuser",
            email="temp@example.com",
            password="temporal123"
        )
        self.token = CustomToken.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.reset_url = reverse("Password_reset")
        self.change_url = reverse("Password_change")

    @patch("api.chirpstack_api.requests.post")
    @patch("api.chirpstack_api.get_chirpstack_user_id", return_value="mock-id-123")
    def test_password_reset_and_change(self, mock_get_id, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {}

        # Paso 1: resetear contraseña temporal (simula email recibido)
        reset_response = self.client.post(self.reset_url, {"email": self.user.email})
        self.assertEqual(reset_response.status_code, 200)

        # Simula la nueva contraseña temporal que se habría enviado al email
        temp_password = "mocktemp123"
        self.user.set_password(temp_password)
        self.user.save()

        # Paso 2: cambiar esa contraseña temporal por la definitiva
        change_response = self.client.post(self.change_url, {
            "old_password": temp_password,
            "new_password": "newsecurepass456"
        })
        self.assertEqual(change_response.status_code, 200)