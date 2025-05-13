import os
import django
import requests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf.settings')  
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from api.models import CentralSystem

# Configurar Django
django.setup()

User = get_user_model()

SUPERUSERS = [

{"username" : os.environ.get("SUPERUSER_1_USERNAME"),
"email" : os.environ.get("SUPERUSER_1_EMAIL"),
"password" : os.environ.get("SUPERUSER_1_PASSWORD")},
{"username" : os.environ.get("SUPERUSER_2_USERNAME"),
"email" : os.environ.get("SUPERUSER_2_EMAIL"),
"password" : os.environ.get("SUPERUSER_2_PASSWORD")},
]

# URL y token de ChirpStack
CHIRPSTACK_API_BASE = os.environ.get("CHIRPSTACK_API_BASE", "http://chirpstack-rest-api:8090/api")
CHIRPSTACK_TOKEN = os.environ.get("CHIRPSTACK_JWT_TOKEN")

headers = {
    "Grpc-Metadata-Authorization": f"Bearer {CHIRPSTACK_TOKEN}",
    "Content-Type": "application/json"
}

# Crear en Django y ChirpStack
for user in SUPERUSERS:
    if not User.objects.filter(username=user["username"]).exists():
        User.objects.create_superuser(user["username"], user["email"], user["password"])
        print(f"✅ Superusuario '{user['username']}' creado en Django.")
    else:
        print(f"ℹ️ Superusuario '{user['username']}' ya existe en Django.")

    # Verifica si ya existe en ChirpStack por email
    try:
        list_resp = requests.get(f"{CHIRPSTACK_API_BASE}/users", headers=headers)
        list_resp.raise_for_status()
        exists = any(u["user"]["email"] == user["email"] for u in list_resp.json().get("result", []))

        if not exists:
            # 1. Crear usuario
            payload = {
                "user": {
                    "email": user["email"],
                    "note": f"Usuario creado desde init_superuser.py",
                    "isAdmin": True,
                    "isActive":True
                }
            }
            create_resp = requests.post(f"{CHIRPSTACK_API_BASE}/users", json=payload, headers=headers)
            create_resp.raise_for_status()
            print(f"✅ Usuario '{user['email']}' creado en ChirpStack.")

            # 2. Obtener ID del usuario recién creado
            user_id = create_resp.json()["id"]

            # 3. Establecer la contraseña correctamente
            password_payload = {"password": user["password"]}
            pass_resp = requests.post(f"{CHIRPSTACK_API_BASE}/users/{user_id}/password", json=password_payload, headers=headers)
            pass_resp.raise_for_status()
            print(f"🔐 Contraseña establecida correctamente para '{user['email']}' en ChirpStack.")
        else:
            print(f"ℹ️ Usuario '{user['email']}' ya existe en ChirpStack.")

    except Exception as e:
        print(f"❌ Error al crear usuario en ChirpStack: {e}")



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