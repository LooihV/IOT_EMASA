import os
import django
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from api.models import CentralSystem

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf.settings')  # Asegúrate de que 'drf' sea el nombre correcto de tu módulo
django.setup()

# Crear Superusuario
User = get_user_model()
SUPERUSER_USERNAME = "EMASADOCK"
SUPERUSER_EMAIL = "admin@example.com"
SUPERUSER_PASSWORD = "emasa123"

if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
    User.objects.create_superuser(SUPERUSER_USERNAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD)
    print(f"Superusuario '{SUPERUSER_USERNAME}' creado con éxito.")
else:
    print("Superusuario ya existe, no se creó uno nuevo.")

# Crear registro en django_site
SITE_ID = 1
SITE_DOMAIN = "localhost:8000"
SITE_NAME = "Mi Sitio Local"

site, created = Site.objects.update_or_create(
    id=SITE_ID,
    defaults={"domain": SITE_DOMAIN, "name": SITE_NAME},
)

if created:
    print(f"✅ Sitio creado con ID {SITE_ID}, dominio {SITE_DOMAIN}")
else:
    print(f"✅ Sitio actualizado con ID {SITE_ID}, dominio {SITE_DOMAIN}")


CENTRAL_NAME = "EMASA"

if not CentralSystem.objects.filter(name=CENTRAL_NAME).exists():
    CentralSystem.objects.create(name=CENTRAL_NAME)
    print("La central se creò con èxito")
else:
    print("Ya existe una central")