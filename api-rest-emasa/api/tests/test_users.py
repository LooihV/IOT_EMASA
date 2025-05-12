from rest_framework.test import APITestCase
from rest_framework import status
from api.models import CustomUser, CustomToken

class UserViewTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="test", email="test@example.com", password="test")
        self.token = CustomToken.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_own_user(self):
        response = self.client.get("/api/v1/Users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)