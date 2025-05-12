from rest_framework.test import APITestCase
from unittest.mock import patch
from api.models import CustomUser, CustomToken

class DeviceActivationTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_superuser(username="test", email="test@example.com", password="test")
        self.token = CustomToken.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @patch("api.views.ChirpstackApiClient.activate_device")
    def test_activate_device(self, mock_activate):
        mock_activate.return_value = {"status": "ok"}
        response = self.client.post("/api/v1/chirpstack/devices/0000000000000001/activation/", {
            "devAddr": "01020304",
            "appSKey": "AABBCCDD00112233445566778899AABB",
            "nwkSEncKey": "FFEEDDCCBBAA99887766554433221100",
            "fCntUp": 0,
            "fCntDown": 0
        })
        self.assertEqual(response.status_code, 200)