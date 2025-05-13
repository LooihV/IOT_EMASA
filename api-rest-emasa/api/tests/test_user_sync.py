from django.test import TestCase
from unittest.mock import patch
from api.models import CustomUser
from api.chirpstack_api import sync_user_to_chirpstack, delete_user_from_chirpstack

class UserChirpstackSyncTest(TestCase):
    @patch("api.chirpstack_api.requests.post")
    def test_user_creation_triggers_chirpstack_sync(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"id": "user-123"}

        user = CustomUser.objects.create_user(username="test", email="test@example.com", password="test")
        sync_user_to_chirpstack(CustomUser, user, True, password_plaintext="test")

        self.assertTrue(mock_post.called)
        called_url = mock_post.call_args[0][0]
        self.assertIn("/api/users", called_url)

    @patch("api.chirpstack_api.requests.get")
    @patch("api.chirpstack_api.requests.delete")
    def test_user_deletion_triggers_chirpstack_delete(self, mock_delete, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": [{"email": "delete@example.com", "id": "user-456"}]
        }
        mock_delete.return_value.status_code = 200

        user = CustomUser.objects.create_user(username="deleteuser", email="delete@example.com", password="pass")
        user.delete()

        self.assertTrue(mock_delete.called)
        called_url = mock_delete.call_args[0][0]
        self.assertIn("/api/users/user-456", called_url)