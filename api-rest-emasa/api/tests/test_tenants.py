from rest_framework.test import APITestCase
from rest_framework import status
from api.models import CustomUser, Tenant, CustomToken

class TenantTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_superuser(username="test", email="test@example.com", password="test")
        self.token = CustomToken.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_list_tenants(self):
        response = self.client.get("/api/v1/Tenants/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)