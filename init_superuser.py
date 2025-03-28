import os
import django
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

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
SITE_DOMAIN = "localhost:8000"
SITE_NAME = "localhost"

site, created = Site.objects.get_or_create(id=1, defaults={"domain": SITE_DOMAIN, "name": SITE_NAME})
if not created:
    site.domain = SITE_DOMAIN
    site.name = SITE_NAME
    site.save()
    print(f"Se actualizó django_site con domain={SITE_DOMAIN} y name={SITE_NAME}.")
else:
    print("Se creó un nuevo registro en django_site.")

print("Configuración inicial completada.")