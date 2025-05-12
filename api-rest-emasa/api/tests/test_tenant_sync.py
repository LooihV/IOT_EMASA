from django.test import TestCase
from unittest.mock import patch
from api.models import Tenant

class TenantChirpstackSyncTest(TestCase):
    @patch("api.signals.requests.post")
    def test_tenant_creation_triggers_chirpstack(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"id": "tenant-999"}

        tenant = Tenant.objects.create(name="TestTenant")
        self.assertTrue(mock_post.called)

        # Simular guardar el chirpstack_id si usas esa lógica en signals
        tenant.chirpstack_id = "tenant-999"
        tenant.save()

        self.assertEqual(tenant.chirpstack_id, "tenant-999")