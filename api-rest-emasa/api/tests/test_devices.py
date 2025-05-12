from rest_framework.test import APITestCase
from unittest.mock import patch
from api.models import CustomUser, CustomToken

class DeviceTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_superuser(username="test", email="test@example.com", password="test")
        self.token = CustomToken.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @patch("api.views.ChirpstackApiClient.create_device")
    def test_create_device(self, mock_create):
        mock_create.return_value = {"id": "dev123"}
        response = self.client.post("/api/v1/chirpstack/devices/", {"name": "Device"})
        self.assertEqual(response.status_code, 201)