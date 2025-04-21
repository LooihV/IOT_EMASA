import requests
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User  

CHIRPSTACK_API_URL = "http://chirpstack-rest-api:8090/api/users"
HEADERS = {
    "Authorization": f"Bearer {settings.CHIRPSTACK_JWT_TOKEN}",
    "Content-Type": "application/json"
}

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
    print("SE ejecuta signal POST save")
    print(f"Email: {instance.email} | Created: {created}")

    user_data = {
        "user": {
            "email": instance.email,
            "note": f"Sincronizado desde Django para {instance.username}",
            "isAdmin": instance.is_superuser,
            "password": instance.password #"Admin1234!"  # Siempre debe ir una contraseña válida al crear
        }
    }

    try:
        user_id = get_chirpstack_user_id(instance.email)
        print(f"User ID en ChirpStack: {user_id}")

        if created or not user_id:
            print("Creando usuario en ChirpStack (nuevo o no encontrado)...")
            response = requests.post(CHIRPSTACK_API_URL, headers=HEADERS, json=user_data)
            print(f"POST STATUS CODE: {response.status_code}")
            print(f"POST RESPONSE TEXT: {response.text}")
            response.raise_for_status()
        elif user_id:
            update_url = f"{CHIRPSTACK_API_URL}/{user_id}"
            print(f"Actualizando usuario en ChirpStack: {update_url}")
            # Eliminamos la contraseña en update para no resetearla por accidente
            user_data["user"].pop("password", None)
            response = requests.put(update_url, headers=HEADERS, json=user_data)
            print(f"PUT STATUS CODE: {response.status_code}")
            print(f"PUT RESPONSE TEXT: {response.text}")
            response.raise_for_status()
    except Exception as e:
        print(f"Excepción al sincronizar usuario: {e}")

@receiver(post_delete, sender=User)
def delete_user_from_chirpstack(sender, instance, **kwargs):
    print("Signal POST delete ejecutado")
    """Elimina el usuario de ChirpStack cuando se elimina en Django."""
    try:
        user_id = get_chirpstack_user_id(instance.email)
        if user_id:
            delete_url = f"{CHIRPSTACK_API_URL}/{user_id}"
            response = requests.delete(delete_url, headers=HEADERS)
            response.raise_for_status()
            print(f"Usuario eliminado de ChirpStack: {instance.email}")
        else:
            print(f"Usuario no encontrado en ChirpStack para eliminar: {instance.email}")
    except Exception as e:
        print(f"Error al eliminar usuario en ChirpStack: {e}")