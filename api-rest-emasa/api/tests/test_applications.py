from rest_framework.test import APITestCase
from unittest.mock import patch
from api.models import CustomUser, CustomToken, Tenant

class ApplicationTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_superuser(username="test", email="test@example.com", password="test")
        tenant = Tenant.objects.create(name="TestTenant", chirpstack_id="fake-id-123")
        self.user.tenant = tenant
        self.user.save()
        self.token = CustomToken.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @patch("api.views.ChirpstackApiClient.create_application")
    def test_create_application(self, mock_create):
        mock_create.return_value = {"id": "app123"}
        response = self.client.post("/api/v1/chirpstack/applications/", {"name": "App", "tenant_id": "123"})
        self.assertEqual(response.status_code, 201)