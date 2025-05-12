from rest_framework.test import APITestCase
from unittest.mock import patch
from api.models import CustomUser, CustomToken

class GatewayTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_superuser(username="test", email="test@example.com", password="test")
        self.token = CustomToken.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @patch("api.views.ChirpstackApiClient.register_gateway")
    def test_register_gateway(self, mock_register):
        mock_register.return_value = {"id": "gw123"}
        response = self.client.post("/api/v1/chirpstack/gateways/", {"name": "GW"})
        self.assertEqual(response.status_code, 201)