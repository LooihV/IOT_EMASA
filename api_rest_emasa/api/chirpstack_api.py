import re
import requests
from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User  

CHIRPSTACK_API_URL = "http://chirpstack-rest-api:8090/api/users"
HEADERS = {
    "Authorization": f"Bearer {settings.CHIRPSTACK_JWT_TOKEN}",
    "Content-Type": "application/json"
}

def is_valid_email(email):
    """Valida si un string es un correo electrónico válido."""
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def get_chirpstack_user_id(email):
    """Busca el ID de un usuario en ChirpStack por su email."""
    try:
        response = requests.get(CHIRPSTACK_API_URL, headers=HEADERS)
        response.raise_for_status()
        users = response.json().get("result", [])
        for user in users:
            if user["email"] == email:
                return user["id"]
    except Exception as e:
        print(f"Error buscando usuario en ChirpStack: {e}")
    return None

@receiver(post_save, sender=User)
def sync_user_to_chirpstack(sender, instance, created, **kwargs):
    print(" Signal POST save ejecutado")
    print(f"Email: {instance.email} | Created: {created}")

    if not is_valid_email(instance.email):
        print("Email inválido, no se sincroniza con ChirpStack.")
        return

    user_data = {
        "user": {
            "email": instance.email,
            "note": f"Sincronizado desde Django para {instance.username}",
            "isAdmin": instance.is_superuser,
            "password": instance.password
        }
    }

    try:
        user_id = get_chirpstack_user_id(instance.email)
        print(f"User ID en ChirpStack: {user_id}")

        if created or not user_id:
            print(" Creando usuario en ChirpStack...")
            response = requests.post(CHIRPSTACK_API_URL, headers=HEADERS, json=user_data)
            print(f" POST STATUS: {response.status_code} | RESPUESTA: {response.text}")
            response.raise_for_status()
        else:
            update_url = f"{CHIRPSTACK_API_URL}/{user_id}"
            user_data["user"].pop("password", None)  
            print(f"🔄 Actualizando usuario en ChirpStack: {update_url}")
            response = requests.put(update_url, headers=HEADERS, json=user_data)
            print(f"✅ PUT STATUS: {response.status_code} | RESPUESTA: {response.text}")
            response.raise_for_status()
    except Exception as e:
        print(f"❌ Excepción al sincronizar usuario: {e}")

@receiver(pre_delete, sender=User)
def delete_user_from_chirpstack(sender, instance, **kwargs):
    print(" Signal PRE delete ejecutado")

    if not is_valid_email(instance.email):
        print("❌ Email inválido, no se elimina de ChirpStack.")
        return

    try:
        user_id = get_chirpstack_user_id(instance.email)
        if user_id:
            delete_url = f"{CHIRPSTACK_API_URL}/{user_id}"
            response = requests.delete(delete_url, headers=HEADERS)
            response.raise_for_status()
            print(f"✅ Usuario eliminado de ChirpStack: {instance.email}")
        else:
            print(f"⚠️ Usuario no encontrado en ChirpStack para eliminar: {instance.email}")
    except Exception as e:
        print(f"❌ Error al eliminar usuario en ChirpStack: {e}")